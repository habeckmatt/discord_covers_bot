from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import discord
import os
from discord.ext import commands

## CHROME VERSION 131.0.6778.109

# Discord bot token and channel ID
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Configure Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = Service('/usr/lib/chromium-browser/chromedriver')

# Scraping function
def scrape_betting_lines():
    driver = webdriver.Chrome(service=service, options=options)
    try:
        url = "https://www.covers.com/picks/nfl"
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        # Find betting lines (update selector as needed)
        bets = driver.find_elements(By.CSS_SELECTOR, '.cover-CoversPicks-PickString')
        betting_lines = [bet.text for bet in bets]
        print(betting_lines)
        return betting_lines
    finally:
        driver.quit()

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Scrape data and post to Discord channel
    betting_lines = scrape_betting_lines()
    channel = bot.get_channel(CHANNEL_ID)

    if betting_lines:
        message = "Here are the latest betting lines:\n" + "\n".join(betting_lines)
    else:
        message = "No betting lines were found."

    if channel is not None:
        await channel.send(message)
        await bot.close()
    else:
        print("Channel not found or inaccessible.")
        bot.close()

# Run the bot
bot.run(DISCORD_TOKEN)
