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
import colorama
from colorama import init,Fore, Back, Style, AnsiToWin32
import sys
import textwrap


#Add option for headless browsing

appName = 'not set'
searching = True
appDataLinkList = []

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)

init(convert=True)
init(wrap=False)

stream = AnsiToWin32(sys.stderr).stream

def startUp():

    print(Fore.LIGHTCYAN_EX+"\n\t\t\t|                                                               |"+
        "\n\t\t\t| ************************* WELCOME *************************** | "+
            "\n\t\t\t| ______________________________________________________________|\n\n"+Style.RESET_ALL)

    
def getAppName():

    tempAppName = input(' Enter the app name: ')

    #tempAppName = tempAppName.replace(" ","") #remove spaces from the input
    #can use strip() also

    tempAppName = " ".join(tempAppName.split()) #remove spaces from the input from leading and ending

    if not tempAppName:
        #input is empty
        print(Fore.RED + "\n Invalid input! Please enter a valid input !",file=stream)
        print(Style.RESET_ALL)
        getAppName() #recall the method to get a valid input
       
    else:
        global appName #update the global variable
        appName = tempAppName #assign the value to global var
        searchConfirm()
   

def searchConfirm():
    searchConfirm = input("\n Start the searching ? (Y/N) :")
    searchConfirm = searchConfirm.replace(" ","")

    if (searchConfirm == "Y") | (searchConfirm == "y") :
        print(Fore.LIGHTBLUE_EX+"\n Searching...",file=stream)
        print(Style.RESET_ALL)
        #time.sleep(6)
        #searchingTheAppList()
        getData()

    else:
        getAppName()


def searchingTheAppList():
    #this method is not working properly

    url = "https://play.google.com/store/apps"

   
    driver.get(url)

    #print("\n\t tittle: "+driver.title+" "+driver.current_url)

    driver.find_element_by_id("gbqfq").send_keys(appName) #find the search box and fill the box with the app name

    driver.find_element_by_id("gbqfb").click()


    try:
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME,"K2pK9")))

    except (TimeoutException,NoSuchElementException) as e:
        print("\nElement not found " )

        #print("\n\t tittle: "+driver.title+" "+driver.current_url)

        soup=BeautifulSoup(driver.page_source, 'lxml')

        mainAppList = soup.find_all("div",attrs={"class","Vpfmgd"})

        for i,item in enumerate(mainAppList):
            if(i < 10) :
                appTitle = item.find("div",attrs={"class","b8cIId ReQCgd Q9MA7b"})
                titleText = appTitle.get_text()
                print("\t\t"+Fore.GREEN+str(i+1)+" "+titleText,file=stream)
                print(Style.RESET_ALL)


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

            print("\t  "+Fore.LIGHTCYAN_EX+"("+str(i+1)+")"+Fore.LIGHTWHITE_EX+" "+titleText,file=stream)

    validateTheSelectedIndex()

def validateTheSelectedIndex () :

    print(Style.RESET_ALL)
    selectedIndex = input(" Enter the index of the item you want to view : ")

    try:
        if(int(selectedIndex) < 1) | (int(selectedIndex) > 15):
            print(Fore.RED+" Invalid index. Please enter a valid index.",file=stream)
            print(Style.RESET_ALL)
            validateTheSelectedIndex()
        else:
            viewSelectedAppData(link = appDataLinkList[(int(selectedIndex)-1)])

    except:
        print(Fore.RED+" Invalid index. Please enter a valid index.",file=stream)
        print(Style.RESET_ALL)
        validateTheSelectedIndex()

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

    print(Fore.LIGHTCYAN_EX+"\n\t _________________________________________ ABOUT _______________________________________ \n\n",file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  NAME : "+Fore.LIGHTMAGENTA_EX+mainTitle.get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  DEVELOPED BY : "+Fore.LIGHTYELLOW_EX+developerName.get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  TOTAL DOWNLOADS : "+Fore.LIGHTRED_EX+descripList[4].get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  VIEW IN PLAYSTORE : "+Fore.LIGHTGREEN_EX+link,file=stream)

    #Reviews section
    print(Fore.LIGHTCYAN_EX+"\n\t ________________________________________ REVIEWS ______________________________________ \n\n",file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  RATING : "+Fore.LIGHTYELLOW_EX+ratingTotal.get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  TOTAL REVIEWS : "+Fore.LIGHTYELLOW_EX+totalRatings.get_text()+"\n",file=stream)

    colorList = [Fore.LIGHTGREEN_EX,Fore.LIGHTYELLOW_EX,Fore.LIGHTMAGENTA_EX,Fore.LIGHTBLUE_EX,Fore.LIGHTRED_EX]

    for i,item in enumerate(ratingsList):
        rateNum = item.find("span",attrs={"class","Gn2mNd"}).get_text()
        rate = item.find("span",attrs={"class",spanClassList[i]})['style']
        updatedText = str(rate).replace("width:","")

        print(colorList[i]+"\t\t   "+rateNum+Fore.LIGHTWHITE_EX+" -------->"+colorList[i]+updatedText,file=stream)

    #Description section
    print(Fore.LIGHTCYAN_EX+"\n\t ______________________________________ DESCRIPTION _____________________________________ \n\n",file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  CURRENT VERSION : "+Fore.LIGHTBLACK_EX+descripList[5].get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  SIZE : "+Fore.LIGHTGREEN_EX+descripList[3].get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  TOTAL DOWNLOADS : "+Fore.LIGHTBLUE_EX+descripList[4].get_text(),file=stream)
    print(Fore.LIGHTWHITE_EX+"\t  REQUIRES ANDROID : "+Fore.LIGHTRED_EX+descripList[6].get_text(),file=stream)

    #Find the top comments
    print(Fore.LIGHTCYAN_EX+"\n\t ______________________________________ TOP COMMENTS _____________________________________ \n\n",file=stream)

    commentsSections = soupSub.find_all("div",attrs={"class","d15Mdf bAhLNe"})

    for i,item in enumerate(commentsSections):
        commentatorName = item.find("span",attrs={"class","X43Kjb"})
        commentedDate = item.find("span",attrs={"class","p2TkOb"})
        comment = item.find("div",attrs={"class","UD7Dzf"})

        print("\t "+Fore.WHITE+str(i+1)+") "+Fore.GREEN+commentatorName.get_text()+"\n\t    "+Fore.CYAN+commentedDate.get_text())

        commentText = comment.get_text()

        splitetdText = commentText.split("...Full Review",1)[1]#splitting text from "...Full Review" to avoid repeating text

        dedented_text = textwrap.dedent(str(splitetdText)).strip()
        formatted_para = textwrap.fill(dedented_text, width=90)
        print("\n "+Fore.LIGHTWHITE_EX+textwrap.indent(formatted_para,"\t    ")+"\n")

    
    driver.quit()
        
startUp()
getAppName()
 