import scrapy
import csv
import time

from scrapy import signals 
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import FormRequest
from scrapy.mail import MailSender
from scrapy.utils.response import open_in_browser
from scrapy.exceptions import *

from django.core.mail import send_mail
from houzz_scrap.items import HouzzScrapItem
from interior_app.models import Locations, LocationData, Categories, ScrapLocations, ScrapeStatus


class HouzzSpider(scrapy.Spider):
    """
    This class define a Spider that scrapes posts from WattPanel blog
    """
    name = "houzzScrapper"
    # download_delay = 5.0
    # allowed_domains = [""]

    # categories = ["architects", "interior-designers-and-decorators", "design-build-firms", "furniture-and-accessories" ]
    # locations = [] # # locations = ['chandigarh', 'Hyderabad', 'delhi', 'himachal']   
    cat_urls = [
        "https://www.houzz.in/professionals/architects/c/",
        "https://www.houzz.in/professionals/interior-designers-and-decorators/c/",
        "https://www.houzz.in/professionals/design-build-firms/c/",
        "https://www.houzz.in/professionals/furniture-and-accessories/c/",
    ]
    start_urls = []

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_idle, signals.spider_idle)

    def spider_opened(self, spider):
        print("\n***************************************** ")
        print("\n**************** Spider Opened ********** ")
        print("\n***************************************** ")

        if ScrapeStatus.objects.all():
            ScrapeStatus.objects.filter(scrape_status=False).update(scrape_status=True)
            print("Status scrape_status==> ", status[0].scrape_status) 
            print("Status scrape_status type ==> ", type(status[0].scrape_status) )
            
        else:
            status = ScrapeStatus(scrape_status=True)
            status.save()                 


    def spider_closed(self, spider):
        print("\n***************************************** ")
        print("\n**************** Spider Closed ********** ")
        print("\n***************************************** ")

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        print("\n***************************************** ")
        print("\n**************** Spider Idle ************ ")
        print("\n***************************************** ")         
        try:
            print("**** Try *******")
            if ScrapeStatus.objects.all():
                ScrapeStatus.objects.filter(scrape_status=True).update(scrape_status=False)
                status = ScrapeStatus.objects.all()
                print("Status scrape_status==> ", status[0].scrape_status) 
                print("Status scrape_status type ==> ", type(status[0].scrape_status))                   

            raise DontCloseSpider
        except:
            print("**** Except *******")
            pass
        finally:
            print("**** Finally *******")
            raise CloseSpider("End scrapping")


    
    def get_urls(self):
        locationss = ScrapLocations.objects.all()
        print("Location/Cities ====> ",locationss)
        for location in locationss:
            for cat_url in self.cat_urls:
                print("location", location)
                # locations.append(location.city)       
                url = cat_url + location.city +""
                print("============ complete URL ========= > ", url)
                self.start_urls.append(url)


        
    # start_url = "https://www.houzz.in/professionals/searchDirectory?topicId=26676&query=Architects+%26+Building+Designers&location=Hyderabad%2C+India&distance=50&sort=4"
    # start_url = "https://www.houzz.in/professionals/interior-designers-and-decorators/c/delhi/p/15"

    def start_requests(self):
        self.get_urls()
        
        for url in self.start_urls:                   
            # new_url = url + location
            yield self.make_requests_from_url(url)

    
   
    def parse(self, response):  #parse_pages(self,response): 
        print("\nPage url =========> ",response.url) 

        cat_url = response.url
        print("Response url ==> ",cat_url)
        cat_string = cat_url.split('/')
        print("category_string =====> ",cat_string[4])
        location_string = cat_string[6].strip()
        location_string = cat_string[6].replace("%20"," ")

        print("location_string =====> ",location_string)        

        profile_pages = response.xpath("//a[@class='header-5 text-unbold']/@href").extract()
        if profile_pages:
            print("\n profile_pages =====================> ",profile_pages )
            for page  in  profile_pages:
                # yield response.follow(page, self.parse_profiles)
                request = scrapy.Request(page, callback=self.parse_profiles,  meta={'location': location_string, "category":cat_string[4]}, dont_filter = True)
                yield request

           
        # Verify if contains more pages
        try:
            next_page = response.xpath("//a[@class='hz-pagination-link hz-pagination-link--next']/@href").extract()[0]
            # next_page = response.url  +"/p/" +str(self.p)
            print("\nNext_Profile_Page==============> ",next_page)        
            # self.p += 15            
           
            if next_page:
                next_page = response.urljoin(next_page)
                request = scrapy.Request(next_page, callback=self.parse, meta={'location': location_string, "category":cat_string[4]}, dont_filter = True)
                yield request    
        except IndexError:
            print(" ***************************************************************************** ")
            print(" ******************************* Index out of range ************************** ")
            pass


    def parse_profiles(self, response):
        item = HouzzScrapItem() 

        location = response.meta.get('location')
        category = response.meta.get('category')

        name = response.xpath("//h1[@class='hz-profile-header__name']/text()").extract()
        print("\n Profile Name :============> ",name)
        phone = response.xpath('//a[@class="hz-profile-header__contact-method hz-track-me"]/span/text()').extract()
        if not phone:
            phone.append("")
        print("\nPhone number ==> ", phone[0])

        about_div = response.xpath('//div[@class="profile-about__content"]/div')

        contents = ""

        for row in about_div:
            content = row.css("div::text").extract()
            if content:
                contents = content[0]

            content1 = row.css("h6 ::text").extract()
            if content1:
                contents = contents + " " +content1[0]

            content2 = row.css("p ::text").extract()
            if content2:
                contents = contents + " " +content2[0]

        contents = contents.replace('\n','')
        # print("contents ==> ",contents)  

        person_info = response.xpath('//div[@class="profile-meta__val"]/text()')[0].extract()
        seprated_person_all_info = (person_info).split("\n")
        person_name = seprated_person_all_info[0]
        if not person_name:
            person_name = ""
        print("person_name: ", person_name)        
        print("Location =====> ",location)
        print("Category =====> ",category)

        categories = Categories.objects.get(slug=category)
        print("\nCategories ===> ", categories)
        location = Locations.objects.get(location=location)

        # if not LocationData.objects.filter(person_name=person_name, profile_name=name[0], categories=categories).exists():
        # print("==========  Unique record ==========")
        item['location'] = location
        item['categories'] = categories
        item['profile_name'] = name[0]
        item['person_name'] = person_name        
        item['phone'] = phone[0]
        item['about_us'] = contents

        yield item
        # else:
        #     print("============ Duplicate record ========== ")

