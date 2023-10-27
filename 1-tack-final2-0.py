from collections import defaultdict
from datetime import datetime, timedelta  # 
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

    def validate_birthday(self, value):
        try:
            day, month, year = map(int, value.split('.'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                return False
        except ValueError:
            return False
        return True

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        # Assuming the phone number should have exactly 10 digits
        return len(value) == 10 and value.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "No birthday set."

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phone_str}, birthday: {self.show_birthday()}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self, current_date):
        upcoming_birthdays = []
        for record in self.data.values():
            birthday = record.birthday
            if birthday:
                # Extract day and month from the birthday
                day, month, _ = map(int, birthday.value.split('.'))
                if month == current_date.month:
                    days_until_birthday = day - current_date.day
                    if 0 <= days_until_birthday <= 7:
                        upcoming_birthdays.append((record.name.value, days_until_birthday))
        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name."
        except IndexError:
            return "Invalid input. Please try again."
        except SyntaxError:
            return "Invalid input. Please try again."

    return inner

@input_error
def add_contact(args, address_book):
    if len(args) < 2:
        return "Invalid command. Usage: add [name] [phone] [birthday (optional)]"
    name, phone = args[0], args[1]
    record = Record(name)
    record.add_phone(phone)
    if len(args) == 3:
        record.add_birthday(args[2])
    address_book.add_record(record)
    return "Contact added."

@input_error
def change_phone(args, address_book):
    if len(args) != 2:
        return "Invalid command. Usage: change [name] [new phone]"
    name, new_phone = args
    record = address_book.find(name)
    if record:
        record.add_phone(new_phone)
        return "Phone number changed."
    return "Contact not found."
    
    
@input_error    
def show_phone(args, address_book):    
    if len(args) != 1:
        return "Invalid command. Usage: phone [name]"

    name = args[0]
    record = address_book.find(name)
    if record:
        phone_numbers = record.phones
        if phone_numbers:
            return f"Phone numbers {name}: {', '.join(str(phone) for phone in phone_numbers)}"
        else:
            return f"No phone numbers found for {name}."
    return "Contact not found."    

@input_error
def add_birthday(args, address_book):
    if len(args) != 2:
        return "Invalid command. Usage: add-birthday [name] [birthday]"
    name, birthday = args
    record = address_book.find(name)
    if record:

        if len(birthday.split('.')) == 2:
            birthday += f".{datetime.now().year}"
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, address_book):
    if len(args) != 1:
        return "Invalid command. Usage: show-birthday [name]"
    name = args[0]
    record = address_book.find(name)
    if record:
        return record.show_birthday()
    return "Contact not found."

@input_error
def birthdays(args, address_book):
    current_date = datetime.now()
    end_of_week = current_date + timedelta(days=7)

    upcoming_birthdays = []
    for record in address_book.data.values():
        birthday = record.birthday
        if birthday:
            # Враховуємо рік у даті народження
            birthdate = datetime.strptime(birthday.value, "%d.%m.%Y")
            birthdate = birthdate.replace(year=current_date.year)
            if current_date <= birthdate <= end_of_week:
                days_until_birthday = (birthdate - current_date).days
                upcoming_birthdays.append((record.name.value, days_until_birthday, birthdate.strftime('%A')))

    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."

    upcoming_birthdays.sort(key=lambda x: (x[1], x[2]))  # Сортування за днями і днями тижня
    result = "Upcoming birthdays in the next week:\n"
    for name, days_until_birthday, day_of_week in upcoming_birthdays:
        # result += f"{day_of_week}: {name} - {days_until_birthday} days\n"
        result += f"{day_of_week}: {name}\n"
    return result
    
@input_error
def show_all(address_book):
    if not address_book:
        return "Address book is empty."
    return "\n".join([str(record) for record in address_book.values()])

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_phone(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book.data))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(args, address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
