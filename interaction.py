from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv

load_dotenv()
from class_fichier import C_Fichier
from selenium.webdriver.common.keys import Keys



import time
import os


class Account:
    def __init__(self, driver="", email=os.getenv("EMAIL"), password=os.getenv("PASSWORD")):
        self.driver = driver
        self.email = email
        self.password = password
        self.destractions = 0

        # End of init function

    def loading_screens(self):
        try:
            WebDriverWait(self.driver, 1000).until(
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
                WebDriverWait(self.driver, 1000).until(
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
        profile = webdriver.FirefoxProfile()
        options = FirefoxOptions()


        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()

        options.profile=profile
        self.driver = webdriver.Firefox(options=options)


        self.driver.get("https://visa.vfsglobal.com/mar/fr/prt/login")
        self.loading_screens()
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
            pass_Field = self.driver.find_element(By.ID, "mat-input-1")
        finally:
            pass_Field = self.driver.find_element(By.ID, "mat-input-1")
            pass_Field.send_keys(self.password)
            print("NOTE: INPUT PASSWORD")
            self.remove_destraction()
        return

    def wait_recptcha_to_be_solved(self):
        try:
            iframe = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
                )
            )
        except:
            print("ERROR: WE CANNOT SWITCH TO RECAPTCHA IFRAME")
        else:
            self.driver.switch_to.frame(iframe)
            # i=10
            # while i!=0:
            print(f"WAITING FOR RECAPTCHA TO BE SOLVED...")
            try:
                WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="recaptcha-anchor"][contains(@aria-checked, "true")]')
                    )
                )
            except Exception as err:
                # i=i-1
                print(err)
            else:
                print("NOTE: RECAPTCHA HAS BEEN SOLVED")
                self.driver.switch_to.default_content()
                self.remove_destraction()
                return True


            # for i in range(10):
            #     try:
            #         recaptcha = self.driver.find_elements(By.CSS_SELECTOR, '#recaptcha-anchor[aria-checked="true"]')
            #     except:
            #         print(f"WARNING: WAITING FOR RECAPTCHA TO BE SOLVED {10-i}...")
            #         time.sleep(5)
            #     else:
            #         if len(recaptcha) != 0:
            #             print("NOTE: RECAPTCHA HAS BEEN SOLVED")
            #             self.driver.switch_to.default_content()
            #             return True
            #         else:
            #             print(f"WARNING: WAITING FOR RECAPTCHA TO BE SOLVED {10-i}...")
            #             time.sleep(5)
            # self.driver.switch_to.default_content()
            # return False



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
            print(len(options))
            for option in options:
                print(option.text)
                try:
                    self.driver.execute_script("arguments[0].click();", option)
                except Exception as err:
                    print(err)
                else:
                    self.loading_screens()
                    agence_mat_select = self.driver.find_element(By.XPATH, '//*[@id="mat-select-2"]')
                    self.driver.execute_script("arguments[0].click();", agence_mat_select)
                    option_type = self.driver.find_element(By.XPATH, "//*[text()=' Schengen ']")
                    try:
                        self.driver.execute_script("arguments[0].click();", option_type)
                    except Exception as err:
                        print(err)
                    else:
                        self.loading_screens()
                        try:
                            WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, "//*[text()=' Désolé, mais aucune place de rendez-vous n'est actuellement disponible. Veuillez réessayer plus tard. '"))
                            )
                        except Exception as err:
                            print(err)
                        else:
                            print("NOTE: NO RESERVATION DATE IS AVAILABLE")
                            self.driver.execute_script("arguments[0].click();", agence_mat_select)
        return





