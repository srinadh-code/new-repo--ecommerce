

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer


#  DRF API (JSON)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def profile_page(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        # CREATE profile if not exists
        if not profile:
            profile = Profile.objects.create(
                user=request.user,
                full_name=full_name,
                phone_number=phone_number,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
            )
        else:
            #  UPDATE profile
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.address = address
            profile.city = city
            profile.state = state
            profile.pincode = pincode
            profile.save()

        return redirect("profile_page")

    return render(request, "profile.html", {"profile": profile})
@login_required
def delete_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        profile.delete()
    return redirect("profile_page")
