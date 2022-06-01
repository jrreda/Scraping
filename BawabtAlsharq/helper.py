from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # import KEYS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import sys
import random
import string
import live_connect_db
import beta_connect_db
import datetime as DT


# Define variables
name = 'test'
image_path = os.getcwd()+"/messi.jpeg"
test_string = "test test test testttt 2131 ST."
website = "https://www.test.com"
country = 'Egypt'
phone = '01069907582'
# phone = random_phone()
email = 'mahmoudredabs@gmail.com'
# email = (random_char(9)+"@test.com")
password = 'Pa$$w0rd!'
checkbox = True
search_input = 'fire alarm'
next_week = format(DT.timedelta(days=7) + DT.date.today(), '%m/%d/%Y')

# domains
domain = str(input("\nlive or beta?\n"))
if domain == 'beta':
    domain = "https://flapsy.org/"
    # Update mahmoudredabs@gmail.com in the db
    beta_connect_db.update_mahmoudredabs()
elif domain == 'live':
    domain = "https://bawabtalsharq.com/"
    # Update mahmoudredabs@gmail.com in the db
    live_connect_db.update_mahmoudredabs()
else:
    print("Choose either 'live' or 'beta'")


is_required = str(input("\nFill required only? [yes OR no]\n"))


# load the driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.delete_all_cookies()


def check_element_visability(page:str, text:str):
    confermation_text = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]')
    if (confermation_text.text == text):
        print(f"{page} Confirmation was successful ✔️​")
    else:
        print(f"{page} Confirmation was not successful ❌")
    ## Press OK
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/div/button').click()


def register():
    driver.get(f"{domain}register")
    ## Fill the form
    # first name
    driver.find_element(by=By.XPATH, value='//*[@id="first_name"]').send_keys(name)
    # last name
    driver.find_element(by=By.XPATH, value='//*[@id="last_name"]').send_keys(name)
    # country
    driver.find_element(by=By.XPATH, value='//*[@id="country"]').send_keys(country)
    # phone
    driver.find_element(by=By.XPATH, value='//*[@id="phone"]').send_keys(phone)
    # email
    driver.find_element(by=By.NAME, value='email').send_keys(email)
    # password
    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)
    # password confirm
    driver.find_element(by=By.XPATH, value='//*[@id="password-confirm"]').send_keys(password)
    # check
    driver.find_element(by=By.XPATH, value='//*[@id="checkbox"]').click()
    # submit
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/div/div/div/div/div/div/div[1]/div[2]/div/form/div[7]/div/button').click()
        # verify the mail
        if domain == "https://flapsy.org/": beta_connect_db.verify_mail()
        elif domain == "https://bawabtalsharq.com/": live_connect_db.verify_mail()
        time.sleep(2)
    except Exception as e:
        print("Can't press Submit on Register!")
        sys.exit(1)
        # raise
    # Confirm Registration
    check_element_visability(page="Register", text="Check your mail, to verify your account")

def logout(is_after_becomeAsupplier):
    # Click NavBar dorpdown menu
    driver.find_element(by=By.XPATH, value='//*[@id="navbarDarkDropdownMenuLink"]').click()
    if is_after_becomeAsupplier:
        # click on Becoma A supplier
        driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[1]/div/div[3]/ul/li[4]/ul/div/div[3]/a[3]').click()
        print("Logged out!")
    else:
        # click on Becoma A supplier
        driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[1]/div/div[3]/ul/li[4]/ul/div/div[3]/a[4]').click()
        print("Logged out!")
    time.sleep(2)           # wait 2 sec till the driver reloads

def sign_in():
    # click on signin
    driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[1]/div/div[3]/ul/li[3]/div/div/p[2]/a').click()
    ## fill the form
    # fill email
    driver.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys(email)
    # fill password
    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)
    # press on login
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/div/div/div/div/div/div/div[1]/div[2]/div/form/div[4]/div/button').click()
    print("Logged back in!")
    time.sleep(2) # wait

def become_a_supplier(is_required, is_from_buyer):
    if is_from_buyer:
        # Click NavBar dorpdown menu
        driver.find_element(by=By.XPATH, value='//*[@id="navbarDarkDropdownMenuLink"]').click()
        # click on Becoma A supplier
        driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[1]/div/div[3]/ul/li[4]/ul/div/div[3]/a[1]').click()
        time.sleep(2)           # wait 3 sec till the driver reloads
        if is_required == 'yes':
            ### 1st step - Company Details
            # Company name *
            driver.find_element(by=By.NAME, value='name_en').send_keys(name)
            # Company Address *
            driver.find_element(by=By.NAME, value='address_en').send_keys(test_string)
            time.sleep(2)                               # driver.implicitly_wait(2)
        else:
            ### 1st step - Company Details
            # Company name
            driver.find_element(by=By.NAME, value='name_en').send_keys(name)
            # Company email
            driver.find_element(by=By.NAME, value='company_email').send_keys(email)
            # Company Phone Number
            driver.find_element(by=By.NAME, value='Company_phone').send_keys(phone)
            # Company Addres
            driver.find_element(by=By.NAME, value='address_en').send_keys(test_string)
            # Official website
            driver.find_element(by=By.NAME, value='website').send_keys(website)
            # Commercial Registration No.
            driver.find_element(by=By.NAME, value='commercial_registration').send_keys(test_string)
            # Tax Id
            driver.find_element(by=By.NAME, value='tax_id').send_keys(test_string)
            # Certifications
            time.sleep(2)                               # driver.implicitly_wait(2)
            iframe_cert = driver.find_element(by=By.ID, value='certificates_ifr')
            driver.switch_to.frame(iframe_cert)        # switch to iframe
            text_area_cert = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
            text_area_cert.clear()                     # clear the text area
            text_area_cert.send_keys(test_string)
            text_area_cert.send_keys(Keys.ENTER)
            text_area_cert.send_keys(test_string)
            driver.switch_to.default_content()          # return to original iframe
            time.sleep(2)                               # driver.implicitly_wait(2)
            # About Company
            iframe_about = driver.find_element(by=By.ID, value='description_en_ifr')
            driver.switch_to.frame(iframe_about)        # switch to iframe
            text_area_about = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
            text_area_about.clear()                     # clear the text area
            text_area_about.send_keys(test_string)
            text_area_about.send_keys(Keys.ENTER)
            text_area_about.send_keys(test_string)
            driver.switch_to.default_content()          # return to original iframe
            time.sleep(2)                               # driver.implicitly_wait(2)
        # submit
        try:
            submit = driver.find_element(by=By.XPATH, value='//*[@id="beVendorSubmitBtn"]')
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print("Can't press Submit on Become A Supplier ❌❌❌")
            sys.exit(1)
        ## Press OK
        # driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/div/button').click()
        # Confirm Registration
        check_element_visability(page="Buyer -> Become A Supplier", text="We will get in contact soon")
    else:
        if domain == "https://flapsy.org/": beta_connect_db.update_mahmoudredabs()
        elif domain == "https://bawabtalsharq.com/": live_connect_db.update_mahmoudredabs()
        ### Become A Supplier Before Register
        driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[2]/div/div/div[1]/div/ul/li[3]/a').click()
        # if is_required:
        if is_required == 'yes':
            ### 1st step - Account Info
            # first name *
            driver.find_element(by=By.XPATH, value='//*[@id="first_name"]').send_keys(name)
            # last name *
            driver.find_element(by=By.XPATH, value='//*[@id="last_name"]').send_keys(name)
            # country *
            driver.find_element(by=By.XPATH, value='//*[@id="country"]/option[68]').click()
            # Phone Number *
            driver.find_element(by=By.XPATH, value='//*[@id="phone"]').send_keys(phone)
            # Email *
            driver.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys(email)
            # password *
            driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)
            # password confirm *
            driver.find_element(by=By.XPATH, value='//*[@id="password_confirmation"]').send_keys(password)
            ## Company Info
            # Company name *
            driver.find_element(by=By.XPATH, value='//*[@id="exampleInputEmail1"]').send_keys(name)
            # Company Address *
            driver.find_element(by=By.NAME, value='address_en').send_keys(test_string)
        else:
            ### 1st step - Account Info
            # first name *
            driver.find_element(by=By.XPATH, value='//*[@id="first_name"]').send_keys(name)
            # last name *
            driver.find_element(by=By.XPATH, value='//*[@id="last_name"]').send_keys(name)
            # country *
            driver.find_element(by=By.XPATH, value='//*[@id="country"]/option[68]').click()
            # Phone Number *
            driver.find_element(by=By.XPATH, value='//*[@id="phone"]').send_keys(phone)
            # Email *
            driver.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys(email)
            # password
            driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)
            # password confirm
            driver.find_element(by=By.XPATH, value='//*[@id="password_confirmation"]').send_keys(password)
            ### Company Info
            # Company name
            driver.find_element(by=By.XPATH, value='//*[@id="exampleInputEmail1"]').send_keys(name)
            # Company email address
            driver.find_element(by=By.XPATH, value='//*[@id="company_email"]').send_keys(email)
            # Company phone
            driver.find_element(by=By.XPATH, value='//*[@id="Company_phone"]').send_keys(phone)
            # Company Addres
            driver.find_element(by=By.NAME, value='address_en').send_keys(test_string)
            # Official website
            driver.find_element(by=By.NAME, value='website').send_keys(website)
            # Commercial Registration No.
            driver.find_element(by=By.NAME, value='commercial_registration').send_keys(test_string)
            # Tax Id
            driver.find_element(by=By.NAME, value='tax_id').send_keys(test_string)
            # Certifications
            time.sleep(2)                               # driver.implicitly_wait(2)
            iframe_cert = driver.find_element(by=By.ID, value='certificates_ifr')
            driver.switch_to.frame(iframe_cert)        # switch to iframe
            text_area_cert = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
            text_area_cert.clear()                     # clear the text area
            text_area_cert.send_keys(test_string)
            text_area_cert.send_keys(Keys.ENTER)
            text_area_cert.send_keys(test_string)
            driver.switch_to.default_content()          # return to original iframe
            time.sleep(2)                               # driver.implicitly_wait(2)
            # About Company
            iframe_about = driver.find_element(by=By.ID, value='description_en_ifr')
            driver.switch_to.frame(iframe_about)        # switch to iframe
            text_area_about = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
            text_area_about.clear()                     # clear the text area
            text_area_about.send_keys(test_string)
            text_area_about.send_keys(Keys.ENTER)
            text_area_about.send_keys(test_string)
            driver.switch_to.default_content()          # return to original iframe
            time.sleep(2)                               # driver.implicitly_wait(2)
        # accept terms & conditions
        check = driver.find_element(by=By.XPATH, value='//*[@id="checkbox"]')
        driver.execute_script("arguments[0].click();", check)
        # submit
        try:
            submit = driver.find_element(by=By.XPATH, value='//*[@id="beVendorSubmitBtn"]')
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print("Can't press Submit on Register!")
            sys.exit(1)
        # Confirm
        check_element_visability(page="Become A Supplier without Register",
                                text="Your Request Added Successfully")

def contact_us(is_logged):
    driver.find_element(by=By.XPATH, value='//*[@id="header"]/div[2]/div/div/div[1]/div/ul/li[4]/a').click()
    if is_logged:
        # subject
        driver.find_element(by=By.XPATH, value='/html/body/section/form/div/div/div/div[1]/div[2]/div[3]/input').send_keys(name)
        # message
        driver.find_element(by=By.XPATH, value='//*[@id="floatingTextarea"]').send_keys(test_string)
    else:
        # mail
        driver.find_element(by=By.XPATH, value='/html/body/section/form/div/div/div/div[1]/div[2]/div[1]/input').send_keys(email)
        # phone
        driver.find_element(by=By.XPATH, value='/html/body/section/form/div/div/div/div[1]/div[2]/div[2]/input').send_keys(email)
        # subject
        driver.find_element(by=By.XPATH, value='/html/body/section/form/div/div/div/div[1]/div[2]/div[3]/input').send_keys(name)
        # message
        driver.find_element(by=By.XPATH, value='//*[@id="floatingTextarea"]').send_keys(test_string)
    # send
    try:
        driver.find_element(by=By.XPATH, value='/html/body/section/form/div/div/div/div[1]/div[2]/div[5]/button').click()
    except Exception as e:
        print("Can't press Submit on Send in Contact Us ❌❌❌")
        sys.exit(1)
    # Confirm Registration
    check_element_visability(page="Contact Us", text="You mail has been sent successfully")

def search():
    # type alarm in search bar
    driver.find_element(by=By.XPATH, value='//*[@id="myInput3"]').send_keys(search_input)
    # click on search
    driver.find_element(by=By.XPATH, value='//*[@id="basic-addon2"]').click()
    # click on the products
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/div/div/div/div/a').click()

def submit_rfq(is_required):
    time.sleep(2) # wait
    # click on request_now
    element = driver.find_element(by=By.CLASS_NAME, value='GTM-request-now')
    driver.execute_script("arguments[0].click();", element)
    ### 1st step
    time.sleep(2) # driver.implicitly_wait(10)
    # if is_required:
    if is_required == 'yes':
        # unit
        driver.find_element(by=By.XPATH, value='//*[@id="unit_id"]/option[2]').click()
        # Target Price
        driver.find_element(by=By.XPATH, value='//*[@id="target_price"]').send_keys(156123)
        # sourcing purpose
        driver.find_element(by=By.XPATH, value='//*[@id="source_propose_id"]/option[2]').click()
        ### Description
        ifr = driver.find_element(by=By.ID, value='details_ifr')
        driver.switch_to.frame(ifr)                 # switch to iframe
        text_area = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
        text_area.clear()                           # clear the text area
        time.sleep(3)                               # wait for 5 sec
        text_area.send_keys(test_string)
        text_area.send_keys(Keys.ENTER)
        text_area.send_keys(test_string)
        driver.switch_to.default_content()          # return to original iframe
        time.sleep(3)                               # driver.implicitly_wait(3)
        # Upload Image
        driver.find_element(by=By.XPATH, value='//*[@id="file-upload"]').send_keys(image_path)
        # Press next
        next = driver.find_element(by=By.XPATH, value='//*[@id="quickForm"]/div[1]/div[11]/button')
        driver.execute_script("arguments[0].click();", next)

        ### 2nd step
        time.sleep(3)  # driver.implicitly_wait(10)
        # Country
        driver.find_element(by=By.XPATH, value='//*[@id="country_id"]/option[4]').click()
        # # Payment Method
        driver.find_element(by=By.XPATH, value='//*[@id="payment_term_id"]/option[4]').click()
        # Trade Terms
        driver.find_element(by=By.XPATH, value='//*[@id="trade_term_id"]/option[4]').click()
        # Currency
        driver.find_element(by=By.XPATH, value='//*[@id="currency_id"]/option[4]').click()
        # Shipping Method
        driver.find_element(by=By.XPATH, value='//*[@id="shipping_method_id"]/option[4]').click()
        # Available Data
        driver.find_element(by=By.XPATH, value='//*[@id="endDate"]').send_keys(next_week)
    else:
        # unit
        driver.find_element(by=By.XPATH, value='//*[@id="unit_id"]/option[2]').click()
        # Target Price
        driver.find_element(by=By.XPATH, value='//*[@id="target_price"]').send_keys(156123)
        # sourcing purpose
        driver.find_element(by=By.XPATH, value='//*[@id="source_propose_id"]/option[2]').click()
        # Company Certificate (!*)
        driver.find_element(by=By.XPATH, value='//*[@id="companyCertificate"]').send_keys(test_string)
        # Product Certificate (!*)
        driver.find_element(by=By.XPATH, value='//*[@id="productCertificate"]').send_keys(test_string)
        ### Description
        ifr = driver.find_element(by=By.ID, value='details_ifr')
        driver.switch_to.frame(ifr)                 # switch to iframe
        text_area = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
        text_area.clear()                           # clear the text area
        time.sleep(3)                               # wait for 5 sec
        text_area.send_keys(test_string)
        text_area.send_keys(Keys.ENTER)
        text_area.send_keys(test_string)
        driver.switch_to.default_content()          # return to original iframe
        time.sleep(3)                               # driver.implicitly_wait(3)
        # Upload Image
        driver.find_element(by=By.XPATH, value='//*[@id="file-upload"]').send_keys(image_path)
        # Press next
        next = driver.find_element(by=By.XPATH, value='//*[@id="quickForm"]/div[1]/div[11]/button')
        driver.execute_script("arguments[0].click();", next)

        ### 2nd step
        time.sleep(3)  # driver.implicitly_wait(10)
        # Country
        driver.find_element(by=By.XPATH, value='//*[@id="country_id"]/option[4]').click()
        # # Port destination
        driver.find_element(by=By.XPATH, value='//*[@id="port"]').send_keys(test_string)
        # # Payment Method
        driver.find_element(by=By.XPATH, value='//*[@id="payment_term_id"]/option[4]').click()
        # Trade Terms
        driver.find_element(by=By.XPATH, value='//*[@id="trade_term_id"]/option[4]').click()
        # Currency
        driver.find_element(by=By.XPATH, value='//*[@id="currency_id"]/option[4]').click()
        # Shipping Method
        driver.find_element(by=By.XPATH, value='//*[@id="shipping_method_id"]/option[4]').click()
        # Available Data
        driver.find_element(by=By.XPATH, value='//*[@id="endDate"]').send_keys(next_week)
        # Other Details
        time.sleep(3)                               # driver.implicitly_wait(3)
        iframe_other = driver.find_element(by=By.ID, value='other_requirements_ifr')
        driver.switch_to.frame(iframe_other)        # switch to iframe
        text_area_other = driver.find_element(by=By.XPATH, value='//*[@id="tinymce"]')
        text_area_other.clear()                     # clear the text area
        time.sleep(3)                               # driver.implicitly_wait(3)
        text_area_other.send_keys(test_string)
        text_area_other.send_keys(Keys.ENTER)
        text_area_other.send_keys(test_string)
        driver.switch_to.default_content()          # return to original iframe
        time.sleep(3)                               # driver.implicitly_wait(3)
    # # Press Submit
    # try:
    submit_final_rfq = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
    driver.execute_script("arguments[0].click();", submit_final_rfq)
    # except Exception as e:
        # print("Can't press Submit RFQ - Specific ❌❌❌")
        # sys.exit(1)
    # Confirm RFQ submition
    check_element_visability(page="Specific RFQ", text="Request has been sent successfully")