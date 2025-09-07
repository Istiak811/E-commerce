from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail 
from django.core.exceptions import  ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import CustomAuthenticationform,CustomPasswordResetForm,CustomSetPasswordForm,CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser,UserProfile
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required
def user_dashboard(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email= request.POST.get('email', user.email)

        user.save()

        user_profile.mobile = request.POST.get('mobile', user_profile.mobile)
        user_profile.address_1 = request.POST.get('address_1', user_profile.address_1)
        user_profile.address_2 = request.POST.get('address_2', user_profile.address_2)
        user_profile.city = request.POST.get('city', user_profile.city)
        user_profile.state = request.POST.get('state', user_profile.state)
        user_profile.country = request.POST.get('country', user_profile.country)

        user_dashboard.save()

        return redirect('user_dashboard')
    context = {
        'user_info' : user,
    }
    return render(request, 'accounts/user-dashboard.html', context)


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('Fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not full_name or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with same email already exists.")
            print("Error:A user with same email already exists.")
            return redirect('signup')
        try:
            user = CustomUser.objects.create_user(username=full_name,email=email,password=password)
            user.is_verified = False
            user.save()

            messages.success(request, "Registration is done.Please Verify the mail.")

            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}/accounts/verify/{urlsafe_base64_encode{force_bytes(user.pk)}}/{default_token_generator.make_token(user)}"
            send_verification_email(user, verification_link)
            return redirect('login')
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, "An error occured while creating account. Please Try again")
            return redirect('signup')
    return render(request, 'accounts/sign-up.html')