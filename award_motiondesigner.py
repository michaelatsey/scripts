
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import logging
import gc
import os
import socket
import argparse

default_number_vote = 2000
default_url = 'https://africancreative.net/categorie-meilleur-motion-designer'
default_identifier ='choice-fdf3aee9-91fc-4394-93c9-49c64eb6b2ad-selector'

parser = argparse.ArgumentParser(description="Award script.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# bash or command line args
parser.add_argument('-v ','--vote', type=int, default=default_number_vote, help='number of votes (default: 2000 votes)')
parser.add_argument("-i", "--identifier", default=default_identifier, help="totalpoll canditate radio id")
parser.add_argument("--url", default=default_url, help="url of award")
args = parser.parse_args()
config = vars(args)

logging.basicConfig(filename='vote_motion_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
mService=Service(ChromeDriverManager().install())
i= 0
vote_current_index= 0

def change_tor_ip():
    password = "awardpassword"
    control_port = 9051
    command = f'AUTHENTICATE "{password}"\r\nSIGNAL NEWNYM\r\nQUIT\r\n'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", control_port))
        s.sendall(command.encode("utf-8"))

        response = s.recv(1024)
        if response.startswith(b"250 OK"):
            print("Tor IP changed successfully")
            logging.info("Tor IP changed successfully")
        else:
            print(f"Error changing Tor IP: {response.decode('utf-8').strip()}")
            logging.error(f"Error changing Tor IP: {response.decode('utf-8').strip()}")

    except socket.error as e:
        print(f"Socket error: {e}")
        logging.error(f"Socket error: {e}")


    finally:
        s.close()

def vote():
    global i
    global vote_current_index
    global config
        
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    #options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--start-maximized")
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    driver = webdriver.Chrome(service=mService, options=options)
    driver.get(config['url'])
    
    time.sleep(2)
    try:
        checkbox = driver.find_element(By.ID,config['identifier'])
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click(checkbox).perform()
        time.sleep(3)
        print("VOTE:" + str(vote_current_index))
        logging.info("VOTE:" + str(vote_current_index))
    except NoSuchElementException:
        i+= 1
        print("Nothing to click:" + str(i))
        logging.info("Nothing to click:" + str(i))
        change_tor_ip()
    finally:
        driver.quit()
        print("Driver quit: " + str(i))
        logging.info("Driver quit" + str(i))

    vote_current_index += 1


change_tor_ip()

for _ in range(config['vote']):
    vote()
