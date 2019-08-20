# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from interior_app.models import Locations, LocationData, Categories, ScrapLocations


class HouzzScrapPipeline(object):

	# def __init__(self):
	# 	self.create_connection()
	# 	self.create_table()

	# def create_connection(self):
	# 	self.db = sqlite3.connect("houzz.db")
	# 	self.cursor = self.db.cursor() 

	# def create_table(self):
	# 	self.cursor.execute(""" DROP TABLE IF EXISTS location_tb """)
	# 	self.cursor.execute(""" create table location_tb (location text, categories text, profile_name text, person_name text, phone text, about_us text) """)
	# 	print("========= Table created =============")


	def process_item(self, item, spider):

		# self.store_location_data(item)		
		item.save()		
		print("================ Saved =================")
		return item
	

	# def store_location_data(self, item):
	# 	self.cursor.execute(""" insert into location_tb(profile_name, person_name, phone, about_us) values(?,?,?,?) """,(item['profile_name'],item['person_name'],item['phone'], item['about_us']))
	# 	# self.cursor.execute(""" insert into location_tb(location, categories, profile_name, person_name, phone, about_us) values(?,?,?,?,?,?) """,(item['location'], item['categories'], item['profile_name'],item['person_name'],item['phone'], item['about_us']))
	# 	self.db.commit()




