import random
import string


def generate_password(length=12, use_digits=True, use_special=True):
    if length < 1:
        raise ValueError("Password length must be at least 1")

    letters = string.ascii_letters
    digits = string.digits
    specials = "!@#$%^&*()-_=+[]{};:,.<>?/"

    chars = letters
    password_chars = []

    if use_digits:
        chars += digits
        password_chars.append(random.choice(digits))
    if use_special:
        chars += specials
        password_chars.append(random.choice(specials))

    # Fill the rest of the password length with random chars
    while len(password_chars) < length:
        password_chars.append(random.choice(chars))

    random.shuffle(password_chars)
    return ''.join(password_chars)
