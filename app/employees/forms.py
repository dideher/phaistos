from django import forms
from employees.models import EmployeeType

blank_choice = [('', '---------'), ]


class EmployeeSearchForm(forms.Form):
    last_name = forms.CharField(label='Επώνυμο', max_length=100, empty_value=None, required=False)
    first_name = forms.CharField(label='Όνομα', max_length=50, required=False)
    # is_active = forms.BooleanField(label='Σε ενεργεία', required=False, initial=True)
    employee_type = forms.ChoiceField(label="Τύπος Εκπαιδευτικού", choices=blank_choice + EmployeeType.choices,
                                      required=False)
    registration_id = forms.CharField(label='ΑΜ', max_length=100, required=False)
    vat_number = forms.CharField(label="ΑΦΜ", max_length=10, required=False)
