from django.core.exceptions import ValidationError
import re


def username_validation(username):
    """
    اعتبارسنجی نام کاربری.
    نام کاربری باید تنها شامل حروف، اعداد، نقطه و آندرلاین باشد و طول آن بین 0 تا 60 کاراکتر باشد.
    """
    pattern = r'^[a-zA-Z0-9._]{0,60}$'
    if re.match(pattern, username):return True
    else: raise ValidationError('نام کاربری درست نمی‌باشد')


def phone_validataion(phone):
    """
    اعتبارسنجی شماره همراه.
    """
    pattern = r'^09\d{9}$'
    if re.match(pattern, phone):return True
    else: raise ValidationError('شماره همراه درست نمی‌باشد')


def send_verify_phone(phone, code):
    #TODO: send verify code to user phone number
    pass