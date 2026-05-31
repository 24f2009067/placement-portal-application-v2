import re

# auth
def validate_email(value):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, value):
        raise ValueError("Invalid email")

    return value


def validate_password(value):

    if len(value) < 4:
        raise ValueError("Password too short")

    return value

def validate_role(value):

    if value not in ["student", "company"]:
        raise ValueError("Invalid role")

    return value