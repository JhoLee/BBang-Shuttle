import os
import json
import re
import subprocess
import time

from requests import get

from selenium import webdriver
import platform

# TODO: Seperate into 'utils.py' and 'Auto-attend.py'

LOG_LEVEL = 0
# 0: quiet
# 1: warn
# 2: warn + info
# 3: warn + info + save_log_to_log_path
LOG_PATH = ''

OS_LIST = {'Darwin': 'mac', 'Windows': 'win', 'Linux': 'lin'}
VER_LIST = ['80', '81', '83']

def download_driver_path(current_os, version):
    if not os.path.exists('src'):
        os.makedirs('src')
    extension = '.exe' if current_os == 'win' else ''
    path = os.path.join('src', 'chromedriver_{}_{}{}'.format(current_os, version, extension))
    if not os.path.exists(path):
        print("[INFO] Downloading driver from dropbox...", current_os, version)
        url = 'http://bit.ly/cd_{}_{}'.format(
            current_os, version)
        with open(path, 'wb') as f:
            response = get(url)
            f.write(response.content)
        subprocess.call(['chmod', '0755', path])

    return path


def load_webdriver(debug=False):
    current_os = OS_LIST[platform.system()]

    options = webdriver.ChromeOptions()

    driver = None

    for ver in VER_LIST:
        _path = download_driver_path(current_os, ver)
        driver = _load_driver(driver, _path, options, debug)

    return driver


def _load_driver(driver, _path, options, debug=False):
    if driver is None:
        if not debug:
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument('disable-gpu')

        try:
            driver = webdriver.Chrome(executable_path=_path, chrome_options=options)
        except:
            print("[DEBUG] Not match. Re-loading with another version.", _path)
            driver = None

        print(driver)
    return driver


def open_page(driver, path):
    driver.get(path)
    window = driver.current_window_handle

    return window


def load_auth_info(json_path):
    with open(json_path) as f:
        secrets = json.load(f)

        return secrets["ID"], secrets["PW"]


def login(driver, main_window, _id, _pw):
    try:
        logout(driver, main_window)
    except:
        pass

    print("[INFO] Login... id:", _id)
    input_id = driver.find_element_by_id('id')
    input_pw = driver.find_element_by_id('pass')

    input_id.send_keys(_id)
    input_pw.send_keys(_pw)

    # Login
    driver.execute_script('login_proc()')
    driver.implicitly_wait(13)

    print("[INFO] Hello,", _id)


def logout(driver, main_window):
    driver.switch_to.window(main_window)
    time.sleep(0.5)
    btn_logout = driver.find_element_by_id('btn_logout')
    btn_logout.click()
    time.sleep(0.5)


def change_display_language(driver, main_window, lang='english'):
    driver.switch_to.window(main_window)
    print("[INFO] Changing display-lanuage into English for qualified searching...")
    time.sleep(0.5)
    select_lang = driver.find_element_by_xpath("//select[@name='lang']/option[text()='ENGLISH']")
    select_lang.click()
    time.sleep(5)
    print("[INFO] Display-lanuage has been changed to English.")


def get_lectures(driver, main_window, year):
    print("[INFO] Crawling lectures info...")
    driver.switch_to.window(main_window)
    time.sleep(0.3)
    panel = driver.find_element_by_id('selfInfoAfter')
    lecture_list = panel.find_element_by_class_name('lecInfo')

    lectures = lecture_list.find_elements_by_xpath("//a[contains(., '{}')]".format(year))
    print("[INFO] You have {} lectures...".format(len(lectures)))
    for idx, lecture in enumerate(lectures):
        print('\t[{}] {}'.format(idx, lecture.text))
    time.sleep(0.3)
    return lectures


def open_lecture_room(driver, window, lecture):
    print("[INFO] Opening The Lecture Room for '{}'".format(lecture.text))
    driver.switch_to.window(window)
    time.sleep(0.3)

    lecture.click()
    time.sleep(0.5)

    lecture_room_url = 'https://ecampus.ut.ac.kr/lms/class/courseSchedule/doListView.dunet'
    driver.get(lecture_room_url)
    time.sleep(1)
    print("[INFO] Lecture room was opened.")


def get_current_courses(driver, main_window, lec):
    print("[INFO] Crawling courses...")
    driver.switch_to.window(main_window)
    time.sleep(0.3)
    open_lecture_room(driver, main_window, lec)

    change_display_language(driver, main_window, 'ENGLISH')

    current_courses_link = driver.find_elements_by_xpath("//a[contains(., 'Lecture view')]")
    current_courses = [course_link.find_element_by_xpath("../..") for course_link in current_courses_link]

    courses = []
    for course in current_courses:
        datas = course.find_elements_by_tag_name('td')
        title = datas[1].text
        lecture_time = datas[2].text
        period = datas[3].text
        status = datas[4].text
        link = datas[5].find_element_by_class_name('lectureWindow')

        if status != 'Complete':
            courses.append(
                {
                    'title': title,
                    'time': int(lecture_time[:-6]),
                    'period': period,
                    'status': status,
                    'link': link,
                }
            )
    print("[INFO] Finished to crawl courses.")
    if len(courses) == 0:
        print("[WARN] There are no unattended courses in this lecture!")
    else:
        print("[INFO] There are {} unattended courses.".format(len(courses)))
        print_courses_info(courses)
    return courses


def extract_progress(status):
    progress = re.findall('\d+', status)
    if len(progress) > 0:
        return int(progress[0])
    else:
        return 0


def compute_left_time(lecture_time, progress):
    """

    :param lecture_time:
    :param progress:
    :return:
    """
    time_left = lecture_time * (100 - progress) * 6 // 10

    return time_left


def print_courses_info(courses):
    for idx, course in enumerate(courses):
        progress = extract_progress(course['status'])
        course['time_left'] = compute_left_time(course['time'], progress)

        print("({})".format(idx))
        print("#" * 40)
        print("\ttitle:", course['title'])
        print("\ttime:", course['time'], 'Minutes')
        print("\tperiod:", course['period'].replace('\n', ' '))
        print("\tstatus:", course['status'])
        print("\ttime left: {} Minutes and {} Seconds".format(
            course['time_left'] // 60,
            course['time_left'] % 60))
        print("#" * 40)
        print()


def attend_courses(driver, window, courses):
    print("[INFO] Start to open courses.")

    driver.switch_to.window(window)
    time.sleep(0.3)
    for course in courses:
        attend_course(driver, window, course)

    print("[INFO] Finished traveling courses.")


def attend_course(driver, window, course):
    print("[INFO] Opening the course '{}' for {} min {} sec.".format(
        course['title'],
        course['time_left'] // 60,
        course['time_left'] % 60))
    driver.switch_to.window(window)
    time.sleep(0.3)

    # todo: Convert this code to use thread instead of `time.sleep()`
    course['link'].click()
    time.sleep(2)
    win_lec = driver.window_handles[-1]
    print("[INFO] It was opened. ")
    # Todo: Compute the ending time...
    print("[INFO] It will be finished at ??:??.")
    time.sleep((course['time_left'] + 2))
    driver.switch_to.window(win_lec)
    time.sleep(2)
    print("[INFO] Time Over!!")
    if len(driver.window_handles) > 1:
        driver.close()
    driver.switch_to.window(window)
    print("[INFO] Closed the course window.")


def log(message, type='INFO'):
    # Todo
    # example: "09:34:40 [INFO] Hello world"
    pass


if __name__ == "__main__":
    # TODO: Use argparser

    driver = load_webdriver(debug=False)
    driver.implicitly_wait(3)
    main_window = open_page(driver, 'https://ecampus.ut.ac.kr')

    SECRETS_JSON = 'secrets.json'
    login_id, login_pw = load_auth_info(SECRETS_JSON)
    login(driver, main_window, login_id, login_pw)

    lectures = get_lectures(driver, main_window, year=2020)
    lecture_range = range(len(lectures))

    choice = int(input("Select the number you want >> "))
    while choice not in lecture_range:
        print("[WARN] Please Enter a number from {}~{}".format(0, len(lectures) - 1))
        print()
        choice = int(input("Select the number you want >> "))
    lec = lectures[choice]

    courses = get_current_courses(driver, main_window, lec)

    attend_courses(driver, main_window, courses)

    driver.close()
