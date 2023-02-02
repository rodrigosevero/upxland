# !/usr/bin/python
# encoding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import pymysql
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time
import sys

driver = None
cpath = "/usr/bin/chromedriver"
# while True:

driver = webdriver.Chrome(cpath)

driver.get("https://upxland.me/properties?sort_by=sale_price&status=sale_upx")
time.sleep(10)

cont = 1
while True:
    print()
    print("--- " + str(cont) +" ----")

    # 1 - São francisco
    # 3 - mahatan
    # 11 - cleveland

    # cidades = [1, 3, 4, 5 ,6, 7, 8, 9, 10, 11]
    # cidades = [51] #buenos aires
    # cidades = [38] #lisboa
    cidades = [9] #lisboa
    # cidades = [36] #rio de janeiro
    for city in cidades:
        # print(city)
        # db = pymysql.connect(db='uplandbot', user='root', passwd='t0c4d0c03lh0')

        db = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='t0c4d0c03lh0',
                             db='upxland',
                             charset='utf8mb4')
        cursor = db.cursor()
        try:
            driver.get(
                "https://upxland.me/properties?sort_by=sale_price&status=sale_upx&city_id="+str(city) + "")
            time.sleep(5)

            # table = driver.find_element_by_xpath('table')
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')

            tbody = soup.find('tbody')
            if (tbody):
                print(tbody)
                contador_tr = 1
                for tr in tbody.find_all('tr'):
                    if (contador_tr == 1):

                        

                        address = tr.find_all('td')[0].text
                        cidade = tr.find_all('td')[1].text
                        neighborhood = tr.find_all('td')[2].text
                        mint_price = tr.find_all('td')[4].text
                        mint_price = mint_price.strip()
                        upx_price = tr.find_all('td')[9].text
                        upx_price = upx_price.lstrip()
                        upx_price = upx_price.replace(".", "")
                        upx_price_int = int(upx_price)
                        owner = tr.find_all('td')[13].text
                        link = tr.find_all('a')[2]
                        url = link.get('href')

                        print(address.lstrip)
                        print(cidade)
                        print(neighborhood)
                        print(mint_price)
                        print(upx_price_int)
                        print(owner)
                        print(url)

                        sql = "SELECT * FROM historico where city = '" + \
                            str(city)+"' and url = '" + str(url) + \
                            "' and owner = '" + \
                            str(owner)+"' order by id desc limit 1"
                        cursor.execute(sql)
                        total = cursor.rowcount

                        if total == 0:

                            #
                            sql1 = "SELECT * FROM historico where city =  " + str(city)+" order by id desc limit 1"
                            cursor.execute(sql1)
                            result = cursor.fetchone()
                            print(result)

                            try:
                                upx_price_anterior = str(result[2])                                                             
                                diferenca = upx_price_int - int(upx_price_anterior)
                                mensagem = "Cidade: "+cidade + " \nBairro: "+str(neighborhood)+" \nProprietário: "+str(owner)+" \nUPX price: "+str(upx_price)+" \nUPX price anterior: "+str(upx_price_anterior)+" \nDiferença: "+str(diferenca)+"upx \nURL: "+str(url)                                
                            except:
                                mensagem = "Cidade: "+cidade + " \nBairro: "+str(neighborhood)+" \nProprietário: "+str(owner)+" \nUPX price: "+str(upx_price)+" \nUPX price anterior: "+str(upx_price_anterior)+" \nDiferença: "+str(diferenca)+"upx \nURL: "+str(url)
                                                                                  
                            print(mensagem)

                            sql = "insert into historico (url,upx_price,cidade,city,owner) values ('" + str(
                                    url)+"','" + str(upx_price)+"','" + str(cidade)+"','" + str(city)+"','" + str(owner)+"')"                            
                            cursor.execute(sql)
                            db.commit()
                            
                            if (diferenca < 0):
                                    db.close()
                                    telebot = 'https://api.telegram.org/bot1215986907:AAHgu6k55tmHXIPdrQAdh55ADPtiKTieds8/sendMessage?parse_mode=HTML&chat_id=@uplandbotbr&text='+mensagem
                                    requests.get(telebot)
                        
                        contador_tr += 1

        except:
            pass
    cont += 1
    # driver.close()
    # sys.exit()
    time.sleep(1)
