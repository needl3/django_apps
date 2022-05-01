import csv
import requests
from bs4 import BeautifulSoup

def main():
    urlDict = dict()
    with open('AnimeList.csv','r') as urlFile:
        readerUrl = csv.DictReader(urlFile, fieldnames=['title', 'url'])
        for row in readerUrl:
            urlDict[row['title']] = row['url']
    with open('FinalDetails.csv','w') as finalFile:
        finalWriter = csv.DictWriter(finalFile, fieldnames=['Name','Image','Summary','Genre','Episodes','Status','Url'])
        finalWriter.writeheader()
        with open('AnimeDetails.csv','r') as detailFile:
            readerPartial = csv.DictReader(detailFile)
            for row in readerPartial:
                finalWriter.writerow({'Name':row['Name'],'Image':row['Image'],'Summary': row['Summary'],'Genre':row['Genre'],'Episodes': row['Episodes'],'Status': row['Status'],'Url':urlDict[row['Name']]})

def getServer(anime_name, ep="1"):
    url = 'https://gogoanime.sk/{}-episode-{}}'.format(anime_name.lower().replace(' ','-'), ep)
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    li_servers = soup.find('div', class_='anime_muti_link').find_all('li')
    li_names = [i.a.text.strip().split('Choose')[0] for i in li_servers]
    a_href = [i.a['data-video'].strip('//') for i in li_servers]
    final = list()
    for j in range(len(li_names)):
        final.append({'Name':li_names[j], 'Url':a_href[j]})
    return a_href

def getVideo(anime_name, episode):
    url = f"//goload.pro/streaming.php?id={getId(anime_name)}==&title={anime_name}"

def getId(anime_name):
    anime_url = anime_name.lower().replace(' ','-')
    html = requests.get(f'https://gogoanime.sk/{anime_url}').text

def queryEpisodes(anime_name, episode):
    # Fetch streaming url of that episode
    url = f"https://gogoanime.sk/{anime_name}-episode-{episode}"
    soup = BeautifulSoup(
        requests.get(url).text, 'html.parser')
    url = soup.find('div',class_="play-video").iframe.get("src")
    return url

if __name__=="__main__":
    print(queryEpisodes('naruto', '2'))