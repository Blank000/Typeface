from django.db import models
from .enums import FeatureMeasuringUnit, TeamPackageStatus, UserActivePackageRoleType, PackageType, CountryCode, Language, FeatureType, PriceUnitType, TimeMeasureUnit
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5, choices=CountryCode.choices, default=CountryCode.INDIA)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.ENGLISH)

class Package(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=PackageType.choices, default=PackageType.DEVELOPER)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField()
    price_unit = models.CharField(max_length=5, choices=PriceUnitType.choices, default=PriceUnitType.RUPEES)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    validity_in_days = models.IntegerField()

class Feature(models.Model):
    type = models.CharField(max_length=30, choices=FeatureType.choices, unique=True)
    per_unit_cost = models.IntegerField()
    cost_measuring_unit = models.CharField(max_length=5, choices=PriceUnitType.choices, default=PriceUnitType.RUPEES)

class PackageFeature(models.Model):
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    usage_limit = models.BigIntegerField()
    feature_measuring_unit = models.CharField(max_length=25, choices=FeatureMeasuringUnit.choices, default=FeatureMeasuringUnit.NUMBER_OF_UNITS)

class PaymentOrder(models.Model):
    bill_amount = models.IntegerField()
    invoice_url = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

class TeamPackage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    payment_order = models.ForeignKey(PaymentOrder, on_delete=models.SET_NULL, null=True)

class TeamPackageAddonOrder(models.Model):
    team_package = models.ForeignKey(TeamPackage, on_delete=models.CASCADE, null=False)
    payment_order = models.ForeignKey(PaymentOrder, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

class TeamPackageAddon(models.Model):
    team_package = models.ForeignKey(TeamPackage, on_delete=models.CASCADE, null=False)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=TeamPackageStatus.choices, default=TeamPackageStatus.CREATED)
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    team_package_addon_order = models.ForeignKey(TeamPackageAddonOrder, on_delete=models.SET_NULL, null=True)


class UserTeamPackageDetails(models.Model):
    user = models.ForeignKey('TypefaceUser', on_delete=models.SET_NULL, null=True)
    team_package = models.ForeignKey(TeamPackage, on_delete=models.CASCADE, null=False)
    team_package_status = models.CharField(max_length=10, choices=TeamPackageStatus.choices, default=TeamPackageStatus.CREATED)
    role_type = models.CharField(max_length=1, choices=UserActivePackageRoleType.choices, default=UserActivePackageRoleType.TRIAL_USER)
    class Meta:
        constraints = [
            models.UniqueConstraint( 
                # cannot have two active entries
                fields=['user_id', 'team_package_status'], 
                condition=Q(team_package_status=TeamPackageStatus.ACTIVE),
                name='unique_active_package_with_user'
            ),
            models.UniqueConstraint( 
                # cannot have two team package entried
                fields=['team_package_id'],
                name='unique_team_package_id'
            ),
        ]

class TypefaceUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True, blank=False, null=False)
    latest_team_package_details = models.ForeignKey(UserTeamPackageDetails, on_delete=models.SET_NULL, null=True)

class TeamFeatureUsage(models.Model):
    team_package = models.ForeignKey(TeamPackage, on_delete=models.SET_NULL, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    usage_limit = models.IntegerField()
    usage_quota_remaining = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint( 
                # cannot have two active entries
                fields=['feature_id', 'team_package_id'],
                name='unique_team_package_feature'
            )
        ]

class FeatureUsageLedger(models.Model):
    team_feature_usage = models.ForeignKey(TeamFeatureUsage, on_delete=models.SET_NULL, null=True)
    number_of_feature_units = models.IntegerField(default=0)
    created_by = models.ForeignKey(TypefaceUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)