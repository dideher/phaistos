from django import forms
from django.utils.translation import gettext_lazy as _
from employees.models import LegacyEmployeeType, EmploymentFinancialSource, SubstituteEmploymentSource, Specialization, \
    SubstituteEmploymentAnnouncement
from main.models import SchoolYear


blank_choice = [('', '---------'), ]


class EmployeeSearchForm(forms.Form):
    last_name = forms.CharField(label='Επώνυμο', max_length=100, empty_value=None, required=False)
    first_name = forms.CharField(label='Όνομα', max_length=50, required=False)
    # is_active = forms.BooleanField(label='Σε ενεργεία', required=False, initial=True)
    employee_type = forms.ChoiceField(label="Τύπος Εργαζόμενου", choices=blank_choice + LegacyEmployeeType.choices,
                                      required=False)
    registration_id = forms.CharField(label='ΑΜ', max_length=100, required=False)
    vat_number = forms.CharField(label="ΑΦΜ", max_length=10, required=False)


class SubstituteEmploymentAnnouncementSearchForm(forms.Form):
    phase = forms.ChoiceField(choices=[('', '')], required=False)
    school_year = forms.ModelChoiceField(queryset=SchoolYear.objects.all(),  empty_label='Χωρίς Φίλτρο', required=False)

    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(),  empty_label='Χωρίς Φίλτρο', required=False)
    financing = forms.ModelChoiceField(queryset=EmploymentFinancialSource.objects.all(),
                                       label=_('Χρηματοδότηση'),
                                       help_text=_("Φιλτράρισμα με βάση το πρόγραμμα χρηματοδότησης"),
                                       empty_label='Χωρίς Φίλτρο',
                                       required=False)
    employment_source = forms.ModelChoiceField(queryset=SubstituteEmploymentSource.objects.all(),  empty_label='Χωρίς Φίλτρο',
                                               required=False)
    is_pending = forms.BooleanField(label=_('Με Τοποθέτηση'),
                                    help_text=_('Φιλτράρισμα προσλήψεων με βάση την τοποθέτηση'),
                                    required=False)

    def __init__(self, *args, **kwargs):

        super(SubstituteEmploymentAnnouncementSearchForm, self).__init__(*args, **kwargs)

        ## TODO: We need to make this smarter
        phase_choices = [('', ''), ]
        self.fields['phase'].choices = SubstituteEmploymentAnnouncement.objects.all().values_list("phase", "phase").distinct()

