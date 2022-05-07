from django.shortcuts import render
from . import models

# Create your views here.
def index(request):
    context = {
        'Projects':[{
            'Name':i.name,
            'Tools':i.tools.split(','),
            'Description':i.description,
            'Image':i.image,
            'ProjectLink':i.link
            }for i in models.Projects.objects.all()],
        'iconGithub':'https://github.com/fluidicon.png'
    }
    return render(request, 'portfolio/index.html', context)