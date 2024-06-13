import datetime
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import time
import io
import os
import re


#Katakana names for randomly generating names
japanese_names_katakana = [
    "アキラ", "アサミ", "アヤ", "アヤカ", "アユミ",
    "エミ", "カナ", "カナコ", "カズキ", "カズヤ",
    "カズヨシ", "カナエ", "キミコ", "ケンジ", "コウイチ",
    "コウジ", "サチコ", "サトシ", "ショウタ", "スミレ",
    "タイチ", "タカシ", "タクミ", "タツヤ", "タマキ",
    "チエ", "チカ", "トシユキ", "トモコ", "ナオ",
    "ナオキ", "ナオト", "ナツキ", "ナナ", "ナナコ",
    "ニイナ", "ネネ", "ノゾミ", "ハルカ", "ハルト",
    "ヒカル", "ヒサシ", "ヒロシ", "ヒロミ", "フミコ",
    "マイ", "マオ", "マサシ", "マサト", "マサヒロ",
    "マナ", "マユ", "マユコ", "マリ", "マリコ",
    "ミキ", "ミズキ", "ミナ", "ミナコ", "ミナミ",
    "ミホ", "ムツミ", "メグミ", "モモ", "モモカ",
    "ヤスコ", "ユイ", "ユウキ", "ユウジ", "ユウタ",
    "ユウト", "ユカ", "ユキ", "ユキコ", "ユミ",
    "ヨウコ", "リエ", "リカ", "リサ", "リツコ",
    "リョウタ", "リョウコ", "レイ", "レイコ", "レン",
    "ロウタ", "ワカナ", "ワタル", "イツキ", "イチロウ",
    "ウミ", "エイタロウ", "オサム", "カイ", "カイト",
    "カオリ", "カスミ", "ガクト", "キョウコ", "コウタロウ"
]

#Hiragana names for randomly generating names.
japanese_names_hiragana = [
    "あきら", "あさみ", "あや", "あやか", "あゆみ",
    "えみ", "かな", "かなこ", "かずき", "かずや",
    "かずよし", "かなえ", "きみこ", "けんじ", "こういち",
    "こうじ", "さちこ", "さとし", "しょうた", "すみれ",
    "たいち", "たかし", "たくみ", "たつや", "たまき",
    "ちえ", "ちか", "としゆき", "ともこ", "なお",
    "なおき", "なおと", "なつき", "なな", "ななこ",
    "にいな", "ねね", "のぞみ", "はるか", "はると",
    "ひかる", "ひさし", "ひろし", "ひろみ", "ふみこ",
    "まい", "まお", "まさし", "まさと", "まさひろ",
    "まな", "まゆ", "まゆこ", "まり", "まりこ",
    "みき", "みずき", "みな", "みなこ", "みなみ",
    "みほ", "むつみ", "めぐみ", "もも", "ももか",
    "やすこ", "ゆい", "ゆうき", "ゆうじ", "ゆうた",
    "ゆうと", "ゆか", "ゆき", "ゆきこ", "ゆみ",
    "ようこ", "りえ", "りか", "りさ", "りつこ",
    "りょうた", "りょうこ", "れい", "れいこ", "れん",
    "ろうた", "わかな", "わたる", "いつき", "いちろう",
    "うみ", "えいたろう", "おさむ", "かい", "かいと",
    "かおり", "かすみ", "がくと", "きょうこ", "こうたろう"
]

#Emojis to be randomly added to names.
emojis = ["🚀", "👀", "🎉", "🌟", "🌙", "⭐", "🍒", "🍂", "🔥", "💫", "🤗", "👈"]

def generate_display_name() -> str:
    """Randomly generates a name."""

    import random
    name_list = random.choice([japanese_names_hiragana, japanese_names_katakana])
    name = random.choice(name_list)

    # one third of the time, add an emoji
    if random.random() < 0.5:
        name += random.choice(emojis)
    return name

def generate_random_username(length=16) -> str:
    """
    Generates a random alphanumeric username.
    
    Args:
    length (int): Length of the username. Default is 8 characters.
    
    Returns:
    str: Randomly generated username.
    """
    characters = string.ascii_letters + string.digits  # Alphanumeric characters
    username = ''.join(random.choice(characters) for _ in range(length))
    return username


def generate_random_datetime() -> datetime:
    "Randomly generates a datetime to be set in the tweet."

    # Set year to 2022
    year = 2022

    # Randomly choose the month and day
    month = random.randint(1, 12)
    # Determine the last day in the selected month
    last_day = 31
    if month in [4, 6, 9, 11]:
        last_day = 30
    elif month == 2:
        last_day = 29 if year % 4 == 0 else 28
    day = random.randint(1, last_day)

    # Randomly choose the time between 8 AM (8*60 minutes) and 10 PM (22*60 minutes)
    minutes_since_midnight = random.randint(8 * 60, 22 * 60)
    hours, minutes = divmod(minutes_since_midnight, 60)

    # Create datetime object
    random_datetime = datetime.datetime(year, month, day, hours, minutes)

    # Format the datetime object to match the style "9:05 AM · Jul 7, 2022"
    formatted_datetime = random_datetime.strftime("%I:%M %p · %b %d, %Y")
    return formatted_datetime.strip()

def highlight_text(text):
    """Useful for picking out important text.
    
    When generating html, text enclosed in <h></h> will be highlighted.
    """

    return re.sub(r'<h>(.+?)</h>', r'<span class="highlight">\1</span>', text)

def generate_tweet_html(
        tweet_text,
        tweet_time = "") -> str:
    
    """For anonymizing Twitter data.
    
    Given text, will rancomly generate a name, username, and time, and set it inside
    the simulated tweet html.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Build the path to the default profile image
    profile_image_path = os.path.join(dir_path, 'default-pfp.png')
    tweet_time = generate_random_datetime()
    display_name = generate_display_name()
    username = generate_random_username()
    tweet_text = tweet_text.replace('\n', '<br>')

    
    # Highlight text enclosed in <h></h>
    tweet_text = highlight_text(tweet_text)
    
    tweet_html = f'''
    <html>
        <head>
            <style>
                .tweet {{
                    font-family: Arial, sans-serif;
                    border: 1px solid #e1e8ed;
                    border-radius: 10px;
                    padding: 10px;
                    max-width: 500px;
                    margin: 10px;
                    position: relative; /* For absolute positioning of the follow button */
                }}
                .tweet-header {{
                    display: flex;
                    align-items: center;
                }}
                .profile-image {{
                    border-radius: 50%;
                    width: 48px;
                    height: 48px;
                    object-fit: cover;
                }}
                .tweet-content {{
                    margin-left: 10px;
                }}
                .username {{
                    display: block; /* Make username appear on a new line */
                    color: #657786;
                }}
                .display-name {{
                    font-weight: bold;
                }}
                .timestamp {{
                    color: #657786;
                    font-size: 12px;
                    margin-top: 10px;
                }}
                .follow-button {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    padding: 5px 15px;
                    background-color: #1da1f2;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="tweet" id="tweet">
                <button class="follow-button">Follow</button>
                <div class="tweet-header">
                    <img src="{profile_image_path}" class="profile-image" alt="Profile Image">
                    <div class="tweet-content">
                        <span class="display-name">{display_name}</span>
                        <span class="username">@{username}</span>
                    </div>
                </div>
                <p>{tweet_text}</p>
                <div class="timestamp">{tweet_time}</div>
            </div>
        </body>
    </html>
    '''
    return tweet_html

def generate_tweet_png(
        text: str,
        tweet_id: str, 
        html_dir: str="html", 
        png_dir: str="png",
        tweet_time: str=""):
    """
    Pipeline for simulating a tweet.

    Args:
        text (str): Text to be set inside the simulated tweet.
        tweet_id (str): Filename with which to save the tweet.
        html_dir (str): Directory to save the html of the simulated tweet.
        png_dir (str): Directory to save the image of the tweet, which is the final output.

    """

    # Set up Selenium with a headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Generate the HTML and write it to a file
    html_content = generate_tweet_html(text, tweet_time=tweet_time)
    with open(f"{html_dir}/{tweet_id}.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    url = os.path.abspath(html_dir)
    url = os.path.join(url, f"{tweet_id}.html")

    # Load the HTML file
    driver.get(url)  # Update the path to your temp.html file
    time.sleep(2)  # Wait for it to render

    # Find the tweet element by id and take a screenshot of it
    tweet_element = driver.find_element(By.ID, "tweet")
    tweet_screenshot = tweet_element.screenshot_as_png

    # Convert screenshot to an Image object and save it as JPEG
    image_stream = io.BytesIO(tweet_screenshot)
    image = Image.open(image_stream)
    image.save(f"{png_dir}/{tweet_id}.png")

    # Clean up
    driver.quit()

    return 