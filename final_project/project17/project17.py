import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("http://example.com")
time.sleep(1)
pass_element = driver.find_element_by_id('pass')

reg_texts = driver.find_elements_by_class_name('reg-text')

for reg_text in reg_texts:
    reg_text.send_keys(Keys.TAB)
    if reg_text.get_attribute("value").strip() == '':
        reg_text.parent_element.get_attribute("class").remove('reg-input-focus')
    else:
        reg_text.parent_element.get_attribute("class").add('reg-input-focus')
    user_agent = driver.execute_script("return navigator.userAgent")
    if 'Chrome' in user_agent:
        autofilled_inputs = driver.execute_script("return document.querySelectorAll('input:-webkit-autofill')")
        if len(autofilled_inputs) == 2:
            pass_element.parent_element.get_attribute("class").add('reg-input-focus')

name_element = driver.find_element_by_id('name')
name_element.send_keys(Keys.TAB)
driver.quit()
