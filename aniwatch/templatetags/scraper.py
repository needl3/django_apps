import requests
import string
from bs4 import BeautifulSoup
import csv
import time

class ScrapeAnime:
	def __init__(self):
		self.base = "https://gogoanime.sk"
		self.all_anime = "/anime-list-"
		self.anime_dict = dict()


	def scrapeAnime(self, c, file=None, page_number=1):

		print('[+] Fetching for '+c+" in page "+str(page_number), end='\n')

		# Url for all anime list starting with letter <c>
		url=self.base+self.all_anime+c.upper()+"?page="+str(page_number)

		html = requests.get(url).text

		soup = BeautifulSoup(html, 'html.parser')

		anime_list = soup.find('div', class_='anime_list_body')

		# For writing title:url in csv
		writer = csv.DictWriter(file, fieldnames=['title','url'])

		for anime in anime_list.ul.find_all('li'):
			self.anime_dict[anime.a.text] = anime.a.get('href')
			if file:
				writer.writerow({"title":f"{anime.a.text}", "url":f"{anime.a.get('href')}"})

	def scrapeAll(self, to_save=None):
		file = None
		if to_save:
			file = open(to_save,'a')
		for i in string.ascii_uppercase:
			total_pages=int(self.findMaxPages(i))
			for page_number in range(1,total_pages+1):
				self.scrapeAnime(i, file, page_number)
				time.sleep(1)
	def findMaxPages(self, alphabet, max_page=1):
		# First find all shown pages
		url=self.base+self.all_anime+alphabet+"?page="+str(max_page)
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
				return self.findMaxPages(alphabet, m)
		except AttributeError:
			# Means there was no pagination class
			# ie. no listing
			# ie. only one page
			return '1'

	def updateAnimeDetails(self, f, to_save):
		with open(f, 'r') as f_read:
			with open(to_save, 'w') as f_write:
				fieldnames = ['Name', 'Image', 'Summary', 'Genre', 'Episodes', 'Status', 'Url']
				writer = csv.DictWriter(f_write, fieldnames=fieldnames)
				writer.writeheader()

				reader = csv.DictReader(f_read, fieldnames=['title', 'urls'])
				count = 1
				for row in reader:
					print("[+] Writing row "+str(count))
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

if __name__=="__main__":
	# s = BeautifulSoup(requests.get("https://gogoanime.sk/category/naruto").text, 'html.parser')
	# lis = s.find('ul', id='episode_page')
	# print(lis.find_all('li')[-1].a['ep_end'])
#	ScrapeAnime().scrapeAll('AnimeList.csv')
	ScrapeAnime().updateAnimeDetails('AnimeList.csv', 'AnimeDetails.csv')