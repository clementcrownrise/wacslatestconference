from django.shortcuts import render
from faculty.models import Faculty
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib  import messages
from conferencename.models import Conferencename
from django.shortcuts import get_object_or_404
from .forms import ConfregdetailForm
from .models import Confregdetail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def registration(request, id):
    faculties = Faculty.objects.all()
    conference = get_object_or_404(Conferencename, id=id)
    if request.method == "POST":
        
        form = ConfregdetailForm(request.POST)
        if form.is_valid():
            
            registration = form.save(commit=False)
            registration.user = request.user
            registration.conferencename = conference
            #i need to check of this user has not registered for this conference before
            alreadyRegistered = Confregdetail.objects.filter(user = request.user, 
                                                             conferencename = conference )
            if  alreadyRegistered:
                messages.error(request,
                                  "You already registered for this conference, you can NOT register for a conference twice!")
                
            else:

                registration.save()
                #i will send a mail here
                message = render_to_string('emails/conference_registration.html',
                                           {
                                               'user':request.user,
                                               'conference':conference, 
                                           })
                email =EmailMessage(
                    'WACS Conference Registration Notification',
                    message,
                    to=[request.user.email]
                )

                email.content_subtype = 'html'
                email.send()

                messages.success(
                    request, 
                    "Your conference registration was saved, please check your mail for more details!"
                )
            return redirect('dashboard')
        
        else:
            print(form.errors)


    else:
        form = ConfregdetailForm()

    context = {
        'form':form,
        'faculties':faculties,
        'conference':conference,
    }
    return render(request, 'confregdetails/register.html', context)


