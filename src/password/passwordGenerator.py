import random
import string
from src.have_i_been_pawnd.checkAccount import *


class PasswordGenerator:
    """
    Settable Properties:

        | min_upper_chars     |   Minimum length of the password | 6\n
        | max_len     |   Maximum length of the password | 16\n
        | minu_chars  |   Minimum upper case characters required in password | 1\n
        | minl_chars  |   Minimum lower case characters required in password | 1\n
        | minnu_mbers |   Minimum numbers required in password               | 1\n
        | min_schars  |   Minimum special characters in the password         | 1\n

    """

    def __init__(self, min_upper_chars, min_lower_chars, min_numbers, min_special_chars, start_with_password_upper,
                 password_length):

        self.min_upper_chars = min_upper_chars
        self.min_lower_chars = min_lower_chars
        self.min_numbers = min_numbers
        self.min_special_chars = min_special_chars

        self.lower_chars = string.ascii_lowercase
        self.upper_chars = string.ascii_uppercase
        self.numbers = string.digits
        self.special_chars = ['!', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '-', '_', '+', '=', '<', '>', '?']

        self.check_with_api = True
        self.start_password_with_upper = start_with_password_upper
        self.password_length = password_length

    def generate_password(self):

        # first Check if one min number is lower than zero and build Char List

        if self.password_length < 0:
            raise ValueError(
                "Minimum password length to short!\n"
                "Password length cannot be negative!\n"
                "Minimum length is 1, recommended is 16.")
        if self.password_length > 64:
            raise ValueError(
                "Password to long!\n"
                "Cannot be longer than 64.")
        if self.min_upper_chars < 0:
            raise ValueError(
                "Minimum upper case character length to short!\n"
                "Cannot be negative, minimum is 1.\n")
        if self.min_lower_chars < 0:
            raise ValueError(
                "Minimum lower case character length to short!\n"
                "Cannot be negative, minimum is 1.\n")
        if self.min_numbers < 0:
            raise ValueError(
                "Minimum number length to short!\n"
                "Cannot be negative, minimum is 1.\n")
        if self.min_special_chars < 0:
            raise ValueError(
                "Minimum special character length to short!\n"
                "Cannot be negative, minimum is 1.\n")

        # build CharList
        complete_char_list = []

        if self.min_lower_chars > 0:
            complete_char_list += list(self.lower_chars)
        if self.min_upper_chars > 0:
            complete_char_list += list(self.upper_chars)
        if self.min_numbers > 0:
            complete_char_list += list(self.numbers)
        if self.min_special_chars > 0:
            complete_char_list += list(self.special_chars)

        min_password_length = self.min_upper_chars + self.min_lower_chars + self.min_numbers + self.min_special_chars
        if min_password_length > self.password_length:
            raise ValueError("Password cannot be shorter than minimum requirements!\n"
                             "Your minimum length is %s", min_password_length)

        # build password

        # add lower case chars
        password = [random.choice(list(set(self.lower_chars))) for letter in range(self.min_lower_chars)]
        # add upper case chars
        password += [random.choice(list(set(self.upper_chars))) for letter in range(self.min_upper_chars)]
        # add numbers
        password += [random.choice(list(set(self.numbers))) for letter in range(self.min_numbers)]
        # add special chars
        password += [random.choice(list(set(self.special_chars))) for letter in range(self.min_special_chars)]

        # add other chars

        if len(password) < self.password_length:
            # add stuff to password
            password += [random.choice(complete_char_list) for letter in range(self.password_length - len(password))]
        random.shuffle(password)

        if self.start_password_with_upper:
            if password[0].isalpha():
                password[0] = password[0].upper()
            else:  # if not a letter change it to letter
                password[0] = random.choice(list(set(self.upper_chars)))

        password = "".join(password)

        # check generated password with api
        if self.check_with_api:
            if check_password(password):  # TODO Add Check for Internet Connection
                PasswordGenerator.generate_password(self)

        return password



