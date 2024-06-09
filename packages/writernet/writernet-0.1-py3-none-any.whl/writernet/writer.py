# letter_writer/writer.py

import pyautogui
import random
import threading
import time
import logging

pyautogui.FAILSAFE = False

class LetterByLetterWriter:
    def __init__(self):
        self.input_text = ""
        self.current_index = 0
        self.running = False

    def start_writing(self, text):
        self.input_text = text
        self.current_index = 0
        self.running = True
        threading.Thread(target=self.write_text).start()

    def stop_writing(self):
        self.running = False

    def write_text(self):
        while self.running and self.current_index < len(self.input_text):
            letter = self.input_text[self.current_index]
            pyautogui.press(letter)
            if letter == '\n':
                pyautogui.press('home')
            interval = random.uniform(0.007, 0.5)
            time.sleep(interval)
            self.current_index += 1
        self.running = False

    def take_screenshot(self):
        try:
            screenshot_file = 'screenshot.png'
            pyautogui.screenshot(screenshot_file)
            return screenshot_file
        except Exception as e:
            logging.error("Failed to take screenshot", exc_info=True)
            raise e
