from django.db import models
from django.utils.translation import gettext_lazy as _

class UserActivePackageRoleType(models.TextChoices):
    TRIAL_USER = 'N', _('Users')
    ACTIVE_USER_PACKAGE_ADMIN = 'A', _('Moderators')
    ACTIVE_USER_PACKAGE_MEMBER = 'M', _('Moderators')

class PackageType(models.TextChoices):
    DEVELOPER = 'D', _('Developer')
    TEAM = 'T', _('Team')
    BUSINESS = 'B', _('Business'),
    ENTERPRISE = 'E', _('Enterprise')

class CountryCode(models.TextChoices):
    INDIA = '+91', _('India')
    SINGAPORE = '+95', _('Singapore')
    INDONESIA = '+62', _('Indonesia')

class Language(models.TextChoices):
    ENGLISH = 'en', _('English')
    CHINESE = 'zh', _('Chinese')

class FeatureType(models.TextChoices):
    NUMBER_OF_IMAGES = 'NUMBER_OF_IMAGES', _('Number of Images')
    NUMBER_OF_WORDS = 'NUMBER_OF_WORDS', _('Number of Words')
    NUMBER_OF_USERS = 'NUMBER_OF_USERS', _('Number of Users')

class PriceUnitType(models.TextChoices):
    RUPEES = 'RS', _('RUPEES')
    US_DOLLAR = 'USD', _('US Dollar')

class FeatureMeasuringUnit(models.TextChoices):
    NUMBER_OF_UNITS = 'NUMBER_OF_UNITS', _('Number of units')

class TimeMeasureUnit(models.TextChoices):
    SECONDS = 'SEC', _('Seconds')
    MINUTES = 'MIN', _('Minutes')
    HOURS = 'HR', _('Hours')
    DAYS = 'DAY', _('Days')
    WEEKS = 'WEEK', _('Week')
    MONTHS = 'MONTH', _('Month')
    HALF_YEARLY = 'HALF_YEAR', _('Half Yearly')
    YEARLY = 'YEAR', _('Yearly')

class TeamPackageStatus(models.TextChoices):
    CREATED = ' CREATED', _("Created")
    EXPIRED = ' EXPIRED', _("Expired")
    FAILED = ' FAILED', _("Failed")
    ACTIVE = ' ACTIVE', _("Active")
    