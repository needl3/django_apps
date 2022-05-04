import requests
import string
from bs4 import BeautifulSoup
import csv
import time
import logging

class ScrapeAnime:
	def __init__(self):
		self.base = "https://gogoanime.sk"
		self.all_anime = "/anime-list-"
		self.writer = None
		logging.basicConfig(filename='anime_scrape.log', level=logging.INFO)

	def scrapeAnimeDetails(self,url):
		logging.info('Scraping anime details for: '+url)
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

		db_val = {"Summary":summary,
				 "Genre":genre,
				 "Episodes":episodes,
				 "Status":status,
				 "Image":image_link,
				 "Released": released
				 }
		return db_val

	def scrapeAnime(self, c, file=None, db_obj=None, page_number=1):

		logging.info('[+] Fetching for '+c+" in page "+str(page_number))

		# Url for all anime list starting with letter <c>
		url=self.base+self.all_anime+c.upper()+"?page="+str(page_number)

		html = requests.get(url).text

		soup = BeautifulSoup(html, 'html.parser')

		anime_list = soup.find('div', class_='anime_list_body').ul.find_all('li')

		# For writing title:url in csv
		fieldnames = ['Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Status', 'Released', 'Url']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()

		for anime in anime_list:
			# Find basic info i.e URL to anime
			title = anime.a.text
			url = anime.a.get('href')


			try:
				db_val = self.scrapeAnimeDetails(self.base+url)
				db_val['Name'] = title
				db_val['Url'] = url
				writer.writerow(db_val)

				time.sleep(1)
			except Exception as e:
				logging.debug("Exception for "+ title + "\n URL: "+url+"\n Exception: "+e)
				pass


	def scrapeAll(self, to_save=None):
		file = None
		if to_save:
			file = open(to_save,'a')
		for i in string.ascii_uppercase:
			total_pages=int(self.findMaxPages(i))
			for page_number in range(1,total_pages+1):
				self.scrapeAnime(i, file, page_number)
				time.sleep(1)
			break

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
				fieldnames = ['Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Status', 'Url']
				writer = csv.DictWriter(f_write, fieldnames=fieldnames)
				writer.writeheader()

				reader = csv.DictReader(f_read, fieldnames=['title', 'urls'])
				count = 1
				for row in reader:
					logging.info("[+] Writing row "+str(count))
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
	def updateNewSeasons(self, file=None, models=None):
		logging.info("Updating new seasoned animes")
		'''
			Updates HOT tab
			This should be cron jobed every 7 days to update new animes in main database
		'''

		new_page = "new-season.html"
		if file != None:
			file = open(file,'w')
			self.writer = csv.DictWriter(file, fieldnames=['Name',  'Url'])
			self.writer.writeheader()

		for i in range(1, int(ScrapeAnime().findMaxPages(page=new_page))+1):
			url = self.base+"/"+new_page+"?page="+str(i)

			soup = BeautifulSoup(requests.get(url).text,'html.parser')
			new = soup.find('div', class_='last_episodes').ul.find_all('li')
			details = [{'Name':i.text.strip().split('\n')[0], 'Image':i.div.a.img['src'], 'Url':i.div.a['href'].split('/category/')[1]} for i in new]
			for i in details:
				if file != None:
					self.writer.writerow({'Name':i['Name'], 'Url':i['Url']})
				if models != None:
					# Check if I have this new anime in database
					# If not make an entry
					try:
						models.Video.objects.get(name=i['Name'])
						# If I have that anime, check if it's in Hot table
						# If not make an entry
						try:
							models.Hot.objects.get(name=i['Name'])
						except:
							models.Hot(name=i['Name']).save()
					except:
						# Since this anime is not in Video table
						# Make an entry with all it's details
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
		if file != None:
			file.close()
	def updateNewReleases(self, models):
		'''
			Updates NewReleases Section i.e recent;y released new episodes
			Scrapes {Name, Last Episode} and compare with our database(Recent Releases)
			If some in my database are left out, check if they are completed and assign status accordingly
		'''
		new_list = ScrapeAnime().scrapeNewSection()	# Returns list of {Name:episode}
		print(new_list)
		for n,ep in new_list.items():
			try:
				models.Video.objects.get(name=n)
				try:
					models.NewReleases.objects.get(name=n)
				except:
					models.NewReleases(name=n).save()
			except:
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

	def updatePopular(self, models):
		new_list = ScrapeAnime().scrapePopular()	# Returns list of {Name:url}
		for n,url in new_list.items():
			try:
				models.Video.objects.get(name=n)
				try:
					models.Popular.objects.get(name=n)
				except:
					models.Popular(name=n).save()
			except:
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

if __name__=="__main__":
	DatabaseManagement().updateNewReleases()