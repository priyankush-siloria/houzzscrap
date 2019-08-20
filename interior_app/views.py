from django.shortcuts import render
import json
import os
import sys
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from interior_app.models import Locations, LocationData, Categories, ScrapLocations, ScrapeStatus
# from interior_app.Interiors import dataScraper
from django.core.mail import send_mail
from django.conf import settings

import subprocess
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings

# from houzz_scrap.spiders.houzz_spider import HouzzSpider 
# from spiders.houzz_spider import HouzzSpider


# Create your views here.
class IndexView(TemplateView):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		# LocationData.objects.filter(location__location="himachal").delete()
		return render(request, self.template_name, {})


@csrf_exempt
def addLocation(request):
	if request.method=="POST":
		if request.is_ajax():
			location = request.POST.get('location').lower()		
			print("Loaction recieved --> ", location)
			if not Locations.objects.filter(location=location).exists():
				loc = Locations(location=location)
				loc.save()
				print(" location saved ")
				return JsonResponse({"status":"success", "loc":location })			
			else:
				print(" Already exist ")
				return JsonResponse({"status":"failed", "loc":location })
		else:
			print("Not ajax call")

	return HttpResponseRedirect(" ")


def loadLocations(request):
	locs = Locations.objects.all()
	# print("locations: ",len(locs))
	locations = []
	for loc in locs:
		locations.append(loc.location)

	if ScrapeStatus.objects.all():
		status = ScrapeStatus.objects.all()	
		print("Status scrape_status==> ", status[0].scrape_status)
		return JsonResponse({"status":"success", "locs":locations, "ScrapeStatus":status[0].scrape_status}) 
	else:	 	
	 	status = False
	 	print("else Status ==> ", status)
	 	return JsonResponse({"status":"success", "locs":locations, "ScrapeStatus":status})
	

	return JsonResponse({"status":"success", "locs":locations, "ScrapeStatus":status[0].scrape_status})


@csrf_exempt
def scrapeData(request):
	if request.method=="POST":     

		ScrapLocations.objects.all().delete()
		cities = request.POST.get('cities')
		cityList = cities.split(',')
		for city in cityList:
			loc = ScrapLocations(city=city)
			loc.save()

		subject = "Houzz Scraping Alert"
		sccuess_status="Houze Scraping script is started."
		recipients = ["director@avioxtechnologies.com","sauravsaha.in@gmail.com"]
		send_status = mailSend(subject, recipients, html_message=sccuess_status)
		try:
			print("====== Try block ======= ")
			
			project_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			# print("project directory ==> ", project_Dir)
			# print("New path => ", os.path.join(project_Dir, 'houzz_scrap'))
			CONFIG_PATH = os.path.join(project_Dir, 'houzz_scrap')
			os.chdir(CONFIG_PATH)			
			p = subprocess.call(["scrapy", "crawl","houzzScrapper"])
			# p = subprocess.call(["scrapy", "crawl","houzzScrapper","-o","chd_arch.csv"])
			print("Process end")

			sccuess_status="Houze Scraping script is completed successfully."	
			recipients = ["director@avioxtechnologies.com","sauravsaha.in@gmail.com"]
			send_status = mailSend(subject, recipients, html_message=sccuess_status)

			return JsonResponse({"status":"success"})
		except Exception as e:
			print("===== exception block ==> ",str(e))
			raise e
			sccuess_status="Script is stopped due to some error."
			recipients = ["director@avioxtechnologies.com","sauravsaha.in@gmail.com"]
			send_status = mailSend(subject, recipients, html_message=sccuess_status)
			return JsonResponse({"status":"failed"})
	return HttpResponseRedirect("")


def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		return True
	except Exception as e:
		print(str(e))
		return False


class DatabaseView(TemplateView):
	template_name = "database.html"

	def get_context_data(self, **kwargs):
		context = super(DatabaseView, self).get_context_data(**kwargs)
		context['records'] = LocationData.objects.all()
		context['categories'] = Categories.objects.all()        
		return context



def searchByLocation(request):	
	q = request.GET.get('q')
	print("q ==> ",q)
	category = request.GET.get("categories")
	print("category ==> ",category)
	if category=="all":
		if q:
			records = LocationData.objects.filter(location__location__contains=q)
		else:
			records = LocationData.objects.all()
	else:
		if q:
			records = LocationData.objects.filter(location__location__contains=q, categories__slug__contains=category)
		else:
			records = LocationData.objects.filter(categories__slug__contains=category)
	categories = Categories.objects.all() 
	print("categories ==> ",categories)
	return render(request, "database.html" , {'records':records,'categories':categories,"cat_search_item":category,"search_item":q})



