from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from bs4 import BeautifulSoup

import io, csv, json, requests, os
from . import models

def index(request):
    # Store dict containing trending and recommended
    if request.method == 'POST':
        return render(request, 'aniwatch/error.html', {'method':'Please don\'t POST'})
    context = {
        'Recents':[{'Title':models.Video.objects.get(name=i.name).name,
                        'Url':models.Video.objects.get(name=i.name).name,
                        'Image':models.Video.objects.get(name=i.name).image_link
                        } for i in models.Recents.objects.all()],
        'Trending':[{'Title':models.Video.objects.get(name=i.name).name,
                        'Url':models.Video.objects.get(name=i.name).name,
                        'Image':models.Video.objects.get(name=i.name).image_link
                        } for i in models.Trending.objects.all()],
        'Recommended':[{'Title':models.Video.objects.get(name=i.name).name,
                        'Url':models.Video.objects.get(name=i.name).name,
                        'Image':models.Video.objects.get(name=i.name).image_link
                        } for i in models.Recommended.objects.all()],
        }
    return render(request, 'aniwatch/index.html', context)

def query(request):
    if request.method == 'GET':
        return render(request, 'aniwatch/error.html', {'method':"You cant just Get, ploxx"})
    
    # pull video information from Video model
    anime = {'Query':str(request.POST['anime_name']),
            'Anime':[{'Title':i.name,
                        'Url':i.name,
                        'Image':i.image_link
                        }for i in models.Video.objects.filter(name__startswith=str(request.POST['anime_name']))[:20]
                    ]
            }
    return render(request, 'aniwatch/query.html', anime)


@xframe_options_exempt
def anime(request, anime_name, episode=False):
    # Return a page with video
    obj = models.Video.objects.get(name=anime_name)
    context = {'Anime':obj,
                'Servers': getServers(obj.url.split('/category/')[1], "1" if not episode else episode),
                'iframe':episode
    }
    return render(request, 'aniwatch/anime.html', context)

def animePlayer(request, anime_name, episode):
    return anime(request, anime_name, episode)

def queryEpisodesJson(request, anime_name, episode):
    # Fetch streaming url of that episode
    url = f"https://gogoanime.sk/{anime_name}-episode-{episode}"
    soup = BeautifulSoup(
            requests.get(url).text, 'html.parser')
    url = soup.find('div',class_="play-video").iframe.get("src")
    return JsonResponse(json.dumps({"Url":url}), safe=False);

def getServers(anime_name, episode="1"):
    url = f'https://gogoanime.sk/{anime_name}-episode-{episode}'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    li_servers = soup.find('div', class_='anime_muti_link').find_all('li')
    li_names = [i.a.text.strip().split('Choose')[0] for i in li_servers]
    a_href = [i.a['data-video'].strip('//') for i in li_servers]
    final = list()
    for j in range(len(li_names)):
        final.append({'Name':li_names[j], 'Url':a_href[j]})
    return final

class MovieUpload(View):
    def get(self, request):
        return render(request, 'aniwatch/upload_csv.html')

    def post(self, request):
        if str(request.POST['key']) != os.environ['dj_key']:
            return render(request, 'aniwatch/error.html', {'method':'User not authorized to update database'})

        file = io.TextIOWrapper(request.FILES['data'].file)
        database = csv.DictReader(file)
        database = list(database)
        #'Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Status', 'Url']
        obj = [
            models.Video(
                name = row['Name'],
                image_link = row['Image'],
                summary = row['Summary'],
                genre = row['Genre'],
                status = row['Status'],
                episodes = row['Episodes'],
                url = row['Url']
                )
            for row in database
            ]
        try:
            bulk_obj = models.Video.objects.bulk_create(obj)
            return render(request, 'aniwatch/error.html', {'method':'Data Imported Successfylly'})
        except Exception as e:
            return render(request, 'aniwatch/error.html', {'method':f'Failed to import Data:    {e}'})

class RecentsUpload(View):
    def get(self, request):
        return render(request, 'aniwatch/upload_trending_csv.html')

    def post(self, request):
        if str(request.POST['key']) != os.environ['dj_key']:
            return HttpResponse("<h1>User not authorized to update database</h1>")

        file = io.TextIOWrapper(request.FILES['data'].file)
        database = csv.DictReader(file)
        database = list(database)
        #'Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Status']
        obj = [
            models.Video(
                name = row['Name'],
                image_link = row['Image'],
                summary = row['Summary'],
                genre = row['Genre'],
                status = row['Status'],
                episodes = row['Episodes'],
                url = row['Url']
                )
            for row in database
            ]
        try:
            bulk_obj = models.Video.objects.bulk_create(obj)
            return render(request, 'aniwatch/error.html', 'Data imported Successfully.')
        except Exception as e:
            return render(request, 'aniwatch/error.html', 'Failed to import bulk data\nError: {e}')