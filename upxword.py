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

while True:

    # 1 - São francisco
    # 3 - mahatan
    # 11 - cleveland

    cidades = [1, 3, 4, 5 ,6, 7, 8, 9, 10, 11]
    # cidades= [11]
    for city in cidades:
        # print(city)
        # db = pymysql.connect(db='uplandbot', user='root', passwd='t0c4d0c03lh0')
        
        db = pymysql.connect(host='rodrigosevero.com.br',
                                    user='sist8335_uplandbot',
                                    password='t0c4d0c03lh0',
                                    db='sist8335_uplandbot',
                                    charset='utf8mb4')
        cursor = db.cursor()
        try:
            driver.get("https://upx.world/bigdata?city="+str(city) +"&sort=sale_price_upx&status=ForSaleUpx")
            time.sleep(5)
        
            table = driver.find_element_by_xpath('//table/tbody')
            table = driver.page_source
            soup = BeautifulSoup(table, 'html.parser')

            tbody = soup.find('tbody')
            if (tbody):
                # print(tbody)
                contador_tr = 1
                for tr in tbody.find_all('tr'):
                    if (contador_tr == 1):

                        try:

                            address = tr.find_all('td')[1].text
                            cidade = tr.find_all('td')[2].text
                            neighborhood = tr.find_all('td')[3].text
                            mint_price = tr.find_all('td')[4].text
                            mint_price = mint_price.strip()
                            upx_price = tr.find_all('td')[12].text
                            upx_price = upx_price.strip()
                            upx_price = upx_price.replace(",", "")
                            upx_price_int = int(upx_price)
                            # upx_price = "{:0,.3f}".format(float(upx_price))
                            dono = tr.find_all('td')[16].text
                            dono = dono.strip()
                            link = tr.find_all('a')[1]
                            url = link.get('href')

                            print("Cidade: "+str(cidade)+"...")
                            print()

                            sql = "SELECT * FROM historico where city = '" + str(city)+"' and url = '" + str(url) + "' and owner = '"+str(dono)+"' order by id desc limit 1"
                            cursor.execute(sql)
                            total = cursor.rowcount

                            if total == 0:

                                sql1 = "SELECT * FROM historico where city =  " + str(city)+" order by id desc limit 1"
                                cursor.execute(sql1)
                                result = cursor.fetchone()
                                
                                try:                                    
                                    upx_price_anterior = str(result[2])
                                    upx_price_anterior = upx_price_anterior.replace(",", "")
                                    upx_price_anterior_int = int(upx_price_anterior)
                                    diferenca = int(upx_price_int) - int(upx_price_anterior_int)
                                    mensagem = "Cidade: "+cidade + " \nEndereço: "+address+" \nBairro: "+str(neighborhood)+" \nProprietário: "+str(dono)+" \nUPX price: "+str(upx_price)+" \nUPX price anterior: "+str(upx_price_anterior)+" \nDiferença: "+str(diferenca)+"upx \nURL: "+str(url)
                                    # upx_price_anterior = "{:0,.3f}".format(float(upx_price_anterior))
                                    
                                except:
                                    mensagem = "Cidade: "+cidade + " \nEndereço: "+address+" \nBairro: "+str(neighborhood)+" \nProprietário: "+str(dono)+" \nUPX price: "+str(upx_price)+"upx \nURL: "+str(url)

                                print(mensagem)
                                sql = "insert into historico (url,upx_price,cidade,city,owner) values ('" + str(
                                    url)+"','" + str(upx_price)+"','" + str(cidade)+"','" + str(city)+"','" + str(dono)+"')"
                                # try:
                                cursor.execute(sql)
                                db.commit()
                                # except:
                                #     db.rollback()
                                if (diferenca < 0):
                                    db.close()
                                    telebot = 'https://api.telegram.org/bot1215986907:AAHgu6k55tmHXIPdrQAdh55ADPtiKTieds8/sendMessage?parse_mode=HTML&chat_id=@uplandbotbr&text='+mensagem
                                    requests.get(telebot)
                                print("-------")
                            contador_tr += 1
                            else:
                                print()
                            
                        except:
                            pass
            # print("fim")?
        except:
            pass
    # driver.close()
    # sys.exit()
    time.sleep(1)