from django.core.validators import RegexValidator

uzbek_phone_regex = RegexValidator(
    regex=r'^(\+998|998|8)?(9[012345789]|3[3])[0-9]{7}$',
    message="Telefon raqami quyidagi formatda bo'lishi kerak: +998xxxxxxxxx yoki 998xxxxxxxxx yoki 8xxxxxxxxx"
)