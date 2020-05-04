# %% md
## Set Root Directory and Out Directory

# %%

import os
import time

ROOT_DIR = os.path.abspath('')
OUT_DIR = os.path.join(ROOT_DIR, 'out')

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# %% md

## Load WebDriver for Chrome
# https://sites.google.com/a/chromium.org/chromedriver/downloads

# %%

DRIVER = os.path.join(ROOT_DIR, 'chromedriver_mac_81')

# %%
from selenium import webdriver

driver = webdriver.Chrome(DRIVER)

driver.implicitly_wait(3)

window = {}

window['main'] = driver.current_window_handle

# %% md

## Open Page

# %%

ECAMPUS = 'https://ecampus.ut.ac.kr'

# %%


driver.get(ECAMPUS)

# %% md
## Load Authentication Info

# %%
import json

SECRET_JSON = os.path.join(ROOT_DIR, 'secrets.json')

# %%

with open(SECRET_JSON) as f:
    secrets = json.load(f)

login_id = secrets["ID"]
login_pw = secrets["PW"]


# %% md
## Login

# %%

def logout():
    btn_logout = driver.find_element_by_id('btn_logout')
    btn_logout.click()


def login(_id, _pw):
    try:
        logout()
    except:
        pass

    # Enter Info
    input_id = driver.find_element_by_id('id')
    input_pw = driver.find_element_by_id('pass')

    input_id.send_keys(_id)
    input_pw.send_keys(_pw)

    # Login
    driver.execute_script('login_proc()')


# %%
time.sleep(2)
login(login_id, login_pw)

login_id, login_pw = (None, None)
time.sleep(3)
# %%

panel = driver.find_element_by_id('selfInfoAfter')
lecture_list = panel.find_element_by_class_name('lecInfo')

print(lecture_list)

lectures = lecture_list.find_elements_by_xpath("//a[contains(., '2020')]")

print(lectures)

# %% md

## Enter The Lecture

# %%

sample_lecture = lectures[0]

sample_lecture.click()

# %% md
# You can enter the 'lecture room' with path below.
# It will lead you to the lecture room of the last lecture you entered...
# %%

lecture_room_url = "https://ecampus.ut.ac.kr/lms/class/courseSchedule/doListView.dunet"

driver.get(lecture_room_url)
time.sleep(2)
# %% md

## Get courses list


# %%
# not_progressed_list = driver.find_elements_by_xpath("//td[contains(., 'not progressed')]")
current_courses_link = driver.find_elements_by_xpath("//a[contains(., 'Lecture view')]")
current_courses = [course_link.find_element_by_xpath("../..") for course_link in current_courses_link]

current_courses_data = []
titles = []
links = []
mins = []
for course in current_courses:
    datas = course.find_elements_by_tag_name('td')
    title = datas[1].text
    lecture_time = datas[2].text
    period = datas[3].text
    status = datas[4].text
    link = datas[5].find_element_by_class_name('lectureWindow')
    # link = datas[5]

    print(title, lecture_time, period, status, link)
    print()
    if status != "Complete":
        titles.append(title)
        links.append(link)
        mins.append(int(lecture_time[:-6]))

print(titles)

# %% md
## Check Study Time and Open Lecture Window

# %%
import tqdm

print('test')

links[0].click()
print("{} courses.".format(len(links)))
seconds = [minute for minute in mins]
for sec, title, link in tqdm.tqdm(zip(seconds, titles, links)):
    print("{} for {}minutes...".format(title, sec // 60))
    link.click()
    time.sleep(sec)
    time.sleep(3)
    window['lecture'] = driver.window_handles[-1]
    time.sleep(3)

    driver.switch_to.window(window['lecture'])
    time.sleep(5)
    if len(driver.window_handles) > 1:
        driver.close()
    window['lecture'] = None
    time.sleep(0.5)
    driver.switch_to.window(window['main'])
    print("Course End")

print("Finished.")

# %%


# sample_link = links[-1]
# sample_course = sample_link.find_element_by_xpath("../..")
# tds = sample_course.find_elements_by_tag_name('td')
# # sample_lecture_time = abcs[-1].find_element_by_name('td')[2][:-7]
# print(tds[1].text)

# TODO: "not progressed and lecture VIEW'

# sample_link.click()
# window['lecture'] = driver.window_handles[-1]
# time.sleep(5)
# %%
# window['lecture']

# %%
