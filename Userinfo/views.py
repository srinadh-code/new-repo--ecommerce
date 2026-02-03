from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import ProfileSerializer,OrderSerializer
from django.contrib.auth.hashers import check_password

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # create profile only once
        if Profile.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            Profile.objects.create(
                user=request.user,
                **serializer.validated_data
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OrderlistView(APIView):
   permission_classes=[IsAuthenticated]
   def get(self,request):
       order=Order.objects.filter(user=request.user).order_by('-created_at')
       serializer=OrderSerializer(order,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
class ResetPasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        old_password=request.data.get("old_password")
        new_password=request.data.get("new_password")

        if not check_password(old_password,user.password):
            return Response(
                {
                    "error":"old password not matched"
                },status=status.HTTP_400_BAD_REQUEST
            )
        if len(new_password)<8:
            return Response({
                "error":"password must contain atleast 8 characters"
            },status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response(
            {"message":"password updated success"},status=status.HTTP_200_OK
        )
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

