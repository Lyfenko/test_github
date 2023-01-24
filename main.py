from collections import UserDict
from datetime import datetime
from datetime import date
import os
import pickle


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.isalpha():
            self.__value = value
        else:
            raise ValueError

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.replace("+", "").replace("(", "").replace(")", "").isdigit():
            self.__value = value
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self.__value = value
        except:
            self.__value = value


class Record:
    def __init__(self, name: Name, phone: list = None, birthday: Birthday = None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            by_bd = self.birthday.value.split('.')
            needed_data = datetime(year=int(today.year), month=int(by_bd[1]), day=int(by_bd[0]))
            needed_data = needed_data.date()
            difference = needed_data - today
            result = difference.days
            return f'Days left until birthday = {result}'
        else:
            return "No Birthday found"


    def add_phone(self, phone: Phone):
        self.phone.append(phone)

    def del_phone(self, phone: Phone):
        for p in self.phone:
            if phone.value == p.value:
                self.phone.remove(p)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def __repr__(self):
        return f"name: {self.name.value}, phone: {[i.value for i in self.phone]}, birthday: {self.birthday.value}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.n = None

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n=2, days=0):
        self.n = n
        index = 1
        print_block = '-' * 50 + '\n'
        for record in self.data.values():
            if days == 0 or (record.birthday.value is not None and record.days_to_birthday(record.birthday) <= days):
                print_block += str(record) + '\n'
                if index < n:
                    index += 1
                else:
                    yield print_block
                    index, print_block = 1, '-' * 50 + '\n'
        yield print_block

    def show_all_records(contacts, *args):
        if not contacts:
            return 'Phone book is empty'
        result = 'List of all users:\n'
        print_list = contacts.iterator()
        for item in print_list:
            result += f'{item}'
        return result

    def show_phone_numbers(self, name: Name):
        return [i.value for i in self.data[name].phone]


def input_error(func):

    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Please, enter the name and number"
        except ValueError:
            return "Enter a valid number"
        except KeyError:
            return "No such name in phonebook"

    return wrapper


def hello(*args):
    return "How can I help you?"


def add_users(*args):
    try:
        name = Name(args[0])
    except ValueError:
        return "Please enter a name"
    phone_list = []
    for i in args:
        try:
            phone_list.append(Phone(i))
        except ValueError:
            continue
    try:
        bday = Birthday(args[-1])
    except ValueError:
        bday = Birthday(None)

    rec = Record(name, phone_list, bday)
    if rec.name.value not in Phonebook:
        Phonebook.add_record(rec)
    else:
        return f"The name {name.value} already exists. Please use the 'change {name.value}' command"
    return f"Contact {name.value} added successfully"

@input_error
def add_number(*args):
    Phonebook[args[0]].add_phone(Phone(args[1]))
    return f"Phone number {args[1]} is successfully added for user {args[0]}"


@input_error
def del_number(*args):
    Phonebook[args[0]].del_phone(Phone(args[1]))
    return f"Phone number {args[1]} is successfully deleted"

@input_error
def change_phone(*args):
    Phonebook[args[0]].change_phone(Phone(args[1]), Phone(args[2]))
    return f"Phone number for {args[0]} is successfully changed from {args[1]} to {args[2]}"


@input_error
def phone(*args):
    return Phonebook.show_phone_numbers(args[0])

@input_error
def days_to_b_day(*args):
    return Phonebook[args[0]].days_to_birthday()


def show_all(*args):
    return Phonebook.show_all_records(args[0])


def view(*args):
    lst = ["{:^10}: {:>10}".format(k, str(v)) for k, v in Phonebook.items()]
    return "\n".join(lst)


def end_work(*args):
    return "Good bye"

def find_text(*args):
    text = args[0][0]
    flag = 0
    result = ''
    for record in Phonebook.values():
        rec_text = str(record)
        if rec_text.find(text) != -1:
            result += str(record) + '\n'
            flag += 1
    if flag == 0:
        result = f'There are no "{text}" symbols in the Phonebook'
    return result


COMMANDS = {hello: ["hello", "hi"],
            change_phone: ["change"],
            phone: ["phone"],
            end_work: ["exit", "close", "good bye", ".", "bye"],
            add_users: ["add user"],
            add_number: ["add number"],
            show_all: ["show all", "show"],
            del_number: ["delete"],
            days_to_b_day: ["tell days to birthday"],
            view: ["all users"],
            find_text: ["find"]
            }

def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, tuple(user_input[len(i):].strip().split(" "))


def main():
    while True:
        user_input = input(">>> ")
        try:
            result, data = parse_command(user_input)
            print(result(*data))
            if result is end_work:
                break
        except TypeError:
            print("No such command")

if __name__ == "__main__":

    Phonebook = AddressBook()

    if os.path.isfile('Phonebook.bin'):
        with open('Phonebook.bin', 'rb') as file:
            Phonebook = pickle.load(file)

    main()

    with open('Phonebook.bin', 'wb') as file:
        pickle.dump(Phonebook, file)