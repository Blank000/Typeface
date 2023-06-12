from django.core.management.base import BaseCommand
from subscription.models import *
from subscription.enums import *

class Command(BaseCommand):
    help = 'Populate data in MyModel table'

    def handle(self, *args, **options):
        # Features
        image_feature_type = Feature.objects.create(type=FeatureType.NUMBER_OF_IMAGES, per_unit_cost=10, cost_measuring_unit=PriceUnitType.RUPEES)
        word_feature_type = Feature.objects.create(type=FeatureType.NUMBER_OF_WORDS, per_unit_cost=5, cost_measuring_unit=PriceUnitType.RUPEES)
        user_feature_type = Feature.objects.create(type=FeatureType.NUMBER_OF_USERS, per_unit_cost=20, cost_measuring_unit=PriceUnitType.RUPEES)
        
        # Country
        india =  Country.objects.create(name="india", country_code=CountryCode.INDIA, language=Language.ENGLISH)
        
        # Packages
        developer_package = Package.objects.create(name="Developer", type=PackageType.DEVELOPER, price=10000, price_unit=PriceUnitType.RUPEES, country_id = india.id, is_active=True, validity_in_days=30)
        team_package = Package.objects.create(name="Team", type=PackageType.TEAM, price=50000, price_unit=PriceUnitType.RUPEES, country_id = india.id, is_active=True, validity_in_days=30)
        business_package = Package.objects.create(name="Business", type=PackageType.BUSINESS, price=200000, price_unit=PriceUnitType.RUPEES, country_id = india.id, is_active=True, validity_in_days=30)
        
        # PackageFeature
        developer_package_image_feature = PackageFeature.objects.create(package_id=developer_package.id, feature_id=image_feature_type.id, usage_limit=1000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        team_package_image_feature = PackageFeature.objects.create(package_id=team_package.id, feature_id=image_feature_type.id, usage_limit=5000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        business_package_image_feature = PackageFeature.objects.create(package_id=business_package.id, feature_id=image_feature_type.id, usage_limit=20000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)

        developer_package_word_feature = PackageFeature.objects.create(package_id=developer_package.id, feature_id=word_feature_type.id, usage_limit=5000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        team_package_word_feature = PackageFeature.objects.create(package_id=team_package.id, feature_id=word_feature_type.id, usage_limit=20000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        business_package_word_feature = PackageFeature.objects.create(package_id=business_package.id, feature_id=word_feature_type.id, usage_limit=100000, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)

        developer_package_user_feature = PackageFeature.objects.create(package_id=developer_package.id, feature_id=user_feature_type.id, usage_limit=1, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        team_package_user_feature = PackageFeature.objects.create(package_id=team_package.id, feature_id=user_feature_type.id, usage_limit=10, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        business_package_user_feature = PackageFeature.objects.create(package_id=business_package.id, feature_id=user_feature_type.id, usage_limit=100, feature_measuring_unit=FeatureMeasuringUnit.NUMBER_OF_UNITS)
        

        self.stdout.write(self.style.SUCCESS('Data populated successfully'))