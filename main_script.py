from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
#import pandas as pd
import os
import json
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import urllib3

#Add option for headless browsing

appName = 'not set'
searching = True
appDataLinkList = []

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)

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
        #searchingTheAppList()
        getData()

    else:
        getAppName()


def searchingTheAppList():
    #this method is not working properly

    url = "https://play.google.com/store/apps"

   
    driver.get(url)

    print("\n\t tittle: "+driver.title+" "+driver.current_url)

    driver.find_element_by_id("gbqfq").send_keys(appName) #find the search box and fill the box with the app name

    driver.find_element_by_id("gbqfb").click()


    try:
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME,"K2pK9")))

    except (TimeoutException,NoSuchElementException) as e:
        print("\nElement not found " )

        print("\n\t tittle: "+driver.title+" "+driver.current_url)

        soup=BeautifulSoup(driver.page_source, 'lxml')

        mainAppList = soup.find_all("div",attrs={"class","Vpfmgd"})

        for i,item in enumerate(mainAppList):
            if(i < 10) :
                appTitle = item.find("div",attrs={"class","b8cIId ReQCgd Q9MA7b"})
                titleText = appTitle.get_text()
                print("\t\t"+str(i+1)+" "+titleText)


def getData():
    #create the url and get the data
    #print("This is the app name: "+appName)

    updatedAppName = appName.replace(" ","%20")

    createdUrl = "https://play.google.com/store/search?q="+updatedAppName+"&c=apps"

    #print("New text : "+updatedAppName)
    #print("new url : "+createdUrl)

    driver.get(createdUrl)

    soup=BeautifulSoup(driver.page_source, 'lxml')

    mainAppList = soup.find_all("div",attrs={"class","Vpfmgd"})

    for i,item in enumerate(mainAppList):
        if(i < 15) :
            appTitle = item.find("div",attrs={"class","b8cIId ReQCgd Q9MA7b"})

            titleText = appTitle.get_text()
            url = appTitle.find("a")
            dataUrl = "https://play.google.com"+url['href']

            appDataLinkList.append(dataUrl)

            print("\t "+str(i+1)+" "+titleText)

    validateTheSelectedIndex()

def validateTheSelectedIndex () :

    selectedIndex = input("\nEnter the index of the item you want to view : ")

    if(int(selectedIndex) < 1) | (int(selectedIndex) > 10):
        print("Invalid index. Please enter a valid index.")
        validateTheSelectedIndex()
    else:
        viewSelectedAppData(link = appDataLinkList[(int(selectedIndex)-1)])


def viewSelectedAppData(link):

    spanClassList =["L2o20d P41RMc","L2o20d tpbQF","L2o20d Sthl9e","L2o20d rhCabb","L2o20d A3ihhc"]

    driver.get(link)#go to the new link

    soupSub=BeautifulSoup(driver.page_source, 'lxml')

    mainDataDiv = soupSub.find("div",attrs={"class","sIskre"})
    mainTitle = mainDataDiv.find("h1",attrs={"class","AHFaub"})
    developerName = mainDataDiv.find("a",attrs={"class","hrTbp R8zArc"})
    totalRatings = mainDataDiv.find("span",attrs={"class","AYi5wd TBRnV"})

    descripList = soupSub.find_all("div",attrs={"class","IQ1z0d"})#GET IMPORTANT DATA

    ratingTotal = soupSub.find("div",attrs={"class","BHMmbe"})
    ratingsList = soupSub.find_all("div",attrs={"class","mMF0fd"})

    print("\n\t NAME : "+mainTitle.get_text())
    print("\t DEVELOPED BY : "+developerName.get_text())
    print("\t TOTAL DOWNLOADS : "+descripList[4].get_text())
    print("\t VIEW IN PLAYSTORE : "+link)

    print("\n\t\t\t -------------- REVIEWS -------------- \n")
    print("\t RATING : "+ratingTotal.get_text())
    print("\t TOTAL REVIEWS : "+totalRatings.get_text()+"\n")

    for i,item in enumerate(ratingsList):
        rateNum = item.find("span",attrs={"class","Gn2mNd"}).get_text()
        rate = item.find("span",attrs={"class",spanClassList[i]})['style']
        updatedText = str(rate).replace("width:","")

        print("\t\t"+rateNum+" --------"+updatedText)

    print("\n\t\t\t ------------- DESCRIPTION -------------\n")

    print("\t CURRENT VERSION : "+descripList[5].get_text())
    print("\t SIZE : "+descripList[3].get_text())
    print("\t TOTAL DOWNLOADS : "+descripList[4].get_text())
    print("\t REQUIRES ANDROID : "+descripList[6].get_text())


startUp()
getAppName()
