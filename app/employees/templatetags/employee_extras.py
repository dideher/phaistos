from django import template
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.utils import timezone

from employees.models import Employee, WorkExperience, Employment
from leaves.models import Leave
from phaistos.commons import days360

register = template.Library()


@register.filter(is_safe=True)
def duration_string_from_days(value):
    try:
        value_int: int = int(value)
    except ValueError:
        return ""

    years = int(value_int / 360)
    value_int -= (years * 360)

    months = int(value_int / 30)
    value_int -= (months * 30)

    days = value_int

    return f'{years} έτη {months} μην. {days} ημ.'


@register.inclusion_tag('employees/custom_tag_show_leaves.html', takes_context=True)
def show_leaves(context):
    employee: Employee = context.get('employee')
    if employee is not None:
        leaves_list: QuerySet[Leave] = Leave.objects.filter(employee_id=employee, is_deleted=False).order_by('-date_from')
        # paginator = Paginator(leaves_list, 10)  # Show 25 contacts per page.
        # page = request.GET.get('lpage')
        # leaves = paginator.get_page(page)
        # return {'leaves': leaves}
        return {'leaves': leaves_list}
    else:
        return {'leaves': None}


@register.inclusion_tag('employees/custom_tag_show_work_experience.html', takes_context=True)
def show_work_experience(context):
    employee: Employee = context.get('employee')
    request = context.get('request')
    if employee is not None:
        workexperiences_list: QuerySet[WorkExperience] = WorkExperience.objects.filter(employee_id=employee).order_by('-date_from')
        # paginator = Paginator(workexperiences_list, 5)  # Show 25 contacts per page.
        # page = request.GET.get('wpage')
        # workexperiences = paginator.get_page(page)
        # return {'workexperiences': workexperiences}
        return {'workexperiences': workexperiences_list}
    else:
        return {'workexperiences': None}


@register.inclusion_tag('employees/custom_tag_show_employments.html', takes_context=True)
def show_employments(context):
    employee: Employee = context.get('employee')
    request = context.get('request')
    if employee is not None:
        employments_list: QuerySet[Employment] = Employment.objects.filter(employee_id=employee).order_by('-is_active',
                                                                                                          'effective_from')
        # paginator = Paginator(workexperiences_list, 5)  # Show 25 contacts per page.
        # page = request.GET.get('wpage')
        # workexperiences = paginator.get_page(page)
        # return {'workexperiences': workexperiences}
        return {'employments': employments_list}
    else:
        return {'employments': None}


@register.inclusion_tag('employees/custom_tag_show_work_experience_totals.html', takes_context=True)
def show_work_experience_totals(context):
    employee: Employee = context.get('employee')
    request = context.get('request')
    misthologiki_proyp: int = 0
    bathmologiki_proyp: int = 0
    proy_gia_orario: int = 0

    total_days_from_diorismos: int = 0
    ekpaideutiki_yphresia_meta_diorismo: int = 0
    didaktiki_yphresia_meta_diorismo: int = 0

    result = {}

    # ta koritisia elenitsa & manola
    # mk, bathmo (athena mallon den einai ok)
    # na metaferoume hm/nia anal yphresias (to exei mallon to myschool Ημερομηνία 1ης Ανάληψης Υπηρεσίας)
    # hm/nia monimopoihseis +2 xronia (μαλλον το εχει το myschool)
    # na emfanisoume ADT ston employee (to exoume, to pairnw apo thn athina) (DONE)
    # οργανική

    # Προ-Διορισμό

    # Μισθολογικη Προϋπηρεσία.. (ν4354/2015) : 3, 5, 6, 7, 10, 11,13, 15, 16, 17, 18 (afairoume oti broume se 4, 9) (DONE)
    # Βαθμολογική Προϋπηρεσία : 3 (afairoume oti broume se 4, 9) (DONE)
    # Προϋπηρεσια για Ωράριο : 3, 6, 15, 16, 17, 18, 20 (afairoume oti broume se 4, 9, 21) (DONE)

    # eggyhsh: skouzkis & tzombanakis


    #

    #
    #
    # Μετά Διορισμό (απο ΦΕΚ διορισμού μέχρι σήμερα)
    #
    # Εκπαιδευτική Υπηρεσία - ολες οι ημερες μειων αδειων ανευ αποδοχων ετκος ανατραφοης τεκνου, κυσης, λοχιας
    # Διδακτικη - όλες οι ημέρες - 8α δουμε

    if employee is not None:

        if employee.fek_diorismou_date is not None:
            # FEK DIORISMOU is present, let's compute things
            now = timezone.now()
            now_date = now.date()
            timedelta_from_fek = now_date - employee.fek_diorismou_date

            total_days_from_diorismos = days360(employee.fek_diorismou_date, now_date, include_last_lay=True)
            ekpaideutiki_yphresia_meta_diorismo = total_days_from_diorismos
            didaktiki_yphresia_meta_diorismo = total_days_from_diorismos

        else:
            result['no_fek_diorismou'] = True

        we_list: QuerySet[WorkExperience] = WorkExperience.objects.filter(employee=employee).order_by('-date_from')

        for we in we_list:
            # for now let's just inc :
            we_code = we.work_experience_type.code

            if we_code in [4, 9]:
                misthologiki_proyp -= we.duration_total_in_days
                bathmologiki_proyp -= we.duration_total_in_days
            else:
                misthologiki_proyp += we.duration_total_in_days
                bathmologiki_proyp += we.duration_total_in_days

            if we_code in [21, ]:
                proy_gia_orario -= we.duration_total_in_days
            else:
                proy_gia_orario += we.duration_total_in_days

        computed_totals = {
            'misthologiki_proyp': misthologiki_proyp,
            'bathmologiki_proyp': bathmologiki_proyp,
            'proy_gia_orario': proy_gia_orario,
            'ekpaideutiki_yphresia_meta_diorismo': ekpaideutiki_yphresia_meta_diorismo,
            'didaktiki_yphresia_meta_diorismo': didaktiki_yphresia_meta_diorismo,
            'total_days_from_diorismos': total_days_from_diorismos,
        }

        result.update(computed_totals)

    return result
