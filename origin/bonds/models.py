from django.core.validators import RegexValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


class Bond(models.Model):
    # Each of the following class variables represents a database field
    isin = models.CharField(
        max_length=12,
        blank=False,
        validators=[RegexValidator(
            regex="^[a-zA-Z0-9]{12}$",
            message="ISIN number must be 12 digits long and alphanumeric."
        )]
    )
    # From research, the overall size of the global bond market is $128.3 trillion.
    # This is approximately equal to 2^47, so I have chosen this as a maximum value.
    size = models.BigIntegerField(
        validators=[
            MaxValueValidator(
                2 ** 47,
                message="Bond size cannot be larger than the market."
            ),
        ],
        blank=False
    )
    currency = models.CharField(
        max_length=3,
        blank=False,
        validators=[RegexValidator(
            regex="^[a-zA-Z]{3}$",
            message="Please enter a three-digit currency code."
        )]
    )
    maturity = models.DateField(blank=False)  # Only the date
    lei = models.CharField(
        max_length=20,
        blank=False,
        validators=[RegexValidator(
            regex="^[a-zA-Z0-9]{20}$",
            message="LEI number must be 20 digits long and alphanumeric."
        )]
    )
    legal_name = models.CharField(max_length=100, default='', blank=True)  # The length of 100 was decided arbitrarily

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
