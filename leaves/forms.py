from django import forms
from leaves.models import LeaveType

blank_choice = [('', '---------'),]


class LeaveSearchForm(forms.Form):
    # leave_type = forms.ChoiceField(label="Τύπος Εκπαιδευτικού", choices=blank_choice + LeaveType.choices, required=False)
    pass