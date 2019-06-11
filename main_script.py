from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
#import pandas as pd
import os
import json
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time



#Add option for headless browsing


appName = 'not set'
searching = True

def startUp():
    print("\n\t\t\t************************* WELCOME ****************************\n")
    
def getAppName():
    tempAppName = input('\nEnter the app name: ' )
    #tempAppName = tempAppName.replace(" ","") #remove spaces from the input
    #can use strip() also

    tempAppName = " ".join(tempAppName.split()) #remove spaces from the input from leading and ending

    if not tempAppName:
        #input is empty
        print("\nInvalid input! Please enter a valid input !")
        getAppName() #recall the method to get a valid input
       
    else:
        global appName #update the global variable
        appName = tempAppName #assign the value to global var
        searchConfirm()
   

def searchConfirm():
    searchConfirm = input("\nStart the searching ? (Y/N) :")
    searchConfirm = searchConfirm.replace(" ","")

    if (searchConfirm == "Y") | (searchConfirm == "y") :
        print("\nSearching...")
        #time.sleep(6)
        searchingTheAppList()

    else:
        getAppName()


def searchingTheAppList():

    url = "https://play.google.com/store/apps"

    options = FirefoxOptions()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.implicitly_wait(30)
    driver.get(url)

    driver.find_element_by_id("gbqfq").send_keys(appName) #find the search box and fill the box with the app name

    #searchBtn = driver.find_element_by_id("gbqfb") #find the search button
    #driver.execute_script('arguments[0].click()', searchBtn)

    driver.find_element_by_id("gbqfb").click()

    soup_level=BeautifulSoup(driver.page_source, 'lxml')

    mainAppList = soup_level.find_all("div",attrs={"class","Vpfmgd"})

    print("found : "+str(len(mainAppList)))

    for i,item in enumerate(mainAppList):
        if(i < 11) :
            appTitle = item.find("div",attrs={"class","b8cIId ReQCgd Q9MA7b"})
            titleText = appTitle.get_text()
            print("\t\t"+str(i+1)+" "+titleText+"\n")







startUp()
getAppName()
