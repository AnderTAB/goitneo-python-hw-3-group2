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
            raise ValueError(f'Invalid phone number format')
        super().__init__(value)
        
    def validate_phone(self, value):
        return len(value) == 10 and value.isdigit()
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []        
        
    def add_phone(self, phone):
        if not Phone.validate_phone(value):
            raise ValueError(f'Invalid phone number format')
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        self.phones = [i for i in self.phones if i.value != phone]
        
    def edit_phone(self, old_phone, new_phone):
        if not Phone().validate_phone(new_phone):
            raise ValueError("Invalid phone number format")
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_str}"
    
class AddressBook:
    def __init__(self):
        self.data = {}
        
    def add_record(self, record):
        self.data[record.name,value] = record
        
    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]