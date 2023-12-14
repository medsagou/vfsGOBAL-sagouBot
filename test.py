import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium import  webdriver
from utilities import Proxy_Formater

try:
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("start-maximized")
    # # # options.add_argument("--headless")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--ignore-certificate-errors-spki-list')
    # options.add_argument('--ignore-ssl-errors')
    proxy = Proxy_Formater()
    print(f'https://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}')
    options.add_argument(f'--proxy-server=https://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}')
    print("GETTING THE DRIVER")
    driver = uc.Chrome(options=options)

    driver.get("https://www.google.com")
    # self.driver.get("https://visa.vfsglobal.com/mar/fr/prt/login")
except Exception as e:
    print(f"Error {e}")
else:
    print("DRIVER IS SET")