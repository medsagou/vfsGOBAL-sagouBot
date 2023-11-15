# from selenium import webdriver
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv
from selenium_stealth import stealth
from fake_useragent import UserAgent
from seleniumwire import webdriver

import seleniumwire.undetected_chromedriver as uc


load_dotenv()
from class_fichier import C_Fichier
from utilities import get_proxy2, enter_proxy_auth, get_chromedriver, Proxy_Formater, on_connection_error

from selenium.webdriver.common.keys import Keys

import chromedriver_autoinstaller


import time
import os


from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Account:
    def __init__(self, driver="", email=os.getenv("EMAIL"), password=os.getenv("PASSWORD")):
        self.driver = driver
        self.email = email
        self.password = password
        self.destractions = 0

        # End of init function

    def loading_screens(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, 'loader')
                )
            )
        except Exception as err:
            return err
        else:
            print('NOTE: WAITING FOR THE PAGE LOADING 1')
        try:
            WebDriverWait(self.driver, 1000).until(
                EC.invisibility_of_element_located(
                    (By.ID, 'loader')
                )
            )
        finally:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.loading-foreground')
                    )
                )
            except Exception as err:
                return err
            else:
                print("NOTE: WAITING FOR THE PAGE LOADING 2")
            try:
                WebDriverWait(self.driver, 1000).until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, 'div.loading-foreground')
                    )
                )
            finally:
                return True


    def get_driver(self):
        # profile = webdriver.FirefoxProfile()
        # self.driver = webdriver.Firefox()
        # PROXY = '5.255.107.249:8080'
        # print("Proxy Invoked")
        options = webdriver.ChromeOptions()
        # options = webdriver.FirefoxOptions()
        # chrome_profile_path = "C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data"

        # options.add_argument("user-data-dir=" + chrome_profile_path)
        # chromedriver_autoinstaller.install()

        # options.add_experimental_option('prefs', prefs) # import prefs from utilities

        # options.add_experimental_option('prefs', {'profile.managed_default_content_settings.javascript': 2})
        proxy = Proxy_Formater()
        # options.add_argument(f"--proxy-server={proxy.HOST}:{proxy.PORT}")
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}',
                'https': f'https://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}',
                'no_proxy': 'localhost,127.0.0.1',
                # 'on_connection_error': on_connection_error,
                'suppress_connection_errors': False
            },
            # 'proxy': {
            #     'http': f'https://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}',
            #     'https': f'https://{proxy.USER}:{proxy.PASS}@{proxy.HOST}:{proxy.PORT}',
            #     'verify_ssl': True, # it's was False
            # },
        }


        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("start-maximized")
        # # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        # self.driver = webdriver.Firefox(options=options,seleniumwire_options=seleniumwire_options)
        # self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Firefox()


        # driver.get("https://bot.sannysoft.com/")

                        # firefox_options = webdriver.FirefoxOptions()
                        # firefox_options.binary_location = 'C:\\Users\\HP\\Desktop\\Tor Browser\\Browser\\firefox.exe'
                        #
                        # # Set the profile path
                        # firefox_options.profile = 'C:\\Users\\HP\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default\\'
                        # firefox_options.set_preference("network.proxy.type", 1)
                        # firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
                        # firefox_options.set_preference("network.proxy.socks_port", 9150)
                        # firefox_options.set_preference("network.proxy.socks_remote_dns", False)
                        # self.driver = webdriver.Firefox(options=firefox_options)
                        # time.sleep(300)
        # self.driver.get("https://whatismyipaddress.com/")
        # time.sleep(34)
        try:
            print("NOTE: GETTING THE DRIVER")
            self.driver = webdriver.Chrome(options=options,seleniumwire_options=seleniumwire_options)
            stealth(self.driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            print("NOTE: GETTING THE SITE 1")
            self.driver.get("https://visa.vfsglobal.com/mar/fr/prt/login")
        except Exception as e:
            if "Invalid proxy server credentials supplied" in str(e):
                print("Invalid proxy credentials supplied. Please check and try again.")
                self.driver.quit()
                sys.exit()
            else:
                print(f"An error occurred: {e}")
                # self.driver.quit()
                sys.exit()
        else:
            pass
        print("NOTE: GETTING THE SITE")
        # print("NOTE: PYAUTOGUI TRY TO FILL THE PROXY CREDENTIEL")
        # enter_proxy_auth(proxy_username=proxy.USER, proxy_password=proxy.PASS)
        self.loading_screens()
        # self.driver.save_screenshot("screen1.png")
        return

    def email_field(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mat-input-0"))
            )
        finally:
            email_Field = self.driver.find_element(By.ID, "mat-input-0")
            email_Field.send_keys(self.email)
            print("NOTE: INPUT EMAIL")
        return


    def password_field(self):
        try:
            _= self.driver.find_element(By.ID, "mat-input-1")
        finally:
            pass_Field = self.driver.find_element(By.ID, "mat-input-1")
            pass_Field.send_keys(self.password)
            print("NOTE: INPUT PASSWORD")
            self.remove_destraction()
            # time.sleep(10)
            # self.driver.save_screenshot('screen.png')
        return


    def wait_recptcha_to_be_solved_2(self):
        try:
            iframe = WebDriverWait(self.driver, 1000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
                )
            )
        except:
            print("ERROR: WE CANNOT SWITCH TO RECAPTCHA IFRAME")
        else:
            print("NOTE: PRESENCE OF RECAPTCHA")
            self.driver.switch_to.frame(iframe)
            print(f"WAITING FOR RECAPTCHA TO BE SOLVED...")
            try:
                WebDriverWait(self.driver, 55).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="recaptcha-anchor"][contains(@aria-checked, "true")]')
                    )
                )
            except Exception as err:
                print(err)
            else:
                print("NOTE: RECAPTCHA HAS BEEN SOLVED")
                self.driver.switch_to.default_content()
                self.remove_destraction()
                return True

    def wait_recptcha_to_be_solved(self):
        try:
            iframe = WebDriverWait(self.driver, 1000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
                )
            )
        except:
            print("ERROR: WE CANNOT SWITCH TO RECAPTCHA IFRAME")
        else:
            print("NOTE: PRESENCE OF RECAPTCHA")
            self.driver.switch_to.frame(iframe)
            print(f"WAITING FOR RECAPTCHA TO BE SOLVED...")
            for i in range(100):
                try:
                    recaptcha = self.driver.find_elements(By.CSS_SELECTOR, '#recaptcha-anchor[aria-checked="true"]')
                except:
                    print(f"WARNING: WAITING FOR RECAPTCHA TO BE SOLVED {100-i}...")
                    time.sleep(5)
                else:
                    if len(recaptcha) != 0:
                        print("NOTE: RECAPTCHA HAS BEEN SOLVED")
                        self.driver.switch_to.default_content()
                        return True
                    else:
                        print(f"WARNING: WAITING FOR RECAPTCHA TO BE SOLVED {100-i}...")
                        time.sleep(5)
            # self.driver.save_screenshot("screenshot.png")
            self.driver.switch_to.default_content()
            return False



    def remove_destraction(self):
        if self.destractions != 0:
            return
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
                )
            )
        except:
            print("NOTE: NO DESTRACTION THERE")
        else:
            remove_destractionBtn = self.driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
            self.driver.execute_script("arguments[0].click();",remove_destractionBtn)
            print("NOTE: DESTRACTION HAS BEEN REMVOED")
            self.destractions = 1
            return True



    def submit_button(self):
            try:
                submit_button = self.driver.find_elements(By.CSS_SELECTOR,
                    '.mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base ng-star-inserted'.replace(" ","."))
            except:
                print("ERROR: WE CANNOT FIND THE SUBMIT BUTTON")
            else:
                submit_button[0].click()
            return True
    #
    def go_to_reservation_page(self):
        self.loading_screens()
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[text()=" Démarrer une nouvelle réservation "]')
                )
            )
        except:
            print("ERROR: WE CANNOT FIND THE RESERVATION PAGE LINK")
            return False
        else:
            reservation_link = self.driver.find_element(By.XPATH,'//*[text()=" Démarrer une nouvelle réservation "]')
            self.driver.execute_script("arguments[0].click();", reservation_link)
            print("NOTE: SWITCHING TO APPLICATION DETAIL PAGE...")
            return True

    def is_button_active(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[@disabled="true"]//span[contains(text(), " Continuer ")]'))
            )
        except Exception as err:
            print("err01")
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@disabled="false"]//span[contains(text(), " Continuer ")]'))
                )
            except Exception as err:
                print(err)
            else:
                print("NOTE: WE FIND A BUTTON WITH DISABLED FALSE")
            button = self.driver.find_element(By.XPATH, '//button//span[contains(text(), " Continuer ")]')
            self.driver.execute_script("arguments[0].click();", button)
            return True
        else:
            print('NOTE: BUTTON STILL DESABLED')
            return False


    def reservation_loop(self):
        self.loading_screens()
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-select-0"]'))
            )
        except Exception as err:
            print(err)
        else:
            agence_mat_select = self.driver.find_element(By.XPATH, '//*[@id="mat-select-0"]')
            self.driver.execute_script("arguments[0].click();", agence_mat_select)
            options = self.driver.find_elements(By.XPATH, '//mat-option')
            # print(len(options))
            # for option in options:
            #     print(option.text)

            while True:
                for option in options:
                    try:
                        self.driver.execute_script("arguments[0].click();", option)
                    except Exception as err:
                        print(err)
                        break
                    else:
                        self.loading_screens()
                        visa_type = self.driver.find_element(By.XPATH, '//*[@id="mat-select-2"]')
                        self.driver.execute_script("arguments[0].click();", visa_type)
                        option_type = self.driver.find_element(By.XPATH, "//*[text()=' Schengen ']")
                        try:
                            self.driver.execute_script("arguments[0].click();", option_type)
                        except Exception as err:
                            print(err)
                            break
                        else:
                            self.loading_screens()
                            if self.is_button_active():
                                print("NOTE: BUTTON IS CLICKED")
                                print("NOTE: CONGRATULATION WE FIND A DATE")
                                return
                            else:
                                print("NOTE: NO RESERVATION DATE IS AVAILABLE")
                                time.sleep(2)
                                self.driver.execute_script("arguments[0].click();", agence_mat_select)


                            # try:
                            #      = WebDriverWait(self.driver, 20).until(
                            #             EC.presence_of_element_located((By.XPATH, '//div[text()=" Désolé, mais aucune place de rendez-vous n\'est actuellement disponible. Veuillez réessayer plus tard. "'))
                            #         )
                            # except Exception:
                            #     print("err1")
                            #     print("err1")
                            # else:
                            #     print("NOTE: NO RESERVATION DATE IS AVAILABLE")
                            #     self.driver.execute_script("arguments[0].click();", agence_mat_select)




