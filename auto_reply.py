import pyautogui
import pyperclip
import time
import copy
from tkinter import Tk
from configparser import ConfigParser


class AutoReply:
    def __init__(self):
        self.line_group_icon_img = 'data/icon.png'
        self.line_group_icon_highlight_img = 'data/icon_2.png'
        self.message_img = 'data/message_box.png'
        self.text_box_img = 'data/text_box.png'

        self.id_to_find = "14"
        self.id_to_replace = "23"
        self.name_to_find = "王曉明"
        self.name_to_replace = "廖登峰"
        self.status = "在家休息"
        self.phone = "096666666"

    def load_config(self, config_path):
        config = ConfigParser()
        config.read(config_path, encoding="utf-8-sig")

        self.id_to_find = config.get("main", "id_to_find")
        self.id_to_replace = config.get("main", "id_to_replace")
        self.name_to_find = config.get("main", "name_to_find")
        self.name_to_replace = config.get("main", "name_to_replace")
        self.status = config.get("main", "status")
        self.phone = config.get("main", "phone")

    def run(self):
        # find the line group by its icon
        location = pyautogui.locateCenterOnScreen(self.line_group_icon_img)
        if location is None:
            location = pyautogui.locateCenterOnScreen(self.line_group_icon_highlight_img)

        pyautogui.moveTo(location.x+100, location.y)
        pyautogui.doubleClick()

        # wait for window prompt
        time.sleep(0.5)

        # locate the message box location
        location = pyautogui.locateCenterOnScreen(self.message_img)
        print(location)

        pyautogui.leftClick(location.x, location.y)
        pyautogui.hotkey('end')

        # copy the message
        pyautogui.rightClick(location.x, location.y)
        pyautogui.moveTo(location.x+10, location.y+40)
        pyautogui.click()

        # get the message content from clipper board
        string = Tk().clipboard_get().split("\n\n")
        print(string)
        find_flag = False
        for i in range(len(string)):
            if string[i].find(self.id_to_find) is not -1:
                string_to_paste = copy.deepcopy(string[i])
                string_to_paste = string_to_paste.replace(self.id_to_find, self.id_to_replace, 1)
                string_to_paste = string_to_paste.replace(self.name_to_find, self.name_to_replace, 1)

                # find the status location and replace it
                p1 = string[i].find("\n") + len("\n")
                p2 = string[i].find("\n", p1)
                string_to_paste = string_to_paste.replace(string[i][p1:p2], self.status)

                # find the phone number and replace
                p3 = string[i].find("電話") + len("電話")
                string_to_paste = string_to_paste.replace(string[i][p3:], self.phone)

                print(string_to_paste)
                string.insert(i+1, string_to_paste)
                find_flag = True
                break
        if not find_flag:
            return False
        print(string)
        text = ""
        for s in string:
            # skip the last one
            if string.index(s) == len(string):
                break
            text += s + "\n\n"
        pyperclip.copy(text)

        location = pyautogui.locateCenterOnScreen(self.text_box_img)
        print(location)
        pyautogui.moveTo(location.x, location.y+100)
        pyautogui.click()

        pyautogui.hotkey('ctrl', 'v')

        # if the function works find, this comment can be removed.
        # pyautogui.hotkey('enter')
        return True


if __name__ == '__main__':
    ap = AutoReply()

    ap.load_config("config.ini")
    success = ap.run()

    if not success:
        print("can not find the keyword !")


