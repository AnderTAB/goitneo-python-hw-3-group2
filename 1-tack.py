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
        if not Phone.validate_phone(value):
            raise ValueError('Invalid phone number format')
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        if not Birthday.validate_birthday(value):
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

    def add_birthday(self, birthday):
        if not Birthday.validate_birthday(birthday):
            raise ValueError('Invalid birthday format')
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        return "No birthday set for this contact"

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_str}, birthday: {self.show_birthday()}"

class AddressBook:
    def __init(self):
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
        birthdays = [record for record in self.data.values() if record.birthday and next_week >= datetime.strptime(record.birthday.value, '%d.%m.%Y') >= today]
        return birthdays

# Додамо обробники команд:

class AddressBookBot:
    def __init__(self):
        self.book = AddressBook()
        self.commands = {
            "add": self.add_contact,
            "change": self.change_phone,
            "phone": self.show_phone,
            "all": self.show_all_contacts,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.show_birthdays,
            "hello": self.greet,
            "close": self.close,
            "exit": self.close
        }

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command:
                parts = command.split()
                action = parts[0]
                if action in self.commands:
                    self.commands[action](parts[1:])
                else:
                    print("Invalid command. Type 'help' to see the list of available commands.")

    def add_contact(self, args):
        if len(args) != 2:
            print("Invalid number of arguments. Use 'add [name] [phone]'")
            return
        name, phone = args
        if self.book.find(name):
            print("Contact already exists.")
        else:
            record = Record(name)
            record.add_phone(phone)
            self.book.add_record(record)
            print(f"Contact {name} added.")

    def change_phone(self, args):
        if len(args) != 2:
            print("Invalid number of arguments. Use 'change [name] [new phone]'")
            return
        name, new_phone = args
        record = self.book.find(name)
        if record:
            record.add_phone(new_phone)
            print(f"Phone number for {name} changed to {new_phone}.")
        else:
            print(f"Contact {name} not found.")

    def show_phone(self, args):
        if len(args) != 1:
            print("Invalid number of arguments. Use 'phone [name]'")
            return
        name = args[0]
        record = self.book.find(name)
        if record:
            print(f"Phone number for {name}: {', '.join(str(phone) for phone in record.phones)}")
        else:
            print(f"Contact {name} not found.")

    def show_all_contacts(self, args):
        if len(args) != 0:
            print("Invalid number of arguments. Use 'all'")
            return
        if not self.book.data:
            print("No contacts in the address book.")
        else:
            for record in self.book.data.values():
                print(record)

    def add_birthday(self, args):
        if len(args) != 2:
            print("Invalid number of arguments. Use 'add-birthday [name] [DD.MM.YYYY]'")
            return
        name, birthday = args
        record = self.book.find(name)
        if record:
            record.add_birthday(birthday)
            print(f"Birthday added for {name}.")
        else:
            print(f"Contact {name} not found.")

    def show_birthday(self, args):
        if len(args) != 1:
            print("Invalid number of arguments. Use 'show-birthday [name]'")
            return
        name = args[0]
        record = self.book.find(name)
        if record:
            print(f"Birthday for {name}: {record.show_birthday()}")
        else:
            print(f"Contact {name} not found.")

    def show_birthdays(self, args):
        if len(args) != 0:
            print("Invalid number of arguments. Use 'birthdays'")
            return
        birthdays = self.book.get_birthdays_per_week()
        if birthdays:
            print("Birthdays in the next week:")
            for record in birthdays:
                print(f"{record.name.value}: {record.birthday.value}")
        else:
            print("No birthdays in the next week.")

    def greet(self, args):
        print("Hello! I'm your Address Book Bot. You can use me to manage your contacts.")

    def close(self, args):
        print("Goodbye!")
        exit()

if __name__ == "__main__":
bot = AddressBookBot()
bot.run()