from .templatetags import scraper
from . import models

def updateHot():
	scraper.DatabaseManagement().updateNewSeasons(models)

def updateNewReleases():
	scraper.DatabaseManagement().updateNewReleases(models)

def updatePopular():
	scraper.DatabaseManagement().updatePopular(models)

def updateOngoing():
	scraper.DatabaseManagement().updateOngoing(models)