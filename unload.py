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
    links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
    print('Список товаров:', links_list)
    ln_total = len(links_list)
    ln_counter = 0
    price = Price(sys.argv[3])
    for link in links_list:
        ln_counter += 1
        echo(style(f'{ln_counter}/{len(links_list)}', fg='bright_blue'))
        if is_price_have_link(sys.argv[3], link):
            print('Товар уже имеется в прайсе')
            echo(style('Товар уже имеется в прайсе', fg='bright_red'))
            continue
        lo_good = unload_one_good(wd, link, sys.argv[3], False) # <= don't forget remake last parameter
        lc_name = lo_good.name if lo_good.name.count(lo_good.article) != 0 else lo_good.article + ' ' + lo_good.name
        #if 'Под заказ' in lo_good.description:
        #    echo(style('Под заказ', fg='bright_red'))
        #    continue
        ll_unique = list(set(lo_good.prices))
        print('Уникальные цены: ', ll_unique)
        if len(lo_good.prices) != len(lo_good.sizes):
            print('Несоответствие количества цен и количества товаров, пропуск.')
            continue
        for lc_uprice  in ll_unique:
            j = 0
            ll_sizes = []
            ll_prices = []
            for lc_price in lo_good.prices:
                if lo_good.prices[j] == lc_uprice:
                    try:
                        ll_sizes.append(lo_good.sizes[j])
                    except:pass
                j = j + 1
            price.add_good('',
                                prepare_str(lc_name),
                                prepare_str(lo_good.description),
                                prepare_str( str(round(float(lc_uprice.replace(',', '.').replace(' ', ''))*(1 if lo_good.sale else float(sys.argv[4])), 2))),
                                '15',
                                prepare_str(link),
                                prepare_for_csv_non_list(lo_good.pictures),
                                (prepare_str(lo_good.color) if len(lo_good.color)>0 else prepare_for_csv_list(lo_good.colors)),
                                prepare_for_csv_list(ll_sizes))
            price.write_to_csv(sys.argv[3])

if sys.argv[1] == 'reverse':
    reverse_csv_price(sys.argv[2])

if sys.argv[1] == 'ansi':
    convert_file_to_ansi(sys.argv[2] + '_reversed.csv')

#try: wd.driver.quit()
#except: pass