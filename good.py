from queue import Empty
from my_library import *
from driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style
from my_database import DB, Goods


class GoodWD:
	def __init__(self,db:DB, good:Goods, ol:WD, pc_good_link, pc_price:str, submissive:bool, parent:str):
		self.db = db
		self.good = good
		self.ol = ol
		self.submissive = submissive
		self.parent = parent
		self.parent_link = pc_good_link.replace(r'amp;', '')
		ol.Get_HTML(self.parent_link)
		self.Load_Good_Attributes(ol, pc_good_link, pc_price)

	def Load_Good_Attributes(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.size = ''
		self.prices = []
		self.color = ''
		self.colors = []
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = 0
		self.brand = ''
		self.sale = False
		self.instock = ''
		self.id = sx(ol.driver.page_source,'<div class="ty-product-option-child">','<')
		print('id ========>>>', self.id)
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))

		#ol.Get_HTML(pc_good_link)

		self.article = sx(ol.driver.find_element(By.CLASS_NAME, value='ty-features-list').text,'Артикул',' ')
		self.name = ol.driver.find_element(By.TAG_NAME, value='h1').text.strip()
		self.price = sx('|'+ol.driver.find_element(By.CLASS_NAME, value='ty-price-num').get_attribute('innerHTML'),'|','<').strip().replace('&nbsp;','')
		self.description = (ol.driver.find_element(By.CLASS_NAME, value ='ty-features-list').text + ' ' + ol.driver.find_element(By.ID, value ='content_description').text).strip()
		
		soup = BS(ol.page_source, features='html5lib')
		pictures = soup.find_all('a',{'class':'cm-image-previewer cm-previewer ty-previewer'})
		for picture in pictures:
			lc = sx(  str(picture).replace(' ',''),  'href="', '"')
			if len(self.pictures)<12:
				append_if_not_exists(lc, self.pictures)
		
		information_block = ol.driver.find_element(by=By.XPATH, value="""//div[@class='ut2-pb__right']""") # right information panel with base good options
		str_to_file('information.html',information_block.get_attribute('innerHTML'))
		allinstock = information_block.find_elements(by=By.XPATH, value="//span[@class='ty-qty-in-stock ty-control-group__item']")
		if len(allinstock)>=1:
			self.instock = allinstock[1].text
			counter = 0
			for i in range(self.ol.page_source.count('<input type="radio"')):
				lc = sx(self.ol.page_source, '<input type="radio"','</label>',i+1)
				if 	('"'+	pc_good_link+'"' in lc) and \
					('checked' in lc):
					counter += 1
					data = sx(lc,'<bdi>','</bdi>')
					if counter == 1:
						self.size = data
					else:
						self.color = data
				



		
		#for i in range(ol.driver.page_source.count("data-ca-product-url")):
		#	print(sx(ol.driver.page_source,'data-ca-product-url="','"',i+1))
		self.db.save_good_from_parameter(	catalog=pc_price, 
											link_on_parent_page=self.parent, 
											link_on_good=pc_good_link,
											article=self.article,
											name=self.name,
											description=self.description,
											price=self.price,
											pictures=' '.join(self.pictures).strip(),
											colors=self.color,
											sizes=self.size,
											instock=self.instock)

		if '?' not in pc_good_link: # only for no root goods we must find their child variants of sizes and colors
			links = ol.driver.find_elements(by=By.XPATH, value="""//tr[@class='ty-variations-list__item']""")
			#print(links, len(links))
			for link in links:
				lc = sx(link.get_attribute('innerHTML'),'<span class="ty-product-options-content">','<')
				if lc.strip() == self.id.strip(): # if section-id and page-id is coincide we need to write links on other option pages into database
					lc_link_on_variant = sx(link.get_attribute('innerHTML'), '<a href="','"')
					if '?' in lc_link_on_variant: # option-pages have a question mark
						print(lc_link_on_variant)
						self.db.save_good_from_parameter(catalog=pc_price, link_on_parent_page=pc_good_link, link_on_good=lc_link_on_variant)




