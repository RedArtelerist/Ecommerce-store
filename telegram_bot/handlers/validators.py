import re


def isValid(pattern, test, message):
    if re.fullmatch(pattern, test):
        return test
    else:
        raise Exception(message)


def validate_name(text: str, typ: str):
    pattern = re.compile(r'[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*')
    if len(text.strip()) < 2:
        raise Exception(f'{typ} must be at least 2 characters')
    if len(text.strip()) > 20:
        raise Exception(f'{typ} must not exceed 20 characters')
    return isValid(pattern, text, f'Invalid {typ} format')


def validate_email(text):
    pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return isValid(pattern, text, 'Invalid email format')


def validate_phone(text):
    pattern = re.compile(r'((?:\+?3)?8)?[\s\-\(]*?(0\d{2})[\s\-\)]*?(\d{3})[\s\-]*?(\d{2})[\s\-]*?(\d{2})')
    return isValid(pattern, text, 'Invalid phone format')


def validate_address(text):
    if len(text.strip()) < 5:
        raise Exception('Address must be at least 5 characters')
    return text.strip()