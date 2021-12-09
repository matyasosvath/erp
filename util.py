import random
import string

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits


# def generate_id(number_of_small_letters=4,
#                 number_of_capital_letters=2,
#                 number_of_digits=2,
#                 number_of_special_chars=2,
#                 allowed_special_chars=r"_+-!"):


def generate_id(number_of_small_letters=2,
                number_of_capital_letters=0,
                number_of_digits=0,
                number_of_special_chars=0,
                allowed_special_chars=r"_+-!"):

    small_letters = [random.choice(lowercase) for _ in range(number_of_small_letters)]
    upper_letters = [random.choice(uppercase) for _ in range(number_of_capital_letters)]
    numbers = [random.choice(digits) for _ in range(number_of_digits)]
    chars = [random.choice(allowed_special_chars) for _ in range(number_of_special_chars)]
    id = small_letters + upper_letters + numbers + chars
    random.shuffle(id) # return None
    return "".join(id)

if __name__ == '__main__':
    print(generate_id())
