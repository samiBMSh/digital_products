from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidators(RegexValidator):
    regex = '^98(9[0-3]\d{8}|[1-9]\d{9})$'
    message = _('phone number must be a valid 12 digits like 989001234321')
    code = 'invalid_phone_number'


class SKUValidator(RegexValidator):
    regex = '^[a-zA-Z0-9\-\ ]{6,20}$'
    message = _('SKU must be alphanumeric with 6 to 20 characters')
    code = 'invalid_phone_number'


class UsernameValidators(RegexValidator):
    regex = '^[a-zA-Z][a-zA-Z0-9 \.]+$'
    message = _('Enter a valid username starting with a-z'
                'This value may contain only letters, numbers, and underscore characters.')
    code = 'invalid_username'


class PostalCodeValidator(RegexValidator):
    regex = '^[0-9]{10}$'
    message = _('Enter a valid postal code')
    code = 'invalid_postal_code'


class BankCardNumberValidator(RegexValidator):
    regex = '^[0-9]{16}$'
    message = _('Enter a valid card number')
    code = 'invalid_bank_card_number'


validate_phone_number = PhoneNumberValidators()
validate_sku = SKUValidator()
validate_username = UsernameValidators()
validate_postal_code = PostalCodeValidator()
validate_bank_card_number = BankCardNumberValidator()
