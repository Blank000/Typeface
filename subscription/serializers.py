from attr import has
from django import utils
from rest_framework import serializers
from django.contrib.auth import get_user_model
from subscription import enums
from .enums import TeamPackageStatus
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import time
from django.db.models import F
from .utils import generate_invoice_url, generate_content

# Getting the custom user model defined
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Add other fields as needed

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        return super().create(validated_data)
        
class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=False, write_only=True)
    old_password = serializers.CharField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'new_password', 'old_password']  # Add other fields as needed

    def update(self, instance, validated_data):
        # Handle updates separately for password
        if 'new_password' in validated_data:
            if 'old_password' not in validated_data:
                raise serializers.ValidationError({"error_message": "old password is missing"})
            if not check_password(validated_data['old_password'], instance.password):
                raise serializers.ValidationError({"error_message": "password doesn't match"})
            hashed_password = make_password(validated_data['new_password'])
            validated_data['password'] = hashed_password
        return super().update(instance, validated_data)
    
class UserCreateTeamPackageSerializer(serializers.ModelSerializer):
    package_id = serializers.IntegerField(required=True)
    start_time = serializers.IntegerField(required=False)

    class Meta:
        model = TeamPackage
        fields = ('package_id', 'start_time')  # Add other fields as needed

    def create(self, validated_data):
        package = Package.objects.get(id=validated_data.get('package_id'), is_active=True)
        current_user = self.context['request'].user
        start_time = int(time.time()) if validated_data.get('start_time') is None else validated_data.get('start_time')
        end_time = start_time + (package.validity_in_days) * 24 * 60 * 60

        # Create TeamPackage entry
        team_package = TeamPackage.objects.create(
            package_id= package.id, 
            start_time= start_time,
            end_time= end_time
        )

        # User Team Package Details
        UserTeamPackageDetails.objects.create(
            team_package_id= team_package.id,
            user_id= current_user.id,
            role_type= enums.UserActivePackageRoleType.ACTIVE_USER_PACKAGE_ADMIN
        )

        return team_package

class MarkTeamPackageaPaymentSuccessSerializer(serializers.ModelSerializer):
    team_package_id = serializers.IntegerField(required=True, write_only=True)
    is_payment_successful = serializers.BooleanField(required=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    amount_paid = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = PaymentOrder
        fields = ['team_package_id', 'is_payment_successful', 'user', 'amount_paid']  # Add other fields as needed

    def create_team_package_feature_usage(self, team_package):
        package_id = team_package.package_id
        package_features = PackageFeature.objects.filter(package_id=package_id)
        for package_feature in package_features:
            TeamFeatureUsage.objects.create(
                    team_package_id=team_package.id,
                    feature_id=package_feature.feature_id,
                    usage_limit=package_feature.usage_limit,
                    usage_quota_remaining=package_feature.usage_limit
            )

    def create(self, validated_data):
        is_payment_successful = validated_data.get('is_payment_successful')
        team_package_id = validated_data.get('team_package_id')
        current_user = self.context['request'].user

        try:
            team_package = TeamPackage.objects.get(id=team_package_id)
        except TeamPackage.DoesNotExist:
            raise serializers.ValidationError({"error_message": "Team package doesn't exist"})

        if team_package.payment_order_id is not None:
            raise serializers.ValidationError({"error_message": "Payment order already exists for team package"})

        if is_payment_successful:
            # Create PaymentOrder entry
            payment_order = PaymentOrder.objects.create(
                bill_amount=validated_data.get('amount_paid'),
                invoice_url=generate_invoice_url()
            )

            # Update Team package with payment order id
            team_package.payment_order_id = payment_order.id
            team_package.save()

            # Update UserTeamPackageDetails for the field team_package_status to ACTIVE
            user_team_package_details = UserTeamPackageDetails.objects.get(team_package_id=team_package_id)
            User.objects.filter(id=current_user.id).update(latest_team_package_details_id=user_team_package_details.id)

            # Update UserTeamPackageDetails for the field team_package_status to ACTIVE
            user_team_package_details.team_package_status=TeamPackageStatus.ACTIVE
            user_team_package_details.save()

            # Creating user usage table
            self.create_team_package_feature_usage(team_package)
        else:
            UserTeamPackageDetails.objects.filter(id=team_package_id).update(team_package_status=TeamPackageStatus.FAILED)
            raise serializers.ValidationError({"error_message": "Payment failed"})

        return {"message": "Payment successfully captured"}

    def to_representation(self, instance):
        return instance  # Return the instance as the response data
    

class TypefaceContentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureUsageLedger
        fields = []

    def check_if_user_has_active_package(self, user):
        user.user_team_package_details

    def create(self, validated_data):
        current_user = self.context['request'].user
        # Checking if has active package
        if current_user.latest_team_package_details and current_user.latest_team_package_details.team_package_status == TeamPackageStatus.ACTIVE:
            # Updating usage 

            # The below code can be modularised on the basis of feature. As of now, it's very basic
            number_of_words_used, number_of_images_used = generate_content()
            # Assuming, i have got these feature_ids from some cache
            number_of_words_feature_id = 1 # Will be caching by taking out value like Feature.objects.get(type=FeatureType.NUMBER_OF_WORDS).id
            number_of_images_feature_id = 2 # same as above
            is_word_feature_quota_updated = (TeamFeatureUsage.objects.filter(
                feature_id=number_of_words_feature_id, team_package_id=current_user.latest_team_package_details.team_package_id,usage_quota_remaining__gt= number_of_words_used).update(
                usage_quota_remaining=F('usage_quota_remaining') - number_of_words_used
            ) > 0 and number_of_words_used > 0) or number_of_words_used == 0

            if not is_word_feature_quota_updated:
                raise serializers.ValidationError({"error_message": "Word quota feature exhausted"})

            is_image_feature_quota_updated = (TeamFeatureUsage.objects.filter(
                feature_id=number_of_images_feature_id, usage_quota_remaining__gt= number_of_images_used).update(
                usage_quota_remaining=F('usage_quota_remaining') - number_of_images_used
            ) > 0 and number_of_images_used > 0) or number_of_images_used == 0

            if not is_image_feature_quota_updated:
                raise serializers.ValidationError({"error_message": "Image quota feature exhausted"})

            # Creating a ledger record
            try:
                team_feature_usage_word = TeamFeatureUsage.objects.get(feature_id=number_of_words_feature_id, team_package_id=current_user.latest_team_package_details.team_package_id)
            except TeamPackage.DoesNotExist:
                raise serializers.ValidationError({"error_message": "Team Package doesn't seem to support the feature"})
            FeatureUsageLedger.objects.create(
                number_of_feature_units=number_of_words_used,
                team_feature_usage_id=team_feature_usage_word.id,
                created_by_id=current_user.id
            )

            try:
                team_feature_usage_image = TeamFeatureUsage.objects.get(feature_id=number_of_images_feature_id, team_package_id=current_user.latest_team_package_details.team_package_id)
            except TeamPackage.DoesNotExist:
                raise serializers.ValidationError({"error_message": "Team Package doesn't seem to support the feature"})
            FeatureUsageLedger.objects.create(
                number_of_feature_units=number_of_images_used,
                team_feature_usage_id=team_feature_usage_image.id,
                created_by_id=current_user.id
            )
        else:
            raise serializers.ValidationError({"error_message": "Either the package is not active or no package exist for the user"})

        return {"message": "Feature usage successfully captured"}

    def to_representation(self, instance):
        return instance  # Return the instance as the response data
    

class FeatureTypeCountSerializer(serializers.Serializer):
    feature_type = serializers.CharField(source='team_feature_usage__feature__type')
    usage = serializers.IntegerField()
