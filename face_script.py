#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import selenium.webdriver
from selenium import common

WAIT_TO_LOAD = 3
SCROLL_NUMBER = 30

EMAIL = "__EMAIL__"
PASSWORD = "__PASS__"

if __name__ == '__main__':
    # Start Driver
    driver = selenium.webdriver.Firefox()

    # Facebook Login
    driver.get("http://facebook.com")
    user_field = driver.find_element_by_id("email")
    user_field.send_keys(EMAIL)
    user_field = driver.find_element_by_id("pass")
    user_field.send_keys(PASSWORD)
    login_button = driver.find_element_by_id("loginbutton")
    login_button.find_elements_by_tag_name('input')[0].click()

    # Remove Ads modals
    time.sleep(WAIT_TO_LOAD)
    try:
        driver.find_elements_by_class_name("_3ixn")[0].click()
    except:
        pass

    try:
        driver.find_elements_by_class_name("AdBox")[0].click()
    except:
        pass

    try:
        driver.find_elements_by_class_name("Ad")[0].click()
    except:
        pass

    try:
        driver.find_elements_by_class_name("advert")[0].click()
    except:
        pass

    # Scroll main page to load some posts
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for i in range(1, SCROLL_NUMBER):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(WAIT_TO_LOAD)
        print('scroll', i, '/', SCROLL_NUMBER)

    # Collect "Like" elements from posts
    likes = driver.find_elements_by_tag_name('a')
    main_likes = []
    for l in likes:
        try:
            # Criteria to find Facebook like button...
            # This changes all the time and need to be adjusted from time to time... Sad but TRUE
            if l.get_attribute('data-testid') == "UFI2ReactionLink":
                main_likes.append(l)
        except selenium.common.exceptions.NoSuchElementException:
            pass

    # Like Action Process, with some fallbacks
    for i, like in enumerate(main_likes):
        try:
            z = "arguments[0].setAttribute('style', 'position:relative;z-index:99999')"
            driver.execute_script(z, like)
            time.sleep(1)
            x = str(int(like.location['x']))
            y = str(int(like.location['y']))
            driver.execute_script("window.scrollTo(" + x + "," + y + ")")
            time.sleep(1)
            try:
                like.click()
            except Exception as err2:
                time.sleep(WAIT_TO_LOAD)
                try:
                    driver.find_elements_by_class_name('layerCancel')[0].click()
                except:
                    pass
                print("ERR 2:", err2)
        except Exception as err:
            time.sleep(WAIT_TO_LOAD)
            try:
                driver.find_elements_by_class_name('layerCancel')[0].click()
            except:
                pass
            print(err)

        print('like', i, '/', len(main_likes))

    driver.quit()
