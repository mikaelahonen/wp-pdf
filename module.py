import sys
import logging
import time
import pdfkit

import config

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions

#Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(".", "log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

#Variables
file_count = {
    "img": 0,
    "pdf": 0,
    "html": 0,
}

def create_driver():

    options = Options()
    options.add_argument('-headless')

    #executable_path= for the driver path
    driver = webdriver.Firefox(options=options)

    logger.info('Driver initialized')

    return driver

def fix_html(html):

    protocol = config.post_url.split("://")[0]
    #Single quotes
    html = html.replace('="//', '="{}://'.format(protocol))
    #Double quotes
    html = html.replace("='//", "='{}://".format(protocol))

    return html


def export(driver, extension="png", name="", data="", url="", full_screen=False):

    #Get file type
    folder = {
        "png": "img",
        "jpg": "img",
        "html": "html",
        "pdf": "pdf",
    }
    file_type = folder[extension]

    #Increase the file count
    file_count[file_type] += 1
    cnt = str(file_count[file_type]).zfill(2)

    #Create file path
    f_path = "{}{}/{}_{}.{}".format(config.export_dir, file_type, cnt, name, extension)

    if file_type == "img":
        if not full_screen:
            driver.save_screenshot(f_path)
        else:
            f_img = open(f_path, 'wb')
            f_img.write(data)
            f_img.close()
    elif file_type == "pdf":
        pdfkit.from_url(url, f_path)
    elif file_type == "html":
        f_html = open(f_path, 'w')
        f_html.write(data)
        f_html.close()

    logger.info('Exported file {}'.format(f_path))

    return f_path

def enter_credentials(driver):
    #Go to wordpress login page
    driver.get(config.login_url)
    driver.find_element_by_id(config.wp_user_id).send_keys(config.user)
    driver.find_element_by_id (config.wp_pswd_id).send_keys(config.pswd)
    export(driver, 'png', 'wp_credentials')
    logger.info("Entered wp user and password")

    return driver

def login(driver):

    #Log in to Wordpress
    driver.find_element_by_id(config.wp_submit_id).click()
    logger.info("Clicked login button")
    logger.info("Trying login, max retries: {}".format(config.max_retries))

    #Go to the post
    attempt = 0
    again = True


    while (attempt < config.max_retries) and again:

        attempt += 1
        export(driver, "png", 'wp_login')

        try:
            #driver.get(config.login_url)
            driver.find_element_by_id(config.wp_submit_id)
            wait_time = attempt * config.timeout_factor
            logger.info("Login failed, waiting {} seconds".format(wait_time))
            time.sleep(wait_time)
            again = True
        except exceptions.NoSuchElementException:
            logger.info("Login successful")
            again = False


    return driver

def save_post(driver):

    driver.get(config.post_url)

    #Get page source
    post_source = driver.page_source#find_element_by_id(wp_post_id).get_attribute('innerHTML')
    post_source = fix_html(post_source)
    screenshot_data = driver.find_element_by_tag_name('body').screenshot_as_png
    logger.info("Crawled blog post content")

    #Export
    export(driver, "png", 'wp_post_screen')
    export(driver, "png", 'wp_post_full', data=screenshot_data, full_screen=True)
    html_path = export(driver, "html", "wp_post", data=post_source)
    export(driver, "pdf", "wp_post", url=html_path)

    return driver

def kill_driver(driver):
    driver.quit()
    logger.info("Killed the browser driver")
    return True
