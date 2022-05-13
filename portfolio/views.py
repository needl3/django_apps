from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import json
import logging
from . import models

logging.basicConfig(filename='contact_debug.log', encoding='utf-8', level=logging.DEBUG)

# Create your views here.
def index(request):
    context = {
        'Me':{
            'Name':models.Me.objects.all()[0].name,
            'Image':models.Me.objects.all()[0].image_link.split(',')
            },
        'Projects':[{
            'Name':i.name,
            'Tools':i.tools.split(','),
            'Description':i.description,
            'Image':i.image,
            'ProjectLink':i.link
            }for i in models.Projects.objects.all()],
        'Event':[{
            'Name':i.name,
            'Description':i.description,
            'Image':i.image_link
            } for i in models.Events.objects.all()],
        'Contact':[{'LinkSocial':'https://facebook.com/h3mlo',
                    'IconSocial':'facebook'},
                    {'LinkSocial':'https://instagram.com/anis_chapagai',
                    'IconSocial':'instagram'},
                    {'LinkSocial':'https://www.linkedin.com/in/an1sh/',
                    'IconSocial':'linkedin'},
                    {'LinkSocial':'https://snapchat.com/add/segfaulk',
                    'IconSocial':'snapchat'},
                    {'LinkSocial':'https://www.t.me/n33d13',
                    'IconSocial':'telegram'}],
        'iconGithub':'https://github.com/fluidicon.png',   
    }
    return render(request, 'portfolio/index.html', context)

def form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            name = str(data['name'])
            email = str(data['email'])
            phone = str(data['phone'])
            message = str(data['message'])

            # Send mail
            send_mail(
                'Portfolio Message',
                f'Name: {name}\n\
                Email: {email}\n\
                Phone: {phone}\n\
                Message: {message}\n',
                settings.EMAIL_HOST_USER,
                ['anishchapagai0@gmail.com'],
                fail_silently=False)
            return JsonResponse({'Status':'Success'})
        except Exception as e:
            logging.debug("SMTP send_mail"+str(e))
            return JsonResponse({'Status':'Failed'})
    return JsonResponse({'Status':'You nauty nauty ;)'})
