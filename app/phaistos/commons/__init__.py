import calendar

def days360(start_date, end_date, include_last_lay=False):
    """
    Taken from https://github.com/dideher/certificate_of_employment/blob/master/certificate_of_employment/state_funded_associate_professors/days360.py#L6
    :param start_date:
    :param end_date:
    :param include_last_lay: If set to true, then the result will be increased by just one day
    :return:
    """
    # method_eu = False

    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year

    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year

    start_day_is_last_of_February = (start_month == 2 and start_day == 29) or (
                start_month == 2 and start_day == 28 and calendar.isleap(start_year) is False)
    # end_day_is_last_of_February = end_day == 31 or (end_month == 2 and end_day == 29) or
    # (end_month == 2 and end_day == 28 and calendar.isleap(start_year) is False)

    # months_with_31_days = {1, 3, 5, 7, 8, 10, 12}
    # months_with_30_days = {4, 6, 9, 11}
    # end_day_is_last_of_month = (end_day == 31 and end_month in months_with_31_days) or
    # (end_day == 30 and end_month in months_with_30_days)
    # start_day_is_last_of_month = (start_day == 31 and start_month in months_with_31_days) or
    # (start_day == 30 and start_month in months_with_30_days)

    if start_day == 31 or start_day_is_last_of_February:
        start_day = 30

    if start_day == 30 and end_day == 31:
        end_day = 30

    # if end_day_is_last_of_month or end_day_is_last_of_February:
    #   if start_day_is_last_of_month or start_day_is_last_of_February:
    #     end_day = 1
    #     if end_month == 12:
    #       end_year += 1
    #       end_month = 1
    #     else:
    #       end_month += 1
    #   else:
    #     end_day = 30

    result = (end_year - start_year) * 360 + (end_month - start_month) * 30 + end_day - start_day

    return result + 1 if include_last_lay else result