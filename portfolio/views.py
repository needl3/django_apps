from django.shortcuts import render
from . import models

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
        'iconGithub':'https://github.com/fluidicon.png'
    }
    print(context)
    return render(request, 'portfolio/index.html', context)