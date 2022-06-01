from django_cron import CronJobBase
from .templatetags import scraper
from . import models

# RUN_EVERY_MINS format: month day hour minute

class updateHot(CronJobBase):
    RUN_EVERY_MINS =  1 * 1 * 24 * 60 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aniwatch.updateHot'    # a unique code

    def do(self):
    	scraper.DatabaseManagement().updateNewSeasons(models)    

class updateNewReleases(CronJobBase):
    RUN_EVERY_MINS = 1 * 1 * 24 * 60 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aniwatch.updateNewReleases'    # a unique code

    def do(self):
    	scraper.DatabaseManagement().updateNewReleases(models)

class updatePopular(CronJobBase):
    RUN_EVERY_MINS = 1 * 1 * 24 * 60 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aniwatch.updatePopular'    # a unique code

    def do(self):
    	scraper.DatabaseManagement().updatePopular(models)

class updateOngoing(CronJobBase):
    RUN_EVERY_MINS = 1 * 1 * 24 * 60 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aniwatch.updateOngoing'    # a unique code

    def do(self):
    	scraper.DatabaseManagement().updateOngoing(models)