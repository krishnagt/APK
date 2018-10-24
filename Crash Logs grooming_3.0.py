#required files/drivers to be imported
import sys
import time
import datetime
import re
import lxml.html
import os
import shutil
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#mention your username
from selenium.webdriver.support.wait import WebDriverWait

usernameStr = 'apps.philipscl.admin@philips.com'

#after installing the webdriver copy/paste it in the path
#path : usr->local->bin(ubuntu)...maybe different for any other OS.

driver = webdriver.Chrome("/Users/mobileopsblr/Downloads/chromedriver")

# get the current script path.
# here = os.path.dirname(os.path.dirname(__file__))
# Updated the details for windows and Mac/Linux
here = os.path.dirname(os.path.abspath(__file__))
print here
directoryname = 'new'

#specify the URL/specify as parameter/automate...
applinkdeafault = 'https://play.google.com/apps/publish/?account=6760026048432774867'

#Link for the current apps needed for the crash logs reporting
applink = 'https://play.google.com/apps/publish/?account=6760026048432774867#AndroidMetricsErrorsPlace:p='

#All the package id and app id for all the apps -temp 'com.philips.cdp.ohc.tuscany&appid=4972538560402061575',
# 'com.philips.sonicare4kids&appid=4973179805281087130',
#              'com.philips.platform.lumea&appid=4974925465408706761','com.philips.cl.di.figaro&appid=4976268014315616634',
#              'com.philips.cl.di.ka.healthydrinks&appid=4971991141682234909','com.philips.cl.di.kitchenappliances.airfryer&appid=4976153891569046378',
#              'com.philips.moonshot&appid=4973254935345609721','com.philips.src.hss&appid=4976038501092548013',
#              'com.philips.cl.uGrowDigitalParentingPlatform&appid=4976349220016227826'

# Grooming: Shave & Styling
packageid = 'com.philips.cl.di.figaro&appid=4976268014315616634'

appversion = '&appVersion=PRODUCTION'

#For 30 days report
numberofdays = '&lastReportedRange=LAST_30_DAYS'

driver.get('https://www.google.com/accounts/DisplayUnlockCaptcha')

#Automate the process of logging into google
#Login to the Google Play Store
username = driver.find_element_by_id('identifierId')
username.send_keys(usernameStr)
nextButton = driver.find_element_by_id('identifierNext')
nextButton.click()
time.sleep(2)
driver.find_element_by_xpath(".//*[@type='password']").send_keys("CL@dmin15")
driver.find_element_by_xpath(".//*[@id='passwordNext']").click()
time.sleep(5)

driver.get(applink + packageid + appversion + numberofdays)
time.sleep(10)
#get total number of crashes and pages for a given app
# totalpages = str('1')
# driver.get(applink + packageid + appversion + numberofdays)
# time.sleep(7)

#date time filter
mydate = datetime.datetime.now()
#for running it for a month before - problem is we cannot run this in current month
#example: if you run in aug 1 then it will run for complete July but in between will not run
previous_month = mydate.month - 1
prev_month_name = datetime.date(mydate.year, previous_month, mydate.month).strftime('%b')

currentmonth = mydate.strftime("%b")
filtermonth = [prev_month_name,currentmonth, 'Today','Yesterday','Now', 'minutes','ago']

tree = lxml.html.fromstring(driver.page_source)
final1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[7]/div[1]/div/text()')
if(str(final1).__contains__("clusters")):
    totalcrashes = str(final1).strip('[]').strip("''").replace("crash", "").replace("clusters", "").replace(" ", "")
else:
    totalcrashes = str(final1).strip('[]').strip("''").replace("crash", "").replace("cluster", "").replace(" ", "")

if totalcrashes == str('0'):
    totalpages = '0'
    print("Sorry, NO Crash Logs Available")

elif totalcrashes == str(''):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
    nextButton = driver.find_element_by_xpath('//button[@aria-label="Next page"]')
    while nextButton.is_enabled():
        nextButton.click()
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(2)
    #time.sleep(2)
    tree = lxml.html.fromstring(driver.page_source)
#    final1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[7]/div[1]/div/text()')
    final1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div/section/div[8]/div[1]/div/text()')
    totalcrashes = str(final1).strip('[]').strip("''").replace("crash", "").replace("clusters", "").replace(" ", "")
    # if(totalcrashes != str('')):
    #     final2 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/section/div/div/div/span[1]/strong[2]/text()')
    #     totalpages = str(final2).strip('[]').strip("''").replace(" ", "")


#total number of crashes and rows now found
if(totalcrashes!=str('0')):
    #Re-direct the Webpage to the Application crash log page
    driver.refresh()
    time.sleep(7)
    rows = 0

    tree = lxml.html.fromstring(driver.page_source)

    # getting the name of the app
    name = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/header/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/text()')
    appname = str(name).strip('[]').strip("''").replace(": ","-")
    print("Crash Logs for: "+appname)

    tc = int(totalcrashes)
    #storing in folder
    directoryname = appname+'_'+prev_month_name+'- 2018'
    #check if the directory is already existing
    if (os.path.isdir(os.path.join(here, directoryname))):
        print "Crash log folder already exits"
    else:
        #Updated the below to work seemlessly for windows and Mac/Linux
        dirnew = here + os.sep + directoryname
        os.mkdir(dirnew)
        #os.mkdir(os.path.join(here, directoryname))

    os.chdir(os.path.join(here, directoryname))

    #iterating through the pages
    for i in range(tc):
        rows = rows + 1

        if rows%26 == 0:
            rows=1
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
            time.sleep(1)
            # Jump to Page i+1
            nextButton = driver.find_element_by_xpath('//button[@aria-label="Next page"]')
            nextButton.click()
            time.sleep(5)
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+Keys.HOME)

        time.sleep(2)
        tree = lxml.html.fromstring(driver.page_source)

#        final = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[7]/div[1]/div/text()')
#        #Crash on the page
#        element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/section/div/table/tbody[1]/tr['+str(rows)+']/td[1]/div/div')
        final = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[7]/div[1]/div/text()')
        #Crash on the page
        element = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div/section/section/div/table/tbody[1]/tr['+str(rows)+']/td[1]/div/div')
        element.click()
        #time.sleep(2)

        counter = 0
        flagcounter = 6
        nl = "\n\n"
        #Getting internal crash log begins here
        while True:

            #time break given so that the required page can be loaded... time depends upon the connection speed
            time.sleep(1)
            driver.current_url
            #Scroll down
            if counter == 0:
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
                time.sleep(1)

            tree = lxml.html.fromstring(driver.page_source)
            #specify the xpath of the content to be scraped
            # results1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[5]/div/section/div[1]/div[1]/h3/div/text()')
            results1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/section/div[5]/div/section/div[1]/div[1]/h3/div/text()')
            
            # results2 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[5]/div/section/div[1]/div[1]/div//text()')
            results2 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/section/div[5]/div/section/div[1]/div[1]/div//text()')
            
            #results3 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[5]/div/section/div[3]/div/div//text()')
            results3 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/section/div[5]/div/section/div[3]/div/div//text()')
            #count the 'number' of sub-reports
            #num1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[5]/div/section/div[1]/div[2]/span[1]/strong[1]/text()')
            num1 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/section/div[5]/div/section/div[1]/div[2]/span[1]/strong[1]/text()')
            
            #num2 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/section/div[5]/div/section/div[1]/div[2]/span[1]/strong[2]/text()')
            num2 = tree.xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/section/div[5]/div/section/div[1]/div[2]/span[1]/strong[2]/text()')

            counter=counter+1
            print(counter)

            # Strip and get the current month without the number
            clt = str(results1).strip('[]').strip("''").split(",")[0]
            currentlogtime = re.sub(r' \d+', '', clt)
            print currentlogtime

            # patterns = ['software testing', 'guru99']
            # text = 'software testing is fun?'
            # for pattern in patterns:
            #     print('Looking for "%s" in "%s" ->' % (pattern, text))
            #     if re.search(pattern, text):
            #         print('found a match!')
            # else:
            #     print('no match')

            #Update check for filter - time
            match = 0
            for pattern in filtermonth:
                if re.search(pattern, currentlogtime):
                    match = 1
                    break



            #if (currentlogtime not in filtermonth or not(re.search(filtermonth, currentlogtime))):

            #updated condition to check if logs are completed or not
            if(match == 0):
                #str(counter)== str('2')
                print("COMPLETED REPORT "+str(i+1))
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(2)
                backbutton = driver.find_element_by_xpath('//button[@aria-label="Back"]')
                backbutton.click()
                #time.sleep(3)
                break

            #printing into the file
            with open(str(name).strip('[]').strip("''")+" "+str(i+1), "a") as output:
            #with open("h.txt", "a") as output:
                output.write("SUB-REPORT : "+str(counter))
                output.writelines(nl)
                output.write("TIME : ")
                output.write(str(results1).strip('[]').strip("''"))
                output.writelines(nl)
                output.write("DEVICE : ")
                output.write(str(results2).strip('[]'))
                output.writelines(nl)
                output.write("CRASH LOGS : ")
                output.writelines(nl)
                output.write(str(results3).replace("' ', ","").strip('[]').replace(": ","").replace("' '","").replace("''","").replace(",","\n"))
                output.writelines(nl)
                output.write("----------------------------------------------------------------")
                output.writelines(nl)

            if (str(num1).strip('[]').strip("''") == str(num2).strip('[]').strip("''")):
                #str(counter)== str('2')
                if (str(currentlogtime).find("minutes") == -1):
                    print("COMPLETED REPORT "+str(i+1))
                    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                    time.sleep(2)
                    backbutton = driver.find_element_by_xpath('//button[@aria-label="Back"]')
                    backbutton.click()
                    #time.sleep(3)
                    break

            try:
                element_present = EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Next page"]'))
                WebDriverWait(driver, 2).until(element_present)
                # Click the next logs internally within the given crash logs
                #Add condition to take only current month logs
                nextButton2 = driver.find_element_by_xpath('//button[@aria-label="Next page"]')
                nextButton2.click()
            except TimeoutException:
                print "Timed out waiting for page to load"

            # take care of load after every 5 logs
            if counter == flagcounter:
                time.sleep(2)
                flagcounter = flagcounter+5

    print("REPORT DOWNLOAD COMPLETE")

    print("Creating Zip file for the report...")
    # creating zip folder for crash logs
    os.chdir("..")
    #shutil.make_archive(output_filename, 'zip', dir_name)
    shutil.make_archive(directoryname,'zip',os.path.join(here, directoryname))
    #time.sleep(5)
    print("REPORT IS NOW READY TO MAIL")

#closing the web browser
webdriver.Chrome.close(driver)
