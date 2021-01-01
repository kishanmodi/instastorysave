import telebot,time,os
from selenium import webdriver
from flask import Flask, request

'''
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
'''

#web_browser modeule part
chrome_options = webdriver.ChromeOptions()
CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = 'C:\\APPDATA\\Python\\chromedriver.exe'
#WINDOW_SIZE = "1920,1080"
#chrome_options.add_argument("--headless")
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)

bot_token ="bot_token"
bot = telebot.TeleBot(token=bot_token)

#server = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Welcome To Instagram Image Downloader Bot\n     Only Send Username Or Profile Link  ")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'Use //stop Command to stop downloading Pictures \nDon\'t Send Private Profiles')

@bot.message_handler(commands=['xstop'])
def send_stop(message):
    bot.reply_to(message,'Stopped Downloading Images')

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
username.clear()
password.clear()
username.send_keys('username')
password.send_keys('pwd')
time.sleep(3)
driver.find_element_by_class_name('Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB').click()
time.sleep(3)


@bot.message_handler(func = lambda msg: msg.text!="stop")
def at_answer(message):
    try:
        url="https://www.instagram.com/stories" +"/" + message.text
        driver.get(url)   
        print(str(driver.current_url))   
        time.sleep(3)  
        driver.find_element_by_class_name('_42FBe').click()
        try:
            for x in range(100):
                video_id=driver.find_element_by_xpath("//div/div/video/source").get_attribute('src')
                img_id=driver.find_element_by_xpath("//div/div/img").get_attribute('src')
                print(type(img_id))
                print(type(video_id))
                if not video_id:
                    bot.send_photo(message.chat.id,img_id)
                else:
                    bot.send_video(message.chat.id,video_id)
                driver.find_element_by_class_name('FhutL').click()
        except:
            bot.send_message(message.chat.id,"Thank You")
    except:
        bot.send_message(message.chat.id,"No Stories available")
    
    
    
'''
@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200   

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your.herokuapp.com/' + bot_token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
'''

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
