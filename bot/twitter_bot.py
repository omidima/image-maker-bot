from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException

from bot.utils.classes import TwitteDTO, TwitteInformationDTO, TwitterDataDTO, TwitterMetaDTO, TwitterUserDTO

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=./tmp")
options.add_argument(r"--profile-directory=Default")
options.add_argument(r"--disable-dev-shm-usage")
options.add_argument("--disable-headless")
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
# options.binary_location = "/usr/bin/chromium-browser"
options.headless = True
selenium_host = "http://185.208.172.37"
# options = webdriver.ChromeOptions()
driver = webdriver.Remote(command_executor=f"http://185.208.172.37:4444/wd/hub", options=options)
# driver = webdriver.Remote(
#     command_executor=f"{selenium_host}:4444/wd/hub",
#     options=
# )


def login():
    driver.get("https://twitter.com/i/flow/login")
    sleep(5)
    c =  None
    while c is None:
        sleep(1)
        c = driver.find_element(By.TAG_NAME,"input")

    sleep(1)
    c.send_keys("NarangiNet")
    sleep(1)
    driver.find_elements(By.XPATH,'//div[@role="button"]')[-2].click()

    sleep(5)
    c =  None
    while c is None:
        sleep(5)
        c = driver.find_element(By.XPATH,"//input[@name='password']")
        print(c)
    c.send_keys("Omid51172123")
    sleep(1)

    driver.find_elements(By.XPATH,'//div[@role="button"]')[-1].click()
    sleep(5)


def load_twitter():
    try:
        driver.get("https://twitter.com/")
    except InvalidSessionIdException:
        driver = webdriver.Remote(command_executor=f"{selenium_host}:4444/wd/hub", options=options)
        driver.get("https://twitter.com/")


def load_user_page(username:str):
    global driver

    try:
        driver.get("https://twitter.com/"+username)
    except InvalidSessionIdException:
        driver = webdriver.Remote(command_executor=f"{selenium_host}:4444/wd/hub", options=options)
        driver.get("https://twitter.com/"+username)

    sleep(1)

    body = driver.find_element(By.TAG_NAME,'body')
    # body.click()
    for i in range(20):
        body.send_keys(Keys.PAGE_DOWN)
    sleep(1)

    return True


def get_profile_information(username:str) -> TwitterUserDTO | None:
    # name = driver.find_elements(By.CSS_SELECTOR, ".css-901oao.r-1awozwy.r-1nao33i.r-6koalj.r-37j5jr.r-adyw6z.r-1vr29t4.r-135wba7.r-bcqeeo.r-1udh08x.r-qvutc0")[0].text
    try:
        bio = driver.find_element(By.XPATH, "//div[@data-testid='UserDescription']").text
        following = driver.find_elements(By.XPATH, "//a[@role='link']")[12].text
        follower = driver.find_elements(By.XPATH, "//a[@role='link']")[13].text
        return TwitterUserDTO(**{
            # "name": name,
            "bio": bio,
            "following": following,
            "follower": follower,
            "username": username
        })
    except:
        return None


def get_page_twittes(condition= None):

    items = driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
    twitts: list[TwitteDTO] = []
    index = 0
    for i in items:
        try: 
            text = i.find_elements(By.XPATH,"//div[@data-testid='tweetText']")[index].text
            engag = i.find_elements(By.XPATH,"//div[@role='group']")[index].get_attribute("aria-label").split(",")
            comments = "0"
            retwitts = "0"
            like = "0"
            imperation = "0"

            for i in engag:
                if ("views" in i):
                    imperation = i.split()[0]
                elif ("repost" in i):
                    retwitts = i.split()[0]
                elif ("likes" in i):
                    like = i.split()[0]
                elif ("reply" in i):
                    comments = i.split()[0]

            twitte_body = TwitteDTO(**{
                "likes":like,
                "comments":comments,
                "retwitte": retwitts,
                "imperation": imperation,
                "text": text,
            })

            if (condition != None) and condition(twitte_body) :
                twitts.append(twitte_body)
            elif (condition == None):
                twitts.append(twitte_body)
            else:
                pass

            index+=1
        except:
            print("error")
            index+=1
            pass

    retwitts_count = driver.find_elements(By.XPATH,"//span[@data-testid='socialContext']")
    twitts_count = len(twitts) - len(retwitts_count)
    return TwitteInformationDTO(twitts=twitts, meta=TwitterMetaDTO(**{
        "twitts" : twitts_count,
        "retwitts": len(retwitts_count),
        "last_twitte": twitts[0] if len(twitts) > 0 else None
    }))

def check_exists_hashtag(text:str,hashtag:str):
    if text.find(hashtag) > -1: 
        return True
    
    return False


def check_user_status(username:str, hashtag: str):
    load_user_page(username=username)

    user = get_profile_information(username=username)
    if (user is not None):
        twitts = get_page_twittes(condition=lambda x: check_exists_hashtag(x.text,hashtag))
    else:
        twitts = None

    return  TwitterDataDTO(user=user, timeline=twitts)