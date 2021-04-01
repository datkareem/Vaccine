## Vaccine_Finder
## Creator: Kareem T
## Purpose: Notifiesuser at the next availability in local covid vaccinations
## 4/1/21
##
## Requirements: selenium (module),  plyer (module), chromedriver. pip install / download accordingly
## Note: Edit paths for chromedriver and app_icon according to your storage location. Edit desired zips accordingly
## Intended OS: Windows 10............Make sure notifications are not silenced. This can be checked in the action center in the bottom right corner

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from plyer import notification
import time

chromedriver_path = ""
icon_path = ""
area_codes = ["", ""]

options = webdriver.ChromeOptions() #impliments option below. optional
options.add_experimental_option('excludeSwitches', ['enable-logging']) #extra option to avoid meaningless errors at intialization of script. optional
driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)

num_zips = len(area_codes)
zip_code = 0
INDEX = 0

url = 'https://www.mhealthappointments.com/covidappt'
list_id = '//*[@id="covid_vaccine_store_list_content"]' #list of vax sites and their associated availability. parsing the list impliments adaptability on any zipcode


def init_website():
    driver.get(url)
    mile_selection = driver.find_element_by_xpath('//*[@id="fifteenMile-covid_vaccine_search"]') #selects 15 mile radius
    mile_selection.click()

def switch_zip():
    global INDEX
    global zip_code
    INDEX +=1
    if INDEX == num_zips: INDEX = 0 #portability to allow any number of zips. resets to index 0 when index outside of zip list range
    zip_code = area_codes[INDEX]

def enter_zip():
    switch_zip()
    search_bar = driver.find_element_by_id("covid_vaccine_search_input")
    search_bar.clear()
    search_bar.click()
    search_bar.send_keys(zip_code)
    
    search = driver.find_element_by_xpath('//*[@id="covid_vaccine_search"]/div[1]/div[2]/button')
    search.click()


def check_appts():
    raw_list = driver.find_element_by_xpath(list_id) #returns string of sites, each of which is followed by a availability. all information is split by newline
    split_list = raw_list.text.split('\n') #splits sites, availabilities, returns a list
    availabilities = split_list[1::2] #clones the list at every even position to extract only availabilites
    for site in availabilities:
        if site != 'No':
            notification.notify(title="Appointment Available", message=f"Vaccination available at {zip_code}", app_icon=icon_path, timeout=10)


def main():
    init_website()
    driver.minimize_window()
    time.sleep(3)
    while(True):
        enter_zip()
        time.sleep(3)
        check_appts()

if __name__ == "__main__":
    main()