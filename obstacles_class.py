#SELENIUM MODULES
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"

class Prices:

    def __init__(self,product,shopName):
        self.product = product
        self.shopName = shopName
        self.productAndPriceDict = {}

    def get_groceries_price(self,driver):
        self.dict = {'Tesco':"https://www.tesco.com/",'Asda':"https://groceries.asda.com/"} #will add more later
        prices = []
        products = []
        from_store = []

        if 'Tesco' in self.shopName:

            driver.get("%s" % (self.dict['Tesco']))

            search = driver.find_element_by_xpath("(//input[@name='searchKey'])[2]")
            search.send_keys("%s" % (self.product))
            search.send_keys(Keys.RETURN)

            try:
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//span[@class='value']"))
                )
                nameLabel = driver.find_elements_by_xpath("//a[@data-auto='product-tile--title']")
                for index, price in enumerate(main):
                    if nameLabel[index].text in products: #prevent any repeats
                        pass
                    else:
                        products.append(nameLabel[index].text)
                        prices.append(price.text)
                        self.productAndPriceDict["%s" % (nameLabel[index].text)] = price.text
                        from_store.append('Tesco Extra')
            except:
                driver.quit()

        elif 'Asda' in self.shopName:
            driver.get("%s"%(self.dict['Asda']))
            search = driver.find_element_by_xpath("(//*[@id='search'])")
            search.send_keys("%s" % self.product)
            search.send_keys(Keys.RETURN)

            try:
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//strong[@class='co-product__price']")))

                nameLabel = driver.find_elements_by_xpath("//a[@class='co-product__anchor']")

                count = 0
                for index, price in enumerate(main):
                    if nameLabel[index].text in products:
                        break
                    elif count > 20:  # just want to scrape 20
                        break
                    else:
                        count += 1
                        products.append(nameLabel[index].text)
                        prices.append(price.text)
                        self.productAndPriceDict["%s" % (nameLabel[index].text)] = price.text
                        from_store.append("Asda")

            except:
                driver.quit()

        return(self.productAndPriceDict),from_store

    def get_pet_price(self):
        self.dict = {} #add websites

    def get_furniture_price(self):
        self.dict = {} #add websites


class Store:
    def __init__(self,lat,long,category,store_name):
        self.lat = lat
        self.long = long
        self.category = category
        self.store_name = store_name
        self.walk_time = None
        self.dist = None


    def get_product_price(self, productName):
        Price = Prices(productName, self.store_name)
        if "supermarket" in self.category:
            pricesWithProductsDict, shopName = Price.get_groceries_price(webdriver.Chrome(PATH))
            return pricesWithProductsDict, shopName

class Product(Store):
    def __init__(self,lat,long,category,store_name,priority,product_name,price,walk_time,distance):
        super(Product,self).__init__(lat,long,category,store_name)
        self.priority = priority
        self.price = price
        self.product_name = product_name
        self.walk_time = walk_time
        self.dist = distance
