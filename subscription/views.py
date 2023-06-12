from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from subscription.models import TeamFeatureUsage, TeamPackage, FeatureUsageLedger
from .serializers import (UserCreateSerializer, UserUpdateSerializer, 
                          TypefaceContentCreateSerializer, UserCreateTeamPackageSerializer, 
                          MarkTeamPackageaPaymentSuccessSerializer, FeatureTypeCountSerializer)
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView



# Getting the custom user model defined
User = get_user_model()
# Create your views here.
    
class UserCreateAPIView(CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user
    
    def patch(self, request):
        return self.update(request)
    
class UserCreateTeamPackageView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserCreateTeamPackageSerializer

    def post(self, request):
        return self.create(request)
    

class PackagePaymentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = TeamPackage.objects.all()
    serializer_class = MarkTeamPackageaPaymentSuccessSerializer

    def post(self, request):
        serializer = MarkTeamPackageaPaymentSuccessSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TypefaceContentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = FeatureUsageLedger.objects.all()
    serializer_class = TypefaceContentCreateSerializer

    def post(self, request):
        serializer = TypefaceContentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FetchPackageUsageDetailsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeatureTypeCountSerializer

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        queryset = FeatureUsageLedger.objects.filter(
            created_at__range=[start_time, end_time]
        ).values('team_feature_usage__feature__type').annotate(usage=Sum('number_of_feature_units'))

        return queryset