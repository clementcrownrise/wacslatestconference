from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from . models import Account
from conferencename.models import Conferencename 
from faculty.models import Faculty
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date 
from confregdetails.models import Confregdetail
from django.core.exceptions import PermissionDenied

#for email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import uuid 



def register(request):
    print('this is being call')
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            #phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            #faculty = form.cleaned_data.get('faculty')
            password = form.cleaned_data['password']
            username = f"{first_name.lower()}_{uuid.uuid4().hex[:6]}"        
            #faculty_id = request.POST.get('faculty')
            #faculty = Faculty.objects.get(id=faculty_id)
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
                        )
            
            

            #user.phone_number = phone_number
            #user.faculty = faculty
            user.save()
            messages.success(request,"Your account has been created successfully, please login below")
            # mail_subject = 'Account Registration Notification'
            # link =request.build_absolute_uri(
            #     f"/abstracts/"
            # )
            # message = render_to_string('accounts/registrationEmail.html',{
            #     'user':user,
            #     'link':link
            # })
            # to_email = user.email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.content_subtype = 'html'
            # send_email.send()
            return redirect('login')

            #I will need to send account creation email here later

        else:
            #print('form is not valid')
            messages.error(request, 'Error Creating your account, Please try again')
            
    else:
        form = RegistrationForm
   
    
    context= {
        'form':form,
        'faculties':faculties
    }
    return render(request, 'accounts/register.html', context)




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                pass
                #I will check the type of user here and redirect accordingly
                #I will fetch the user's article here
                
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in ')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Username/Password')
            return redirect('login')


    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Notification'
            message = render_to_string('accounts/passwordReset.html',{
                'user':user,
                'domain':current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email box')
            return redirect('login')
        else:
            messages.error(request, 'Account with the email provided does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password'
                        )
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired')
        return redirect('login')
    


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successfully')
            return redirect('login')

        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPasswordpage.html')
    


@login_required
def dashboard(request):
    today = date.today()
    conferences  = Conferencename.objects.all()
    context = {
        'conferences' : conferences,
        'today':today
    }
    return render(request, 'accounts/dashboard.html', context)



@login_required
def myconferences(request):
    today = date.today()
    conferences = Confregdetail.objects.filter(user_id = request.user)
    context = {
        'today':today,
        'conferences':conferences
    }
    return render(request, 'accounts/myconferences.html', context)


@login_required
def myconferencedetails(request, id):
    details = get_object_or_404(Confregdetail,id=id)
    if details.user == request.user:
        print("it is the same user")

    else:
        raise PermissionDenied("You do not have permission to view this detail.")
    context = {
            'details':details
    }
    return render(request, 'confregdetails/details.html', context )