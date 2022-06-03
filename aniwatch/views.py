from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from bs4 import BeautifulSoup

import io, csv, json, requests, os
from . import models
from .templatetags import scraper

def index(request):
    # Store dict containing trending and recommended
    if request.method == 'POST':
        return render(request, 'aniwatch/error.html', {'method':'Please don\'t POST'})
    context = {
        'Recents':[{'Title':i.name,
                    'Url':models.Video.objects.get(name=i.name).url,
                    'Image':models.Video.objects.get(name=i.name).image_link
                    } for i in models.Recents.objects.all()[:10]],
        'New':[{'Title':i.name,
                        'Url':models.Video.objects.get(name=i.name).url,
                        'Image':models.Video.objects.get(name=i.name).image_link
                        } for i in models.NewReleases.objects.all()[:10]],
        'Recommended':[{'Title':i.name,
                        'Url':models.Video.objects.get(name=i.name).url,
                        'Image':models.Video.objects.get(name=i.name).image_link
                        } for i in models.Recommended.objects.all()[:10]],
        }
    return render(request, 'aniwatch/index.html', context)

def query(request):
    if request.method == 'GET':
        return render(request, 'aniwatch/error.html', {'method':"You cant just Get, ploxx"})
    
    # pull video information from Video model
    anime = {'Query':str(request.POST['anime_name']),
            'Anime':[{'Title':i.name,
                        'Url':i.url,
                        'Image':i.image_link
                        }for i in models.Video.objects.filter(name__startswith=str(request.POST['anime_name']))[:20]
                    ]
            }
    return render(request, 'aniwatch/query.html', anime)


@xframe_options_exempt
def anime(request, anime_url, episode=False):
    # Return a page with video

    obj = models.Video.objects.get(url=anime_url)
    context = {'Anime':obj,
                # This conditional episode below will handle if the page is first clicked
                # or page with video has to be served
                'Servers': scraper.ScrapeAnime.getServers(obj.url, "1" if not episode else episode),
                'iframe':episode
    }
    return render(request, 'aniwatch/anime.html', context)

def queryEpisodesJson(request, anime_url, episode):
    # Fetch streaming url of that episode
    url = f"https://gogoanime.sk/{anime_url}-episode-{episode}"
    soup = BeautifulSoup(
            requests.get(url).text, 'html.parser')
    url = soup.find('div',class_="play-video").iframe.get("src")
    return JsonResponse(json.dumps({"Url":url}), safe=False);


class MovieUpload(View):
    def get(self, request):
        context = {
            'headings':['Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Url', 'Type', 'Released']
        }
        return render(request, 'aniwatch/upload_csv.html', context)

    def post(self, request):
        if str(request.POST['key']) != os.environ['dj_key']:
            return render(request, 'aniwatch/error.html', {'method':'User not authorized to update database'})

        file = io.TextIOWrapper(request.FILES['data'].file)
        database = csv.DictReader(file)
        database = list(database)
        #'Name', 'Image', 'Summary', 'Genre', 'Type', 'Episodes', 'Status', 'Url']
        obj = [
            models.Video(
                name = row['Name'],
                image_link = row['Image'],
                summary = row['Summary'],
                genre = row['Genre'],
                status = row['Status'],
                episodes = row['Episodes'],
                url = row['Url'],
                anime_type = row['Type'],
                released = row['Released'],
                )
            for row in database
            ]
        try:
            bulk_obj = models.Video.objects.bulk_create(obj)
            return render(request, 'aniwatch/error.html', {'method':'Data Imported Successfully'})
        except Exception as e:
            return render(request, 'aniwatch/error.html', {'method':f'Failed to import Data:    {e}'})

def popular(request):
    # Filter dubbed anime
    filtered_ongoing_anime = list()
    for i in models.Popular.objects.all():
        if not 'dub' in i.name.lower():
            filtered_ongoing_anime.append(i)

    anime = {
        'Query':'Recently Popular',
        'Anime':[{'Title':i.name,
                'Url':models.Video.objects.get(name=i.name).url,
                'Image':models.Video.objects.get(name=i.name).image_link
                }for i in filtered_ongoing_anime[:20]
            ]
    }
    return render(request, 'aniwatch/query.html', anime)

def hot(request):

    # Filter dubbed anime
    filtered_ongoing_anime = list()
    for i in models.Hot.objects.all():
        if not 'dub' in i.name.lower():
            filtered_ongoing_anime.append(i)

    anime = {
        'Query':'Hot',
        'Anime':[{'Title':i.name,
                'Url':models.Video.objects.get(name=i.name).url,
                'Image':models.Video.objects.get(name=i.name).image_link
                }for i in filtered_ongoing_anime[:20]
            ]
    }
    return render(request, 'aniwatch/query.html', anime)

def genres(request):
    return render(request, 'aniwatch/error.html', {'method':'Need some time to implement this'})
def ongoing(request):

    # Filter dubbed anime
    filtered_ongoing_anime = list()
    for i in models.Video.objects.filter(status='Ongoing'):
        if not 'dub' in i.name.lower():
            filtered_ongoing_anime.append(i)

    anime = {'Query':'Genre: Ongoing',
            'Anime':[{'Title':i.name,
                        'Url':i.url,
                        'Image':i.image_link
                        } for i in filtered_ongoing_anime[:20]
                    ]
            }
    return render(request, 'aniwatch/query.html', anime)

class UpdateConsole(View):
    def get(self, request):
        context = dict()
        return render(request, 'aniwatch/updater_console.html', context)

    def post(self, request):
        return HttpResponse('hemlo')