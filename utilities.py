import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from selenium.webdriver.common.proxy import Proxy, ProxyType
import pyautogui
import os
import zipfile


def get_proxy():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    print('NOTE: GETTING THE PROXIES...')
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH,
                                          '//*[@id="list"]/div/div[2]/div/table//th[contains(., "IP Address")]'))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 15).until(
        EC.visibility_of_all_elements_located((By.XPATH,
                                               '//*[@id="list"]/div/div[2]/div/table/tbody/tr/td[1]')))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.XPATH,
                                               '//*[@id="list"]/div/div[2]/div/table/tbody/tr/td[2]')))]
    driver.quit()
    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i] + ':' + ports[i])
    # print(proxies)
    for i in range(0, len(proxies)):
        try:
            print("Proxy selected: {}".format(proxies[i]))
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server={proxies[i]}')
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.whatismyip.com/proxy-check/?iref=home")
            WebDriverWait(driver, 30).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete')
            print("LOADING FINSHED")
            if "Proxy Type" in WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#the-return"))):
                return proxies[i]
        except Exception:
            driver.quit()

def get_proxy2(ch = ""):
    ch = ch.split(":")

    # Set up Chrome options

    # Set up the proxy with authentication
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = f"{ch[2]}:{ch[-1]}@{ch[0]}:{ch[1]}"
    proxy.ssl_proxy = f"{ch[2]}:{ch[-1]}@{ch[0]}:{ch[1]}"
    print("NOTE: PROXY IS SET")
    return proxy


def enter_proxy_auth(proxy_username, proxy_password):
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    time.sleep(4)
    pyautogui.press('enter')



def get_chromedriver(use_proxy=False, user_agent=None, proxy = ""):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy and proxy != "":
        proxy = proxy.split(":")
        PROXY_HOST=proxy[0]
        PROXY_PORT=proxy[1]
        PROXY_USER=proxy[2]
        PROXY_PASS=proxy[3]
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
        chrome_options.add_argument("start-maximized")
        # options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option('prefs', {'profile.managed_default_content_settings.javascript': 2})
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# CLASSES

class Proxy_Formater:
    def __init__(self, CH="", HOST="", PORT="", USER="", PASS=""):
        self.CH = CH
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASS = PASS
        self.format_ch()
    def format_ch(self):
        if self.CH != "":
            try:
                ch = self.CH.split(":")
            except:
                print("ERROR: THE PROXY STRING IS NOT VALID")
            else:
                self.HOST = ch[0]
                self.PORT = ch[1]
                self.USER = ch[2]
                self.PASS = ch[3]