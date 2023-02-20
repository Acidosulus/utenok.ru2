from click import echo, style
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from sqlalchemy import cast, Date, distinct, union
# создаем класс, от которого будут наследоваться модели

Base = declarative_base()

# определяем модельи классов для автора, книги и издательства
class Goods(Base):
	__tablename__ = "goods"
	row_id = Column(Integer) #, auto_increment=True,  primary_key=True, nullable=False
	catalog = Column(String(10240), nullable=False, primary_key=True,)
	link_on_parent_page = Column(String(10240), nullable=False, primary_key=True)
	link_on_good = Column(String(10240), nullable=False, primary_key=True)
	article = Column(String(10240))
	name = Column(String(10240))
	description = Column(String(10240))
	price = Column(String(10240))
	pictures = Column(String(10240))
	colors = Column(String(10240))
	sizes = Column(String(10240))
	instock = Column(String(10240))

	def __str__(self)->str:
		return 	style(text = 'row_id: ', bg='white', fg='black') + style(text = self.row_id, fg='bright_white') +  '\n'+ \
				style(text = 'catalog: ', bg='white', fg='black') + style(text = self.catalog, fg='bright_white') + '\n'+ \
				style(text = 'link_on_parent_page: ', bg='white', fg='black') + style(text = self.link_on_parent_page, fg='bright_white') +  '\n'+ \
				style(text = 'link_on_good: ', bg='white', fg='black') + style(text = self.link_on_good, fg='bright_white') +  '\n'+ \
				style(text = 'article: ', bg='white', fg='black') + style(text = self.article, fg='bright_white') +  '\n'+ \
				style(text = 'name: ', bg='white', fg='black') + style(text = self.name, fg='bright_white') +  '\n'+ \
				style(text = 'description: ', bg='white', fg='black') + style(text = self.description, fg='bright_white') +  '\n'+ \
				style(text = 'price: ', bg='white', fg='black') + style(text = self.price, fg='bright_white') +  '\n'+ \
				style(text = 'pictures: ', bg='white', fg='black') + style(text = self.pictures, fg='bright_white') +  '\n'+ \
				style(text = 'colors: ', bg='white', fg='black') + style(text = self.colors, fg='bright_white') +  '\n'+ \
				style(text = 'sizes: ', bg='white', fg='black') + style(text = self.sizes, fg='bright_white') +  '\n'+ \
				style(text = 'instock: ', bg='white', fg='black') + style(text = self.instock, fg='bright_white')

	def __repr__(self):
		return f'<Student: row_id={self.row_id} catalog="{self.catalog}" link_on_parent_page="{self.link_on_parent_page}" link_on_good="{self.link_on_good}" article="{self.article}" name="{self.name}" description="{self.description}" price="{self.price}" pictures="{self.pictures}" colors="{self.colors}" sizes="{self.sizes}" instock="{self.instock}">'

class DB:
	def __init__(self, p_sqlite_filepath:str):
		self.Session = sessionmaker()
		print(f"sqlite:{p_sqlite_filepath}")
		self.engine = create_engine(f"sqlite:///{p_sqlite_filepath}")
		self.session = self.Session(bind=self.engine)
		Base.metadata.create_all(self.engine)

	# save good into database, not with help object-parameter, but with separated parameters
	def save_good_from_parameter(self, 	catalog='',
										link_on_parent_page='',
										link_on_good='',
										article='',
										name='',
										description='',
										price='',
										pictures='',
										colors='',
										sizes='',
										instock=''):
		foogood = Goods()
		foogood.catalog = catalog
		foogood.link_on_parent_page = link_on_parent_page
		foogood.link_on_good = link_on_good
		foogood.article = article
		foogood.name = name
		foogood.description = description
		foogood.price = price
		foogood.pictures = pictures
		foogood.colors = colors
		foogood.sizes = sizes
		foogood.instock = instock
		self.save_good(foogood)


	# save good into database
	def save_good(self, 
				good:Goods):
		# try to select from base recod by catalog, parent link and link
		work_record = self.session.query(Goods).filter( Goods.catalog == good.catalog, 
														Goods.link_on_parent_page == good.link_on_parent_page,
														Goods.link_on_good==good.link_on_good )
		if work_record.count()!=0:
			echo(style(text='Updated data:', fg='bright_red')+\
				style(text='Link on head link="', fg='bright_yellow')+style(text=good.link_on_parent_page, fg='bright_green')+\
				style(text='" inner link="', fg='bright_yellow')+style(text=good.link_on_good, fg='bright_green')+\
				style(text='" catalog="', fg='bright_yellow')+style(text=good.catalog, fg='bright_green')+\
				style(text='" allready exists in database.', fg='bright_yellow'))
			work_record.update({'article':good.article, 'name':good.name, 'description':good.description,'price':good.price,
								'pictures':good.pictures,'colors':good.colors, 'sizes':good.sizes, 'row_id':good.row_id, 
								'instock':good.instock})
		else:
			echo(style(text='Inserted data:', fg='bright_blue')+\
				style(text='Link on head link="', fg='bright_yellow')+style(text=good.link_on_parent_page, fg='bright_green')+\
				style(text='" inner link="', fg='bright_yellow')+style(text=good.link_on_good, fg='bright_green')+\
				style(text='" catalog="', fg='bright_yellow')+style(text=good.catalog, fg='bright_green')+\
				style(text='" allready exists in database.', fg='bright_yellow'))
			self.session.add(good)
		self.session.commit()

	def get_none_load_goods_by_parent_link(self, catalog:str, parent_link:str):
		print(catalog, parent_link)
		records = self.session.query(Goods.link_on_good).filter(	Goods.catalog == catalog, 
													Goods.link_on_parent_page == parent_link).filter(func.length(Goods.price)==0)
		print(records)
		ll=[]
		for record in records: ll.append(record.link_on_good)
		return ll
		



	def test(self):
		records = self.session.query(Goods.catalog).distinct()
		ll_catalogs = [] # list of unqie catalogs
		for record in records: ll_catalogs.append(record.catalog)
		for catalog in ll_catalogs:
			ll_parents = [] # list of unique parents into catalog
			records = self.session.query(Goods.link_on_parent_page).filter(Goods.catalog==catalog).distinct()
			for record in records: ll_parents.append(record.link_on_parent_page)
			for parent in ll_parents:
				prices = self.session.query(Goods.price).filter(	Goods.catalog==catalog, 
															Goods.link_on_parent_page==parent,
															func.length(Goods.instock)>0,
															cast(Goods.price, Integer)>0).distinct()
				for price in prices.all():
						print()
						rows = self.session.query(Goods).filter(	Goods.catalog==catalog, 
																	Goods.link_on_parent_page==parent,
																	func.length(Goods.instock)>0,
																	Goods.price==price.price).all()
						lc_name, lc_description, lc_price, lc_link, lc_pictures, lc_size, lc_color = '','','','','','',''
						for row in rows:
							lc_name = f'{row.article} {row.name}'
							lc_description = row.description
							lc_price = price.price
							lc_link = parent
							lc_pictures = row.pictures
							lc_size = f'Рост: {row.colors}  Размер: {row.sizes} {row.instock}'
							print(lc_name, lc_description, lc_price, lc_link, lc_pictures, lc_size)

		return False
				#lc_name, lc_description, lc_price, lc_link, lc_pictures, lc_size, lc_color = ''
				#for record in records.all():
				#	echo(record)
				#	lc_name = record.article + ' ' + record.name
				#	lc_description = record.description
					



if True:
	db = DB('g:\\utenok.ru2\\databases\\DataBase.db')
	db.test()
	#db.test()

if False:
	onegood = Goods()
	onegood.row_id = 1
	onegood.catalog = 'catalog_2'
	onegood.link_on_parent_page = 'parent_2'
	onegood.link_on_good = 'link_1'
	onegood.article = 'article_1'
	onegood.name = 'name_1'
	onegood.description = 'description_1'
	onegood.price = '200'
	onegood.pictures = 'pictures_1'
	onegood.colors = 'colors_1'
	onegood.sizes = 'sizes_1'
	echo(onegood)
	db.save_good(onegood)
	print(db.get_none_load_goods_by_parent_link(".\\csvs\\test.csv","""https://utenok.ru/halat-detskiy-ru-16/"""))


