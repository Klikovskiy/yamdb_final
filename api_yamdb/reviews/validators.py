import datetime as dt


def year_valid(year):
    current_date = dt.date.today()
    if year > current_date.year:
        raise ValueError(f'Некорректно указан год {year}')
