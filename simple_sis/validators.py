from django.core.exceptions import ValidationError


def validate_postcode(value):
    # Try to parse string into integer
    try:
        int_value = int(value)
    except ValueError:
        raise ValidationError('Postcode must be a number')

    # Check against post code ranges for all Australian states
    if int_value >= 2000 and int_value <= 2599 or \
            int_value >= 2619 and int_value <= 2899 or \
            int_value >= 2921 and int_value <= 2999 or \
            int_value >= 2600 and int_value <= 2618 or \
            int_value >= 2900 and int_value <= 2920 or \
            int_value >= 3000 and int_value <= 3999 or \
            int_value >= 4000 and int_value <= 4999 or \
            int_value >= 5000 and int_value <= 5799 or \
            int_value >= 6000 and int_value <= 6797 or \
            int_value >= 7000 and int_value <= 7799 or \
            int_value >= 800 and int_value <= 899:
        return

    raise ValidationError('Invalid postcode')