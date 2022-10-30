import json
import copy
import pandas as p
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
def main():
    jsonList = []
    website = 'http://www.dexel.co.uk'
    browser.get(website)

    Input()
    scrape(jsonList, website)
    SaveFiles(jsonList)

def Input():

    exit_ = False
    keepSearching = True
    width_url = ""
    ratio_url = ""
    rim_url = ""
    while keepSearching:

        #Width searching start
        widthSearch = True
        while widthSearch:
            try:
                widths = []
                answer = ""
                widthselect = Select(browser.find_element("id","tyrewidthselect"))
                widthoptions = widthselect.options
                for option in widthoptions: widths.append(option.get_attribute("value"))
                widths.pop(0)

                for i, value in enumerate(widths):
                    print(str(i+1) + ") " + str(value))

                width = int(input("Please select your width using its listed number: "))
                print("Width selected: " + str(widths[width-1]))
                widthselect.select_by_index(width)
                width_url = str(widths[width-1])
                widthSearch = False
            except:
                answer = str(input("That option isn't available. Do you you wish to continue? Y/N: "))
            if answer.lower() == 'n': break
        
        if widthSearch:
            keepSearching = False
            exit_ = True
            break
        #Width searching end
        


        #Aspect ratio/Profile search start
        ratioSearch = True
        while ratioSearch:
            try:
                aspectratioprofiles = []
                answer = ""
                aspectratioselect = Select(browser.find_element("id","tyreprofileselect"))
                aspectratiooptions = aspectratioselect.options
                for option in aspectratiooptions: aspectratioprofiles.append(option.get_attribute("value"))
                aspectratioprofiles.pop(0)

                for i, value in enumerate(aspectratioprofiles):
                    print(str(i+1) + ") " + str(value))

                aspectratioprofile = int(input("Please select your aspect ratio/profile using its listed number: "))
                print("Aspect ratio/profile selected: " + str(aspectratioprofiles[aspectratioprofile-1]))
                aspectratioselect.select_by_index(aspectratioprofile)
                ratio_url = str(aspectratioprofiles[aspectratioprofile-1])
                ratioSearch = False
            except:
                answer = str(input("That combination isn't available. Do you you wish to continue? Y/N: "))
            
            if answer.lower() == 'n': break
        
        if ratioSearch:
            keepSearching = False
            exit_ = True
            break
        #Aspect Ratio/Profile search end



        #Rim size search start
        rimSearch = True
        while rimSearch:
            try:
                rims = []
                answer = ""
                rimselect = Select(browser.find_element("id","tyrerimselect"))
                rimoptions = rimselect.options
                for option in rimoptions: rims.append(option.get_attribute("value"))
                rims.pop(0)

                for i, value in enumerate(rims):
                    print(str(i+1) + ") " + str(value))

                rim = int(input("Please select your rim size using its listed number: "))
                print("Rim size selected: " + str(rims[rim-1]))
                rimselect.select_by_index(rim)
                rim_url = str(rims[rim-1])
                rimSearch = False
                keepSearching = False
            except:
                answer = str(input("That combination isn't available. Do you you wish to continue? Y/N: "))

            if answer.lower() == 'n': break
        
        if rimSearch:
            keepSearching = False
            exit_ = True
            break
        #Rim size search end
    
    if exit_ == False:
        print("Searching...")
        url = "http://www.dexel.co.uk/shopping/tyre-results?width=" + width_url + "&profile=" + ratio_url + "&rim=" + rim_url + "&speed=."
        browser.get(url)
        #browser.find_element(By.XPATH, "//input[@class='button secondary']").click()

def scrape(jsonList, website):
    tyreData = {}
    columnName = [".column-one.column", ".column-two.column", ".column-three.column"]
    ui.WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "tyre-results")))

    i = 0
    while i < 3:
        col = browser.find_element(By.CSS_SELECTOR, columnName[i])
        tyres = col.find_elements(By.CLASS_NAME, "result")
        for tyre in tyres:
            try:
                name = tyre.find_element(By.CLASS_NAME, "name")
                price = tyre.find_element(By.CLASS_NAME, "price")
                ratings = tyre.find_element(By.CLASS_NAME, "tyre-ratings")
                fuelEfficiency = ratings.find_element(By.CLASS_NAME, "fuel").text
                wetGrip = ratings.find_element(By.CLASS_NAME, "wetgrip").text
                noise = ratings.find_element(By.CLASS_NAME, "noise").text
                extraInfo = tyre.find_element(By.CLASS_NAME, "icons")
                extraInfoIcons = extraInfo.find_elements(By.TAG_NAME, "li")
                extraInfoSlots = ["No", "No", "No", "No"]
                for ii, icon in enumerate(extraInfoIcons):
                    if icon.get_attribute("style") == "display: list-item;":
                        extraInfoSlots[ii] = "Yes"



                nameInfo = name.text.split(" ", 3)
                _name = nameInfo[3]
                try:
                    brand = _name.split(" ", 2)[0]
                    tyrePattern = _name.lstrip(_name.split(" ")[0])
                    tyrePattern = tyrePattern.lstrip()
                except:
                    brand = _name
                    tyrePattern = "N/A"
                width = nameInfo[0].split("/")[0]
                aspectRatio = nameInfo[0].split("/")[1]
                rimDiameter = nameInfo[1][1:]
                construction = nameInfo[1][0]
                loadRating = nameInfo[2].rstrip(nameInfo[2][-1])
                speedRating = nameInfo[2][-1]


                tyreData["website"] = website
                tyreData['brand'] = brand
                tyreData['tyrePattern'] = tyrePattern
                tyreData['width'] = width
                tyreData['aspectRatio'] = aspectRatio
                tyreData['rimDiameter'] = rimDiameter
                tyreData['construction'] = construction
                tyreData['loadRating'] = loadRating
                tyreData['speedRating'] = speedRating

                price = price.text.split(" ")[0]
                tyreData['price'] = price
                tyreData['extraLoad'] = extraInfoSlots[0]
                tyreData['runFlat'] = extraInfoSlots[1]
                tyreData['winter'] = extraInfoSlots[2]
                tyreData['allSeason'] = extraInfoSlots[3]
                tyreData['fuelEfficiency'] = fuelEfficiency
                tyreData['wetGrip'] = wetGrip
                tyreData['noise'] = noise

                data_ = copy.deepcopy(tyreData)
                jsonList.append(data_)

            except:
                continue
        i += 1

    print("Tyres found: " + str(len(jsonList)))

def SaveFiles(jsonList):
    open("tyres.json", "w")
    jsonList = sorted(jsonList, key = lambda i: i['brand'])
    with open('tyres.json', 'w', encoding="utf-8") as f:
        json.dump(jsonList, f, ensure_ascii=False, indent=4)
    print("Saved to JSON file 'tyres.json'")

    with open('tyres.json', encoding="utf-8") as f:
        csvFile = p.read_json(f)
    csvFile.to_csv('tyres.csv', encoding=False, index=False)
    print("Saved to CSV file 'tyres.csv'")

main()