from django.utils import timezone


def date_range(start_date, end_date):
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):  # Include end date
        dates.append(start_date + timezone.timedelta(days=i))
    return dates
