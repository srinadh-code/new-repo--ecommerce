from django.shortcuts import render
from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
