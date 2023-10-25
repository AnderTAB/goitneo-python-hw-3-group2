from datetime import datetime

def birthday_this_year(user):
    today = datetime.today().date()
    name = user["name"]
    birthday = user["birthday"].date()
    birthday_this_year = birthday.replace(year=today.year)
    return {"name": name, "birthday": birthday_this_year}

def get_weekday(birthday):
    return datetime.strftime(birthday, '%A')

def full_list_for_the_next_7_days(users):
    full_dict = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    current_date = datetime.today().date()
    current_day = current_date.weekday()

    users = map(birthday_this_year, users)
    for user in users:
        difference = user["birthday"] - current_date
        week_day = get_weekday(user["birthday"])

        if current_day == 0 and 1 < difference.days <= 5:
            if week_day not in ('Saturday', 'Sunday'):
                full_dict[week_day].append(user["name"])
        
        if current_day > 0 and 1 < difference.days <= 7:
            if week_day in ('Saturday', 'Sunday'):
                week_day = 'Monday'
            full_dict[week_day].append(user["name"])

    return full_dict

def get_birthdays_per_week(users):
    spisok = full_list_for_the_next_7_days(users)

    for day, names in spisok.items():
        if names:
            names_str = ", ".join(names)
            print(f'{day}: {names_str}')

# Example usage:
users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Galia Kvitka", "birthday": datetime(1997, 10, 29)},
    {"name": "Alina Balaba", "birthday": datetime(2003, 10, 26)},
    {"name": "Serhii Stepanenko", "birthday": datetime(1992, 10, 26)},
    {"name": "Alex Melnykov", "birthday": datetime(1988, 10, 26)}
]

get_birthdays_per_week(users)
