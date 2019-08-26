#Import python libraries
import time

#Load config
from module import *

if initialize():

    #Initialize selenium driver
    driver = create_driver()

    driver = enter_credentials(driver)
    driver = login(driver)
    driver = save_post(driver)

    kill_driver(driver)
