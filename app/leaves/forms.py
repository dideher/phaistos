from datetime import datetime, timedelta
from django import forms
from leaves.models import Leave, LeaveType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from employees.models import Employee, EmployeeType
from leaves.models import LeaveType
from bootstrap_modal_forms.forms import BSModalModelForm
from phaistos.commons.forms import EmptyChoiceField
from phaistos.commons.widgets import DatePickerInput

blank_choice = [('', '-----------------'), ]


class DeleteLeaveForm(BSModalModelForm):
    class Meta:
        model = Leave
        fields = ['deleted_comment', ]

        widgets = {
            'deleted_comment': forms.Textarea(attrs={'rows': 4}),
        }


class LeaveForm(BSModalModelForm):
    class Meta:
        model = Leave
        fields = ['date_from', 'date_until', 'leave_type', 'comment', 'number_of_days', 'effective_number_of_days']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'date_from': DatePickerInput(),
            'date_until': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        self.employee: Employee = get_object_or_404(Employee, pk=kwargs.pop('employee_id'))
        super().__init__(*args, **kwargs)

        self.fields['leave_type'].queryset = LeaveType.objects.filter(
            suitable_for_employee_type=self.employee.employee_type).order_by('legacy_code')
        self.fields['number_of_days'].widget.attrs['readonly'] = True

    def clean_leave_type(self):
        data: LeaveType = self.cleaned_data['leave_type']

        if data.suitable_for_employee_type != self.employee.employee_type:
            # ops! leave type is not good for the given employee type
            raise ValidationError(_("Ο τύπος άδειας δεν είναι συμβατός με τον εκπαιδευτικό"))

        return data

    def clean_effective_number_of_days(self):
        data = self.cleaned_data['effective_number_of_days']

        if data <= 0:
            raise ValidationError(_("Η διάρκεια των ημερών άδειας πρέπει να είναι μεγαλύτερη του 0"))

        return data

    def clean_number_of_days(self):

        data = self.cleaned_data

        date_from: datetime.date = data.get("date_from")
        date_until: datetime.date = data.get("date_until")

        if date_from is not None and date_until is not None:
            data['number_of_days'] = ((date_until - date_from) + timedelta(days=1)).days

        return data['number_of_days']

    def clean(self):
        """
        Validates the leave's date_from and date_until
        """
        cleaned_data = super().clean()

        date_from = cleaned_data.get("date_from")
        date_until = cleaned_data.get("date_until")

        if date_from and date_until and date_from > date_until:
            self.add_error('date_until', _('Η ημ/νία λήξης της άδειας είναι προγενέστερη της έναρξης'))

        return cleaned_data


class LeaveSearchForm(forms.Form):

    GREATER_THAN_OR_EQUAL = '>='
    EQUAL_TO = '='
    LESS_THAN_OR_EQUAL = '<='

    EFFECTIVE_DAYS_OPERATOR_CHOICES = [
        (GREATER_THAN_OR_EQUAL, _('Περισσότερες απο')),
        (EQUAL_TO, _('Ίσες με')),
        (LESS_THAN_OR_EQUAL, _('Λιγότερες απο'))
    ]

    DATE_OPERATOR_CHOICES = [
        (GREATER_THAN_OR_EQUAL, _('Μεταγενέστερη')),
        (EQUAL_TO, _('Ίση Με')),
        (LESS_THAN_OR_EQUAL, _('Προγενέστερη'))
    ]

    effective_days_operator = forms.ChoiceField(choices=EFFECTIVE_DAYS_OPERATOR_CHOICES, initial=GREATER_THAN_OR_EQUAL,
                                                label=_('Τελεστής Σύγκρισης Ημερών Άδειας'),
                                                help_text=_(
                                                    'Διαμορφώστε τον τρόπο ερμηνείας των ημερών άδειας '
                                                    'κατά την σύγκριση'),
                                                required=False)
    effective_days = forms.IntegerField(label="Αριθμός Ημερών",
                                        required=False,
                                        help_text=_('Περιορίστε τα αποτελέσματα με βάση την διάρκεια της άδειας'))
    leave_type = forms.ModelMultipleChoiceField(label="Τύπος Άδειας", queryset=LeaveType.objects.all(),
                                                help_text=_('Περιορίστε την αναζήτηση με βάση τον τύπο της άδειας. '
                                                            'Μπορείτε να επιλέξετε περισσότερους τύπους'),
                                                required=False,
                                                widget=forms.SelectMultiple(attrs={'size': 9}))

    employee_type = EmptyChoiceField(choices=EmployeeType.choices,
                                     empty_label='',
                                     label=_("Τύπος Εργαζόμενου"),
                                     help_text=_("Περιόριστε την αναζήτηση με βάση τον τύπο του εργαζόμενου"),
                                     required=False)

    date_from_operator = forms.ChoiceField(choices=DATE_OPERATOR_CHOICES,
                                           initial=GREATER_THAN_OR_EQUAL,
                                           label=_('Τελεστής Σύγκρισης Έναρξης Άδειας'),
                                           help_text=_(
                                               'Διαμορφώστε τον τρόπο ερμηνείας της ημ/νιας έναρξης της '
                                               'άδειας κατά την σύγκριση'),
                                           required=False)
    date_from = forms.DateField(label="Ημ/νια Έναρξης", required=False, widget=DatePickerInput,
                                help_text=_('Περιορίστε με βάση την ημ/νια έναρξης της άδειας'))

    date_until_operator = forms.ChoiceField(choices=DATE_OPERATOR_CHOICES, initial=LESS_THAN_OR_EQUAL,
                                            label=_('Τελεστής Σύγκρισης Λήξης Άδειας'),
                                            help_text=_(
                                                'Διαμορφώστε τον τρόπο ερμηνείας της ημ/νιας λήξης της άδειας '
                                                'κατά την σύγκριση'),
                                            required=False)
    date_until = forms.DateField(label="Ημ/νια Λήξης", required=False, widget=DatePickerInput,
                                 help_text=_('Περιορίστε με βάση την ημ/νια λήξης της άδειας'))

    class Meta:

        widgets = {
            'leave_type': forms.SelectMultiple(attrs={'size': 14}),

        }

    def clean_effective_days(self):
        effective_days = self.cleaned_data['effective_days']

        if effective_days is not None and effective_days <= 0:
            self.add_error('effective_days', _("Η διάρκεια των ημερών άδειας πρέπει να είναι μεγαλύτερη του 0"))

        return effective_days

    def clean(self):
        """
        Validates the leave's date_from and date_until
        """
        cleaned_data = super().clean()

        date_from = cleaned_data.get("date_from")
        date_until = cleaned_data.get("date_until")

        if date_from and date_until:

            if date_from > date_until:
                self.add_error('date_from', _('Η ημ/νία έναρξης της άδειας είναι μεταγενέστερη της λήξης'))

            if date_until < date_from :
                self.add_error('date_until', _('Η ημ/νία λήξης της άδειας είναι προγενέστερη της έναρξης'))

        return cleaned_data