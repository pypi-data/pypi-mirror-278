from abc import ABC, abstractmethod


class FormatPhone(ABC):
    @abstractmethod
    def format_phone(self, phone_input: str):
        pass


class RwandaPhoneFormat(FormatPhone):
    def format_phone(self, phone_input: str):
        """
        This function formats a phone number and returns it in a 250 format (250780000000)
        :param phone_input: string representation of a phone number, e.g. 0780000000
        :return: Newly formatted phone number as a string
        """
        phone_number = phone_input.strip()

        first_three, first_two = phone_number[0:3], phone_number[0:2]
        phone_number_length = len(phone_number)
        if phone_number_length == 9 and phone_number.startswith("7"):
            phone = f"250{phone_number}"
        elif first_three == "+25":
            phone = phone_number.lstrip("+")
        elif first_two == "07":
            phone = f"25{phone_number}"
        else:
            phone = phone_number
        return phone


class UgandaPhoneFormat(FormatPhone):
    def format_phone(self, phone_input: str):
        """
        This function formats a phone number and returns it in a 256 format (256780000000)
        :param phone_input: string representation of a phone number, e.g. 0780000000
        :return: Newly formatted phone number as a string
        """
        phone_number = phone_input.strip()

        first_three, first_two = phone_number[0:3], phone_number[0:2]
        phone_number_length = len(phone_number)
        if phone_number_length == 9 and phone_number.startswith("7"):
            phone = f"256{phone_number}"
        elif first_three == "+25":
            phone = phone_number.lstrip("+")
        elif first_two == "67":
            phone = f"25{phone_number}"
        else:
            phone = phone_number
        return phone
