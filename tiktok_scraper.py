from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        # Changes per tiktok page
    }

    headers = {
        # Changes per tiktok page
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': '', 
    }
    
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

print("STEP 1: Open Chrome browser")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.get("x") #input link of tiktok page


time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

className = "tiktok-1s72ajp-DivWrapper"

script  = "let l = [];"
script += "document.getElementsByClassName(\""
script += className
script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

urlsToDownload = driver.execute_script(script)

print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    downloadVideo(url, index)
    time.sleep(10)
