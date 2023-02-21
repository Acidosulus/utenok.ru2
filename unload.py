from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from driver import *
from good import *
import colorama
from colorama import Fore, Back, Style
from click import echo, style
from my_database import DB, Goods


db = DB('g:\\utenok.ru2\\databases\\DataBase.db')
good = Goods()


def unload_one_good(dw:WD, lc_link_on_good: str, pc_price:str , submissive:bool, parent:str):
	lo_good = GoodWD(db, good, dw, lc_link_on_good, pc_price, submissive, parent)
	print(f'{Fore.YELLOW}Название: {Fore.LIGHTGREEN_EX}{lo_good.name}{Fore.RESET}')
	print(f'{Fore.YELLOW}Артикул: {Fore.LIGHTCYAN_EX}{lo_good.article}{Fore.RESET}')
	print(f'{Fore.YELLOW}Цена: {Fore.LIGHTGREEN_EX}{lo_good.price}{Fore.RESET}')
	print(f'{Fore.YELLOW}Описание: {Fore.LIGHTGREEN_EX}{lo_good.description}{Fore.RESET}')
	print(f'{Fore.YELLOW}Картинки: {Fore.LIGHTCYAN_EX}{lo_good.pictures}{Fore.RESET}')
	print(f'{Fore.YELLOW}В наличии: {Fore.LIGHTCYAN_EX}{lo_good.instock}{Fore.RESET}')
	print(f'{Fore.YELLOW}Цвет: {Fore.LIGHTCYAN_EX} {(lo_good.color if len(lo_good.color)>0 else lo_good.colors)} {Fore.RESET}')
	print(f'{Fore.YELLOW}Размер: {Fore.LIGHTCYAN_EX}{lo_good.size}{Fore.RESET}')
	return lo_good


########################################################################################################################
########################################################################################################################
colorama.init()
########################################################################################################################
########################################################################################################################

if sys.argv[1] == 'good':
	wd = Login()
	print(sys.argv[1], sys.argv[2])
	price = Price(sys.argv[3])
	primary_good = unload_one_good(wd, sys.argv[2], sys.argv[3] , False, sys.argv[2])
	list_of_submissives = db.get_none_load_goods_by_parent_link(sys.argv[3], sys.argv[2])
	print(list_of_submissives)
	for submissive_link in list_of_submissives:
		submissive_good = unload_one_good(wd, submissive_link, sys.argv[3], True, sys.argv[2])
	



if sys.argv[1] == 'catalog':
	wd = Login()
	print(sys.argv[1], sys.argv[2], sys.argv[3])
	price = Price(sys.argv[3])
	ll_list_of_goods = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
	ln_total = len(ll_list_of_goods)
	ln_current_link_number = 0
	for link_on_good in ll_list_of_goods:
		ln_current_link_number += 1
		echo(style(text=f'{ln_current_link_number}', bg='blue', fg='bright_yellow') + \
			style(text=f'/{ln_total}', bg='blue', fg='yellow'))
		primary_good = unload_one_good(wd, link_on_good, sys.argv[3] , False, link_on_good)
		list_of_submissives = db.get_none_load_goods_by_parent_link(sys.argv[3], link_on_good)
		print(list_of_submissives)
		for submissive_link in list_of_submissives:
			submissive_good = unload_one_good(wd, submissive_link, sys.argv[3], True, sys.argv[2])

if sys.argv[1] == 'reverse':
	reverse_csv_price(sys.argv[2])

if sys.argv[1] == 'ansi':
	convert_file_to_ansi(sys.argv[2] + '_reversed.csv')

#try: wd.driver.quit()
#except: pass