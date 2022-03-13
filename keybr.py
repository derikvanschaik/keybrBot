from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class KeybrBot:
    def __init__(self, driver):
        self.driver = driver 
    
    def go_homepage(self):
        self.driver.get("https://www.keybr.com/")
    
    def go_multiplayer(self):
        self.driver.get("https://www.keybr.com/multiplayer")
    
    def wait_for_multiplayer(self): 
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='GO!']")) 
            )
        finally:
            pass
    
    def multiplayer_loop(self):
        for i in range(10): 
            self.wait_for_multiplayer()
            print("done waiting!") 
            for key in self.get_keys(): 
                if key == ' ':
                    self.driver.find_element(by=By.TAG_NAME, value='input').send_keys(Keys.SPACE)
                else:
                    self.driver.find_element(by=By.TAG_NAME, value='input').send_keys(key)
                time.sleep(0.001) 

    # () -> [String] || void 
    # Purpose: Get words user must type 
    def get_word_list(self):
        driver = self.driver 
        class_mappings = {} # words that are to be typed all share the same class 
        for el in driver.find_elements(by=By.XPATH, value="//div/div/span"):   
            if el.get_attribute("class") not in class_mappings:
                class_mappings[el.get_attribute("class")] = [] 
            class_mappings[el.get_attribute("class")].append(el.text)

        for text_list in class_mappings.values(): 
            if '␣' in text_list[0]: # special char for space indicates that this is the list of words user needs to type 
                words = map(lambda string: string.replace("␣", " "), text_list) 
                return words

    def close_pop_up(self):
        self.driver.find_element(by=By.XPATH, value="//h1[text()='Learn to Type Faster']/../../a").click()
    
    # needs to be called before typing loop 
    def activate_input(self):
        self.driver.find_element(by=By.XPATH, value="//div[text()='Click to activate...']").click()

    # () -> [Chars] 
    def get_keys(self):
        keys = [] 
        for word in self.get_word_list():
            keys += list(word)
        return keys
    # loop num param is the number of times this will complete a full typing iteration. 
    def typing_loop(self, loop_num):
        for i in range(loop_num): 
            for key in self.get_keys(): 
                if key == ' ':
                    self.driver.find_element(by=By.TAG_NAME, value='input').send_keys(Keys.SPACE)  
                else:
                    self.driver.find_element(by=By.TAG_NAME, value='input').send_keys(key)
                time.sleep(0.07)       
            time.sleep(0.5)
    
    def terminate(self):
        self.driver.quit() 

def main():
    bot = KeybrBot(webdriver.Chrome())
    #example of multiplayer loop 
    bot.go_multiplayer()
    bot.multiplayer_loop()
    bot.terminate() 
    # wait for page to load
    # example of creating simple typing practice loop 
    '''
    bot.go_homepage()  
    time.sleep(0.5)  
    bot.close_pop_up() 
    time.sleep(0.5)
    bot.activate_input()
    time.sleep(0.5) 
    bot.typing_loop(15)    
    time.sleep(0.5)
    bot.terminate() 
    '''

if __name__ == '__main__':
    main() 