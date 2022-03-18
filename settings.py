
import os

from selenium import webdriver
from selenium.webdriver import Chrome
from seleniumrequests import RequestsSessionMixin
from selenium.webdriver.chrome.service import Service


class WebbDriver(RequestsSessionMixin, Chrome):
    ...


TOKEN = '5009247867:AAHRUCNK8v_yaSjzycUiTH0iUXMWRsILDs0'

options = webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=800,600")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")
DRIVER = WebbDriver(service=Service(executable_path=rf"{os.getcwd()}\chromedriver.exe"), options=options)

print()
