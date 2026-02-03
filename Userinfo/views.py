from django.shortcuts import render
from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

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



@login_required
def profile_page(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")

        #  if profile already exists → update
        if profile:
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.save()
        else:
            #  create new profile
            Profile.objects.create(
                user=request.user,
                full_name=full_name,
                phone_number=phone_number
            )

        return redirect("profile_page")

    return render(request, "profile.html", {"profile": profile})
