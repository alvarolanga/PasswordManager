import random
import string


def generate_password(length=12, use_digits=True, use_special=True): #Generate password function
    if length < 1:
        raise ValueError("Password length must be at least 1") #Cannot be smaller than 1

    letters = string.ascii_letters
    digits = string.digits
    specials = "!@#$%^&*()-_=+[]{};:,.<>?/"

    chars = letters #start with letters
    password_chars = []

    if use_digits:
        chars += digits #add numbers
        password_chars.append(random.choice(digits)) #generate at least a number
    if use_special:
        chars += specials #add special char
        password_chars.append(random.choice(specials)) #generate at least a special char

    # Fill the rest of the password length with random chars
    while len(password_chars) < length:
        password_chars.append(random.choice(chars))

    random.shuffle(password_chars) #always shuffle so the passwords are different
    return ''.join(password_chars)
