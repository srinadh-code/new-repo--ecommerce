from django.shortcuts import render
from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

# class Profile(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self, request):
#         serializer = PhoneSerializer(request.user.profile)
#         return Response(serializer.data)
#     def post(self,request):
#         form=PhoneSerializer(data=request.data)
#         if form.is_valid():
#             form.save(user=request.user)
#             return Response({"message":"profile createad"},status=status.HTTP_201_CREATED)
#         return Response({"meaasage":"invalid crediatens"},status=status.HTTP_400_BAD_REQUEST)
#     def put(self, request):
#         profile = request.user.profile
#         serializer = PhoneSerializer(
#             profile,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not created"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if Profile.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {"message": "Profile created"},
            status=status.HTTP_201_CREATED
        )
