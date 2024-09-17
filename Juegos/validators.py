from django.core.exceptions import ValidationError
import re

class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.findall('[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>).",
                code='password_no_special_char'
            )

    def get_help_text(self):
        return "Tu contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>)."
