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
    Me = models.Me.objects.all()[0]
    context = {
        'Me':{
            'Name':Me.name,
            'Image':Me.image_link.split(','),
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
        'Contact':[{'IconSocial':i.name,
                    'LinkSocial':i.url} for i in models.Contacts.objects.all()],
        'iconGithub':'https://github.com/fluidicon.png',   
    }
    return render(request, 'portfolio/index.html', context)

def form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Send mail
            send_mail(
                'Portfolio Message',
                f'Name: {str(data["name"])}\n\
                Email: {str(data["email"])}\n\
                Phone: {str(data["phone"])}\n\
                Message: {str(data["message"])}\n\
                UserAgent: {str(request.headers["User-Agent"])}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_DEST_USER],
                fail_silently=False)
            return JsonResponse({'Status':'Success'})
        except Exception as e:
            logging.debug("SMTP send_mail"+str(e))
            return JsonResponse({'Status':'Failed'})
    return JsonResponse({'Status':'You nauty nauty ;)'})
