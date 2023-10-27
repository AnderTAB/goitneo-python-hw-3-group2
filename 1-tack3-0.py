from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError('Invalid phone number format')
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError('Invalid birthday format')
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not Phone.validate_phone(phone):
            raise ValueError('Invalid phone number format')
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [i for i in self.phones if i.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not Phone.validate_phone(new_phone):
            raise ValueError('Invalid phone number format')
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def add_birthday(self, birthday):
        if not Birthday.validate_birthday(birthday):
            raise ValueError('Invalid birthday format')
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "No birthday set."

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_str}, birthday: {self.show_birthday()}"

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

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                bday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                if today < bday_date < next_week:
                    upcoming_birthdays.append(f"{record.name.value}'s birthday on {bday_date.strftime('%d.%m.%Y')}")
        return upcoming_birthdays