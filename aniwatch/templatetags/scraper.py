#!/usr/bin/python3
import requests
import string
from bs4 import BeautifulSoup
import csv
import time
import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

class ScrapeAnime:
	def __init__(self):
		self.base = "https://gogoanime.sk"
		self.all_anime = "/anime-list-"
		self.writer = None

		# Logfile for general scrape log
		self.log_scrape_general = setup_logger('second_logger', '.scrape.log')

		# Log handler for resumable fetch
		self.log_scrape_stat = None

	def scrapeAnimeDetails(self,url):
		self.log_scrape_general.info('Scraping anime details for: '+url)
		'''
			Fetch details of that anime
			url = <https://gogoanime.sk/category/anime-url>
		'''

		html_details = requests.get(url).text
		soup_details = BeautifulSoup(html_details, 'html.parser')
		details = soup_details.find('div', 'anime_info_body')

		image_link = details.img['src']

		sub_details = details.find_all('p', class_='type')

		status = sub_details[4].a.text;

		summary = sub_details[1].text.split(":")[1].strip()

		genre = [i.text.strip(', ') for i in sub_details[2].find_all('a')]

		released = sub_details[3].text.split(' ')[1]

		episodes = soup_details.find('ul', id='episode_page').find_all('li')[-1].a['ep_end']

		anime_type = sub_details[0].a.text

		db_val = {"Summary":summary,
				 "Genre":genre,
				 "Episodes":episodes,
				 "Status":status,
				 "Image":image_link,
				 "Released": released,
				 "Type": anime_type,
				 }
		return db_val

	def scrapeAnime(self, c, file=None, db_obj=None, page_number=1, last_anime=None):

		self.log_scrape_general.info('[+] Fetching for '+c+" in page "+str(page_number))

		# Url for all anime list starting with letter <c>
		url=self.base+self.all_anime+c.upper()+"?page="+str(page_number)

		html = requests.get(url).text

		soup = BeautifulSoup(html, 'html.parser')

		anime_list = soup.find('div', class_='anime_list_body').ul.find_all('li')
		if(last_anime):
			next_anime_index = None
			for next_anime_index in range(len(anime_list)):
				if(anime_list[next_anime_index].a.text == last_anime):
					break
			anime_list = anime_list[next_anime_index+1:]

		# For writing title:url in csv
		fieldnames = ['Name', 'Image', 'Summary', 'Genre', 'Type', 'Episodes', 'Status', 'Released', 'Url']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		for anime in anime_list:
			# Find basic info i.e URL to anime
			title = anime.a.text
			url = anime.a.get('href')


			db_val = self.scrapeAnimeDetails(self.base+url)
			db_val['Name'] = title
			db_val['Url'] = url.split('/category/')[1]
			writer.writerow(db_val)

			self.log_scrape_stat.info(f'{c},{page_number},{db_val["Name"]}')
	
			time.sleep(1)


	def scrapeAll(self, to_save):
		file = None

		# Logfile for resuming scrapes
		scrape_log_file = '.scrape_stat.log'

		with open(to_save,'a') as file:
			alphabets = None
			page_start = 1
			last_anime = None

			try:
				alphabets = open(scrape_log_file, 'r').readlines()[-1].strip().split(',')
				page_start = alphabets[1]
				last_anime = alphabets[2]
				alphabets = string.ascii_uppercase[string.ascii_uppercase.index(alphabets[0]):]
				print("Resuming scrape from alphabet", alphabets[0], ' and page ', page_start)
			except:
				alphabets = string.ascii_uppercase

			self.log_scrape_stat = setup_logger('first_logger', scrape_log_file)

			for i in alphabets:
				total_pages=int(self.findMaxPages(i))

				print("Fetching for alphabet ", i)

				for page_number in range(int(page_start),total_pages+1):
					print("Fetching for page ", page_number)
					self.scrapeAnime(i, file=file, page_number=page_number, last_anime=last_anime)

					self.log_scrape_general.info(f"Exception during scraping letter {i} in page {page_number}")

					time.sleep(1)
				page_start = 1
			os.remove(scrape_log_file)

	def findMaxPages(self, alphabet=None, max_page=1, page=None):
		# First find all shown pages
		url = ""
		if page == None:
			url=self.base+self.all_anime+alphabet+"?page="+str(max_page)
		else:
			url = self.base+"/"+page+"?page="+str(max_page)
		html = requests.get(url).text

		soup = BeautifulSoup(html, 'html.parser')
		try:
			pagination = soup.find('ul', class_='pagination-list')
			pages = pagination.find_all('li')
			m = pages[-1].text
			if m == max_page:
				return max_page
			else:
				# Now visit every last pages to reveal further pages
				return self.findMaxPages(alphabet=alphabet, max_page=m, page=page)
		except AttributeError:
			# Means there was no pagination class
			# ie. no listing
			# ie. only one page
			return '1'

	def updateAnimeDetails(self, f, to_save):
		'''
			This was used to unify partial data from two csv's
			during this project's initial database creation

			Don't use it
		'''
		with open(f, 'r') as f_read:
			with open(to_save, 'w') as f_write:
				fieldnames = ['Name', 'Image', 'Summary', 'Genre', 'Type', 'Episodes', 'Status', 'Url']
				writer = csv.DictWriter(f_write, fieldnames=fieldnames)
				writer.writeheader()

				reader = csv.DictReader(f_read, fieldnames=['title', 'urls'])
				count = 1
				for row in reader:
					self.log_scrape_general.info("[+] Writing row "+str(count))
					html = requests.get(self.base+row['urls']).text

					soup = BeautifulSoup(html, 'html.parser')
					try:
						details = soup.find('div', 'anime_info_body')

						image_link = details.img['src']

						sub_details = details.find_all('p', class_='type')

						status = sub_details[4].a.text;

						summary = sub_details[1].text.split(":")[1].strip()

						genre = [i.text.strip(', ') for i in sub_details[2].find_all('a')]

						episodes = soup.find('ul', id='episode_page').find_all('li')[-1].a['ep_end']

						url = None

						# Info to write: Name, ImageLink, Summary, Genre
						writer.writerow({'Name':row['title'], 'Image':image_link, 'Summary':summary, 'Genre': genre, 'Episodes':episodes, 'Status':status, 'Url':url})

						time.sleep(1)

						count += 1
					except:
						pass
	def getServers(anime_url, episode="1"):
		url = f'https://gogoanime.sk/{anime_url}-episode-{episode}'
		r = requests.get(url).text
		soup = BeautifulSoup(r, 'html.parser')
		li_servers = soup.find('div', class_='anime_muti_link')

		# --------------------------------------------------------------------------------------
		# If general convention that links follow is extempted
		# Then scrape the anime page and get links for episodes
		# Then is all the same

		# Current Issue is that for the episode links to appear
		# the javascript must be executed for that particular episode
		# Todo: Find a way to execute that javascript event handler to reveal link

		if li_servers == None:
			
			# Fetch anime's home site and its episode list
			from requests_html import HTMLSession
			session = HTMLSession()

			url = "https://gogoanime.sk/category/"+anime_url
			r = session.get(url).html.render()
			soup = BeautifulSoup(r, 'html.parser')
			soup = soup.find('div', class_='episode_related')
			soup = soup.find_all('li')
			ep = soup[len(soup)-int(episode)]
			ep = ep.a['href']
			url = f'{self.base}{ep}'
			
			r = requests.get(url).text
			soup = BeautifulSoup(r, 'html.parser')
			li_servers = soup.find('div', class_='anime_muti_link')
		# --------------------------------------------------------------------------------------

		li_servers = li_servers.find_all('li')
		li_names = [i.a.text.strip().split('Choose')[0] for i in li_servers]
		a_href = [i.a['data-video'].strip('//') for i in li_servers]
		final = list()
		for j in range(len(li_names)):
			final.append({'Name':li_names[j], 'Url':a_href[j]})
		return final

	def scrapeNewSection(self):
		soup = BeautifulSoup(requests.get(self.base+'/popular.html').text, 'html.parser')
		recents = soup.find('nav', class_='menu_recent').find_all('li')
		all_recents = dict()
		for li in recents:
			a = li.find_all('a')
			name = a[0]['title']
			episode = a[1].p.text[-1]
			url = a[0]['href'].split('-episode')[0][1:]
			all_recents[name] = [episode, url]
		return all_recents

	def scrapePopular(self):
		soup = BeautifulSoup(requests.get(self.base+'/popular.html').text, 'html.parser')
		recents = soup.find('div', class_='last_episodes').find_all('li')
		all_recents = dict()
		for li in recents:
			a = li.find_all('a')
			name = a[0]['title']
			url = a[0]['href'].split('/category/')[1]
			all_recents[name] = url
		return all_recents

class DatabaseManagement:
	def __init__(self):
		self.base = 'https://gogoanime.sk'
		self.writer = None
		self.log_scrape_general = setup_logger('database_update_logger', '.database_update.log')

	def updateNewSeasons(self, models):
		'''
			Updates HOT tab
			This should be cron jobed every day to update new animes in main database
		'''

		new_page = "new-season.html"

		details_all = list()

		for i in range(1, int(ScrapeAnime().findMaxPages(page=new_page))+1):
			url = self.base+"/"+new_page+"?page="+str(i)

			soup = BeautifulSoup(requests.get(url).text,'html.parser')
			new = soup.find('div', class_='last_episodes').ul.find_all('li')
			details = [{'Name':i.text.strip().split('\n')[0], 'Image':i.div.a.img['src'], 'Url':i.div.a['href'].split('/category/')[1]} for i in new]
			for i in details:
				try:
					models.Video.objects.get(name=i['Name'])
					# If I have that anime, check if it's in Hot table
					# If not make an entry
					try:
						models.Hot.objects.get(name=i['Name'])
					except:
						print("New popular anime in town: "+i['Name'])
						models.Hot(name=i['Name']).save()
				except:
					# Since this anime is not in Video table
					# Make an entry with all it's details
					print("New Anime in town: "+i['Name'])
					l_details = ScrapeAnime().scrapeAnimeDetails(self.base+"/category/"+i['Url'])
					models.Video(name=i['Name'],
							url=i['Url'],
							image_link=l_details['Image'],
							summary=l_details['Summary'],
							genre=l_details['Genre'],
							episodes=l_details['Episodes'],
							status=l_details['Status'],
							released=l_details['Released'],
					).save()
					models.Hot(name=i['Name']).save()

			# Remove expired "Anime in Hot Model"
			details_all += [list(i.values())[0] for i in details]
			for anime in models.Hot.objects.all():
				if anime.name not in details_all:
					print("Deleting "+anime.name+" from Hot")
					try:
						models.Hot.objects.get(name=anime.name).delete()
					except:
						print(anime.name + " doesn't exist in the Hot Table")
	def updateNewReleases(self, models):
		'''
			Updates NewReleases Section i.e recent;y released new episodes
			Scrapes {Name, Last Episode} and compare with our database(Recent Releases)
			If some in my database are left out, check if they are completed and assign status accordingly
		'''
		new_list = ScrapeAnime().scrapeNewSection()	# Returns list of {Name:episode}
		for n,ep in new_list.items():
			try:
				models.Video.objects.get(name=n)
				try:
					models.NewReleases.objects.get(name=n)
				except:
					print("New Release found for the anime")
					models.NewReleases(name=n).save()
			except:
				print("Brand new anime in town: "+n)
				db_val = ScrapeAnime().scrapeAnimeDetails(self.base+"/category/"+ep[1])
				models.Video(
					name = n,
					image_link = db_val['Image'],
					summary = db_val['Summary'],
					genre = db_val['Genre'],
					status = db_val['Status'],
					episodes = ep[0],
					url = ep[1]
				).save()
				models.NewReleases(name=n, last_ep=ep[0]).save()

			# Update in main table
			ob = models.Video.objects.get(name=n)
			ob.episodes = ep[0]
			ob.save()

		# Remove expired "Anime"
		for anime in models.NewReleases.objects.all():
			if anime.name not in new_list.keys():
				print("Deleting "+anime.name+" from NewReleases")
				try:
					models.NewReleases.objects.get(name=anime.name).delete()
				except:
					print(anime.name + " doesn't exist in the NewReleases Table")

	def updatePopular(self, models):
		new_list = ScrapeAnime().scrapePopular()	# Returns list of {Name:url}
		for n,url in new_list.items():
			try:
				models.Video.objects.get(name=n)
				try:
					models.Popular.objects.get(name=n)
				except:
					print("New Popular anime in town: "+n)
					models.Popular(name=n).save()
			except:
				print("Brand New Anime in town: "+n)
				db_val = ScrapeAnime().scrapeAnimeDetails(self.base+"/category/"+url)
				models.Video(
					name = n,
					image_link = db_val['Image'],
					summary = db_val['Summary'],
					genre = db_val['Genre'],
					status = db_val['Status'],
					episodes = db_val['Episodes'],
					url = url
				).save()
				models.Popular(name=n).save()

		# Remove expired "Anime"
		for anime in models.Popular.objects.all():
			if anime.name not in new_list.keys():
				print("Deleting "+anime.name+" from Popular")
				try:
					models.Popular.objects.get(name=anime.name).delete()
				except:
					print(anime.name + " doesn't exist in the Popular Table")

	def updateOngoing(self, models):
		old_ongoing = models.Video.objects.filter(status="Ongoing")
		for old_anime in old_ongoing:
			try:
				stat = ScrapeAnime().scrapeAnimeDetails(self.base+"/category/"+old_anime.url)['Status']
			except AttributeError:
				print("Invalid Url ", old_anime.url)
			print("Anime: ", old_anime.name, "New Status: ", stat)
			if(stat != "Ongoing"):
				print("Changing stat of ", old_anime.name, "to ", stat)
				old_anime.status = stat
				old_anime.save()
if __name__=="__main__":
	ScrapeAnime().scrapeAll('UpdatedAnimeDetails.csv')
	os.system("touch done.txt")