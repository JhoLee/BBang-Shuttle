import datetime
import re
import sys
import time

from sources.utils import check_os, check_chrome_version, load_webdriver, load_auth_info

ECAMPUS_PATH = {
    'MAIN': 'https://ecampus.ut.ac.kr',
    'LECTURE_ROOM': 'https://ecampus.ut.ac.kr/lms/class/courseSchedule/doListView.dunet'
}


class EcampusManager(object):


    def __init__(self, debug=False, show_chrome=False):
        """

        :param debug:
        :param show_chrome:
        """
        self.__id = None
        self.__pw = None

        # system
        self.os = check_os()
        self.version = check_chrome_version(self.os)

        # selenium
        self.driver = load_webdriver(show_chrome)
        self.main_window = None

        # list
        self.lecture = None
        self.course = None

        # current status
        self.lectures = []
        self.courses = []  # 전체 코스 목록
        self.attendable_courses = [] # 출석해야 하는 코스 목

        # log
        self.logs = []
        self.log_level = 2
        self.language = 'KOREAN'
        self.msg = self.message()

        if debug:
            self.log_level = 3
        else:
            self.log_level = 2

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def pw(self):
        return self.__pw

    @pw.setter
    def pw(self, value):
        self.__pw = value

    def log(self, message, level='INFO'):
        """
        Push messages into a list(queue).
        self.log_level define how deep to show.
        :param message: message to log.
        :param level: log level
        :type message: str
        :type level: str or int
        """

        LOG_LEVEL = {'NONE': 0, 'WARN': 1, 'INFO': 2, 'DEBUG': 3}
        if isinstance(level, str):
            _level = LOG_LEVEL[level.upper()]
        elif isinstance(level, int):
            _level = level
        else:
            _level = 0
        message = "({:%H:%M:%S}) [{}] {}".format(datetime.datetime.now(), level, message)
        if _level <= self.log_level:
            self.logs.append(message)
        print(message)

    def open_page(self, path):
        self.driver.get(path)
        window = self.driver.current_window_handle

        return window

    def open_main(self):
        """
        Open main page (https://ecampus.ut.ac.kr)
        After open, save this winodw to self.main_window
        """
        if self.main_window is not None:
            self.driver.switch_to.window(self.main_window)
            time.sleep(1)
        self.driver.get(ECAMPUS_PATH['MAIN'])
        time.sleep(3)
        self.main_window = self.driver.current_window_handle

        self.log("Opened main page.", 'DEBUG')

    def login(self):
        """
        Login with self.id, self.pw
        """
        self.open_main()
        try:
            self.logout()
        except:
            pass

        self.log("{} ID: {}".format(self.msg['LOGIN_TRY'], self.id), 'DEBUG')
        input_id = self.driver.find_element_by_id('id')
        input_pw = self.driver.find_element_by_id('pass')

        input_id.send_keys(self.id)
        input_pw.send_keys(self.pw)

        self.driver.execute_script('login_proc()')
        time.sleep(7)

        self.log("{}, {}".format(self.msg['HELLO'], self.id))

    def login_check(self):
        self.log("Checking login...", 'debug')
        msg = ''
        try:
            alert = self.driver.switch_to_alert()
            msg += alert.text
            self.log("Login Failed.", 'debug')
            self.log(msg, 'debug')
            alert.accept()
            is_success = False
        except:
            self.log("Login Success!", 'debug')
            is_success = True

        return is_success,  msg

    def logout(self):
        self.driver.switch_to.window(self.main_window)
        time.sleep(1)

        self.driver.find_element_by_id('btn_logout').click()

        time.sleep(1)
        self.log("{}".format(self.msg['LOGOUT_SUCCESS']), 'DEBUG')

    def change_display_language(self, lang='english'):
        """
        Change display-language into English to find elements by text.
        :param lang:
        """
        self.log("Changing display-language into English for qualified action...", 'debug')
        time.sleep(1)

        select_lang = self.driver.find_element_by_xpath("//select[@name='lang']/option[text()='ENGLISH']")
        select_lang.click()
        time.sleep(5)
        self.log("Display-language has been changed to {}".format(lang), 'debug')

    def get_lectures(self, year):
        """
        Get lecture list from panel, and save them to self.lectures
        :param year: A keyword to find lecture.
        """
        self.log("Crawling lectures info...", 'DEBUG')
        self.driver.switch_to.window(self.main_window)
        time.sleep(3)
        panel = self.driver.find_element_by_id('selfInfoAfter')
        lecture_list = panel.find_element_by_class_name('lecInfo')

        self.lectures = lecture_list.find_elements_by_xpath("//a[contains(., '{}')]".format(year))
        self.log("{} {}".format(self.msg['COURSES_TO_ATTEND'], len(self.lectures)), 'info')

    def open_lecture(self, lecture_idx):
        self.lecture = self.lectures[lecture_idx]
        lecture_name = self.lecture.text
        self.log("Opening the lecture room for '{}'.".format(lecture_name), 'DEBUG')
        self.driver.switch_to.window(self.main_window)
        time.sleep(1)

        self.lecture.click()
        time.sleep(3)

        self.driver.get(ECAMPUS_PATH['LECTURE_ROOM'])
        time.sleep(3)

        self.log("Lecture room for '{}' was opened.".format(lecture_name), 'DEBUG')

    def get_attendable_courses(self, lecture_idx):
        self.log("Crawling attendable courses...", 'DEBUG')
        self.driver.switch_to.window(self.main_window)
        time.sleep(2)

        self.open_lecture(lecture_idx)

        self.change_display_language('English')

        attendable_courses_link = self.driver.find_elements_by_xpath("//a[contains(., 'Lecture view')]")
        attendable_courses = [course_link.find_element_by_xpath(".../..") for course_link in attendable_courses_link]

        # self.courses = []
        for course in attendable_courses:
            datas = course.find_elements_by_tag_name('td')

            title = datas[1].text
            lecture_time = datas[2].text
            period = datas[3].text
            status = datas[4].text
            link = datas[5].find_element_by_class_name('lectureWindow')

            if status != 'Complete':
                self.attendable_courses.append(
                    {
                        'title': title,
                        'time': int(lecture_time[:-6]),
                        'period': period,
                        'status': status,
                        'link': link,
                    }
                )

        self.log("Finished to crawl courses.", 'DEBUG')

        if len(self.attendable_courses) == 0:
            self.log("더 이상 출석할 강의가 없습니다!", 'info')
        else:
            self.log("출석해야할 강의 수: {}".format(len(self.attendable_courses)))
            # self.print_courses_info()
            # TODO: Replace with printing in GUI.
            # Example
            """
            ###########################################
                title: 'Computer Vision'
                time: 50 Minutes
                period: 2020.05.04 ~ 2020.05.08
                status: not progressed
                time left: 50 Minutes and 0 Seconds
            ############################################
            """

    def attend_course(self, course_idx):
        # self.course = self.courses[course_idx]
        self.course = self.attendable_courses.pop(course_idx)
        self.log("Opening the course '{}' for {} min {} sec.".format(
            self.course['title'],
            self.course['time_left'] // 60 + 2,
            self.course['time_left'] % 60))
        self.driver.switch_to.window(self.main_window)
        time.sleep(2)

        self.attend_time = time.time()
        self.finish_time = (self.attend_time + self.course['time_left']) + 120
        finish_time = time.gmtime(self.finish_time)
        finish_time = "{}:{}".format(finish_time.tm_hour, finish_time.tm_min)

        self.course['link'].click()
        time.sleep(4)

        self.lecture_window = self.driver.window_handles[-1]
        self.log("Lecture opened. It will be finished at {}".format(finish_time), 'debug')
        # TODO: Convert to thread.
        # TODO: Or while loop..?
        # Todo: Or checking main's remain time
        time.sleep(self.course['time_left'])

        self.driver.switch_to.window(self.lecture_window)
        time.sleep(3)
        self.log("Time Over!!", "debug")
        if len(self.driver.window_handles) > 1:
            self.driver.close()
        self.driver.switch_to.window(self.main_window)
        self.log("{} '{}'".format(self.msg['COURSE_END'], self.course.text), 'info')

    def attend_all_courses(self):
        self.log("Attending all courses in the lecture..", 'debug')
        self.driver.switch_to.window(self.main_window)
        self.driver.implicitly_wait(1)
        for idx, course in enumerate(self.attendable_courses):
            self.attend_course(idx)

        self.log("현재 강의 내의 모든 영상 출석 완료!", 'info')


    @staticmethod
    def extract_progress(status: str):
        progress = re.findall('\d+', status)
        if len(progress) > 0:
            return int(progress[0])
        else:
            return 0

    @staticmethod
    def compute_left_time(lecture_time, progress):
        time_left = lecture_time * (100 - progress) * 6 // 10

        return time_left

    def message(self):
        language_order = {'KOREAN': 0, 'ENGLISH': 1}
        _lang = language_order[self.language]

        messages = {
            'LOGIN_TRY': [
                "로그인 시도중...",
                "Loggin in..."
            ],
            'LOGIN_SUCCESS': [
                "로그인 되었습니다.",
                "Logged in.",
            ],
            'LOGOUT_SUCCESS': [
                "로그아웃 되었습니다.",
                "Logout success.",
            ],
            'HELLO': [
                "안녕하세요",
                "Hello",
            ],
            'COURSES_TO_ATTEND': [
                "출석해야 하는 강의 수:",
                "Courses to attend:"
            ],
            'COURSE_END': [
                "강의가 끝났습니다.",
                "Course ended.",
            ],



        }

        messages = {key: message[_lang] for key, message in messages.items()}

        return messages

if __name__ == "__main__":
    print("Testing...")

    manager = EcampusManager(debug=True, show_chrome=False)

    sj = 'secrets.json'

    manager.id, manager.pw = load_auth_info(sj)
    manager.login()

    manager.get_lectures(year=2020)
    lecture_range = range(len(manager.lectures))

    choice = int(input("Select the number you want to attend >> "))
    while choice not in lecture_range:
        manager.log("Please enter a number in {}~{}".format(0, len(manager.lectures) - 1), 'warn')
        choice = int(input("Select the number you want >> "))

    manager.get_attendable_courses(lecture_idx=choice)
    if len(manager.courses) > 0:
        manager.attend_course(course_idx=0)
    print("Finish.")

    manager.driver.close()
    sys.exit()
