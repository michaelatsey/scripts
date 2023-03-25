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
import concurrent.futures
import logging

logging.basicConfig(filename='vote_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
mService=Service(ChromeDriverManager().install())
i= 0
vote_current_index= 0
def vote():
    global i
    global vote_current_index
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    options = Options()
    options.add_argument("--incognito")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    #options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-zygote")
    #options.add_argument("--single-process")

    # Configuration de Selenium et ouverture du navigateur
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(service=mService, options=options)
    driver.get("https://africancreative.net/categorie-meilleur-graphiste-designer")
    driver.maximize_window()
    try:
        checkbox = driver.find_element(By.ID,"choice-608f84f9-e44a-4e17-baaf-4f2e34c172d7-selector")
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click(checkbox).perform()
    except NoSuchElementException:
        i+= 1
        print("Nothing to click:" + str(i))
        logging.info("Nothing to click:" + str(i))
        time.sleep(1 * 60)
        
    # Fermer le navigateur
    vote_current_index += 1
    print("VOTE:" + str(vote_current_index))
    logging.info("VOTE:" + str(vote_current_index))
    time.sleep(1)
    driver.quit()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = [executor.submit(vote()) for _ in range(2000)]
