from selenium import webdriver

from interaction import Account
account = Account()
account.get_driver()
account.email_field()
account.password_field()
account.submit_button() if account.wait_recptcha_to_be_solved() else print("ERROR: WE CANNOT SUMBIT THE FORM BECUASE OF RECAPTCHA PROBLEM")
account.go_to_reservation_page()
account.reservation_loop()

