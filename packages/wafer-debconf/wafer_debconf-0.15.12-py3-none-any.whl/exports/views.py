from collections.abc import Iterable
import csv

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView

from wafer.talks.models import Talk

from bursary.models import Bursary
from front_desk.models import CheckIn
from invoices.models import Invoice
from register.dates import nights
from register.models import (
    Accomm, AccommNight, Attendee, ChildCare, Meal, Visa)


class CSVExportView(ListView):
    """Export the given columns for the model as CSV."""
    columns = None
    filename = None

    def get_data_line(self, instance):
        ret = []
        for column in self.columns:
            obj = instance
            for component in column.split('.'):
                try:
                    obj = getattr(obj, component)
                except ObjectDoesNotExist:
                    obj = '%s missing!' % component
                    break
                except AttributeError:
                    obj = getattr(self, component)(obj)
                if not obj:
                    break
                if callable(obj):
                    obj = obj()
            if (not isinstance(obj, (str, bytes))
                    and isinstance(obj, Iterable)):
                ret.extend(str(i) for i in obj)
            else:
                ret.append(str(obj))

        return ret

    def write_rows(self, writer, objects):
        for instance in objects:
            writer.writerow(self.get_data_line(instance))

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            'attachment; filename="%s"' % self.filename
        )

        writer = csv.writer(response)
        writer.writerow(self.columns)
        self.write_rows(writer, context['object_list'])

        return response


class AttendeeAdminMixin(PermissionRequiredMixin):
    permission_required = 'register.change_attendee'


class AttendeeBadgeExport(AttendeeAdminMixin, CSVExportView):
    name = 'Attendee badges'
    model = Attendee
    filename = "attendee_badges.csv"
    ordering = ('user__username',)
    columns = [
        'user.username', 'reconfirm', 'user.email', 'user.get_full_name',
        'nametag_2', 'nametag_3', 'languages', 'food.diet',
    ]


class AttendeeAccommExport(AttendeeAdminMixin, CSVExportView):
    name = 'Accommodation'
    model = Accomm
    filename = "attendee_accommodation.csv"
    ordering = ('attendee__user__username',)
    columns = [
        'attendee.user.username', 'attendee.user.get_full_name',
        'attendee.user.email', 'attendee.reconfirm', 'attendee.paid',
        'attendee.user.attendee.arrived',
        'accomm_bursary', 'attendee.gender',
        'attendee.country', 'option', 'requirements',
        'family_usernames', 'get_checkin_checkouts', 'room',
    ]

    def accomm_bursary(self, accomm):
        try:
            bursary = accomm.attendee.user.bursary
        except ObjectDoesNotExist:
            return ''
        if not bursary.request_accommodation:
            return ''
        return bursary.accommodation_status


class AccommNightsExport(AttendeeAdminMixin, CSVExportView):
    name = 'Accommodation Nights'
    model = AccommNight
    filename = "accommodation_nights.csv"
    columns = [
        'night', 'option', 'paid', 'bursary_accepted', 'bursary_pending',
        'bursary_submitted', 'unknown',
    ]

    def write_rows(self, writer, objects):
        for night in nights(orga=True):
            for option in settings.PRICES['accomm'].keys():
                writer.writerow(self.get_night_data(night, option))

    def get_night_data(self, night, option):
        accomm_night = AccommNight.objects.get(date=night)
        paid = 0
        unknown = 0
        bursaried = {
            'accepted': 0,
            'pending': 0,
            'submitted': 0,
        }
        for accomm in accomm_night.accomm_set.filter(option=option):
            try:
                bursary = accomm.attendee.user.bursary
            except ObjectDoesNotExist:
                bursary = None
            if bursary and bursary.potential_bursary('accommodation'):
                bursaried[bursary.accommodation_status] += 1
            elif accomm.attendee.paid():
                paid += 1
            else:
                unknown += 1
        return [night, option, paid, bursaried['accepted'],
                bursaried['pending'], bursaried['submitted'], unknown]


class ChildCareExport(AttendeeAdminMixin, CSVExportView):
    name = 'Childcare'
    model = ChildCare
    filename = "attendee_child_care.csv"
    ordering = ('attendee__user__username',)
    columns = [
        'attendee.user.username', 'attendee.user.get_full_name',
        'attendee.user.email', 'attendee.reconfirm', 'attendee.paid',
        'attendee.user.bursary.accommodation_status',
        'attendee.arrival', 'attendee.departure',
        'needs', 'details',
    ]


class TalksExport(PermissionRequiredMixin, CSVExportView):
    name = 'Talks'
    model = Talk
    permission_required = 'talks.edit_private_notes'
    filename = "talk_evaluations.csv"
    ordering = ("talk_id",)
    columns = [
        'talk_id', 'title', 'get_authors_display_name', 'abstract',
        'talk_type.name', 'track.name', 'get_status_display', 'review_score',
        'review_count', 'notes', 'private_notes', 'all_review_comments',
    ]

    def all_review_comments(self, talk):
        return [
            "(%s) %s" % (review.reviewer.username, review.notes.raw)
            for review in talk.reviews.all()
            if review.notes.raw
        ]


class FoodExport(AttendeeAdminMixin, CSVExportView):
    name = 'Food'
    model = Meal
    filename = "meals.csv"
    ordering = ('date', 'meal',)
    columns = [
        'date', 'meal', 'total', 'total_unconfirmed',
        'regular', 'vegetarian', 'vegan', 'gluten_free',
        'other', 'other_details',
    ]

    def render_to_response(self, context, **response_kwargs):
        self._confirmed_attendees = {}
        return super().render_to_response(context, **response_kwargs)

    def attendee_confirmed(self, attendee_id):
        if attendee_id not in self._confirmed_attendees:
            if CheckIn.objects.filter(attendee_id=attendee_id).exists():
                return True

            attendee = Attendee.objects.get(id=attendee_id)
            paid = attendee.paid()

            try:
                bursary = Bursary.objects.get(user=attendee.user)
            except Bursary.DoesNotExist:
                bursary = Bursary()

            confirmed = any((
                not bursary.request_any and attendee.billable() and paid,
                not bursary.request_any and not attendee.billable() and attendee.final_dates,
                bursary.request_any and bursary.status_in(None, ['accepted']),
                attendee.reconfirm,
            ))
            self._confirmed_attendees[attendee_id] = confirmed
        return self._confirmed_attendees[attendee_id]

    def get_data_line(self, meal):
        row = {
            'date': meal.date.isoformat(),
            'meal': meal.meal,
            'total': 0,
            'total_unconfirmed': meal.food_set.count(),
            'regular': 0,
            'vegetarian': 0,
            'vegan': 0,
            'gluten_free': 0,
            'other': 0,
            'other_details': [],
        }

        for food in meal.food_set.all():
            if not self.attendee_confirmed(food.attendee_id):
                continue

            diet = food.diet
            if diet == '':
                diet = 'regular'
            elif diet == 'other':
                details = [food.attendee.user.username]
                details.append(food.special_diet)
                row['other_details'].append(': '.join(details))
            row[diet] += 1
            row['total'] += 1

        row['other_details'] = ', '.join(row['other_details'])
        return [row.get(key) for key in self.columns]


class SpecialDietExport(AttendeeAdminMixin, CSVExportView):
    name = 'Special diets'
    filename = "diets.csv"
    ordering = ('attendee__user__username',)
    columns = [
        'username', 'name', 'confirmed', 'diet', 'special_diet'
    ]

    def attendee_confirmed(self, attendee):
        try:
            if attendee.check_in:
                return True
        except CheckIn.DoesNotExist:
            pass

        if attendee.reconfirm:
            return True

        paid = attendee.paid()

        try:
            bursary = attendee.user.bursary
        except Bursary.DoesNotExist:
            bursary = Bursary()

        return any((
            not bursary.request_any and attendee.billable() and paid,
            not bursary.request_any and not attendee.billable() and attendee.final_dates,
            bursary.request_any and bursary.status_in(None, ['accepted']),
        ))

    def get_queryset(self):
        return Meal.objects.get(**self.kwargs).food_set.exclude(
                special_diet__exact='',
                diet__exact='',
            ).select_related(
                'attendee',
                'attendee__user',
                'attendee__user__bursary',
                'attendee__user__userprofile',
            ).order_by(*self.ordering)

    def get_data_line(self, food):
        row = {
            'username': food.attendee.user.username,
            'name': food.attendee.user.userprofile.display_name(),
            'confirmed': self.attendee_confirmed(food.attendee),
            'diet': food.diet,
            'special_diet': food.special_diet,
        }
        return [row.get(key) for key in self.columns]

    def write_rows(self, writer, objects):
        super().write_rows(writer, objects)
        count = {True: 0, False: 0}
        for food in Meal.objects.get(**self.kwargs).food_set.filter(
                special_diet__exact='',
                diet__exact='',
            ).select_related(
                'attendee',
                'attendee__user',
                'attendee__user__userprofile',
            ):
            count[self.attendee_confirmed(food.attendee)] += 1
        for confirmed in (True, False):
            row = {
                'username': '*',
                'name': 'Everyone Else - {} people'.format(count[confirmed]),
                'confirmed': confirmed,
                'diet': '',
                'special_diet': '',
            }
            writer.writerow([row.get(key) for key in self.columns])


class BursaryExport(AttendeeAdminMixin, CSVExportView):
    name = 'Bursaries'
    filename = "bursaries.csv"

    columns = [
        'user.username',
        'user.userprofile.display_name',
        'user.email',
        'user.attendee.arrived',
        'user.attendee.country',
        'travel_from',
        'travel_status',
        'food_status',
        'accommodation_status',
        'expenses_status',
    ]

    approved = ('pending', 'accepted',)

    def get_queryset(self):
        return Bursary.objects.filter(
            Q(travel_status__in=self.approved)
            | Q(food_status__in=self.approved)
            | Q(accommodation_status__in=self.approved)
            | Q(expenses_status__in=self.approved)
        ).exclude(
            user__attendee__id=None, # exclude unregistered people
        ).prefetch_related(
            'user',
            'user__attendee',
            'user__userprofile',
        ).order_by('user__username')


class FingerprintExport(AttendeeAdminMixin, CSVExportView):
    name = 'Fingerprints'
    filename = 'fingerprints.csv'

    queryset = Attendee.objects.exclude(pgp_fingerprints='')
    columns = (
        'user.username',
        'user.userprofile.display_name',
        'user.email',
        'pgp_fingerprints',
        'keysigning_id',
    )


class InvoiceExport(AttendeeAdminMixin, CSVExportView):
    name = 'Invoices'
    filename = 'invoices.csv'

    queryset = Invoice.objects.all()
    ordering = ('reference_number',)
    columns = (
        'reference_number',
        'status',
        'date',
        'last_update',
        'recipient.username',
        'recipient.userprofile.display_name',
        'compound',
        'transaction_id',
        'total',
    )


class VisaExport(AttendeeAdminMixin, CSVExportView):
    name = 'Visas'
    filename = 'visas.csv'

    queryset = Visa.objects.all()
    columns = (
        'attendee.user.username',
        'attendee.user.userprofile.display_name',
        'attendee.user.email',
        'country',
        'travel_bursary_status',
        'accommodation_bursary_status',
        'food_bursary_status',
        'attendance_approval_status',
    )

    def _bursary_status(self, visa, attribute, non_existent_value=''):
        try:
            bursary = visa.attendee.user.bursary
        except ObjectDoesNotExist:
            return non_existent_value
        if attribute != 'attendance':
            if not getattr(bursary, f'request_{attribute}'):
                return non_existent_value
        return getattr(bursary, f'{attribute}_status')

    def travel_bursary_status(self, visa):
        return self._bursary_status(visa, 'travel')

    def accommodation_bursary_status(self, visa):
        return self._bursary_status(visa, 'accommodation')

    def food_bursary_status(self, visa):
        return self._bursary_status(visa, 'food')

    def attendance_approval_status(self, visa):
        return self._bursary_status(visa, 'attendance')
