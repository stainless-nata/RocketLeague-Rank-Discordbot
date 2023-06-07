from discord.ext import commands
from discord import app_commands
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
import discord
import time
import os
import json

load_dotenv()

SCRAPE_URL = os.getenv('SCRAPE_URL')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def scrape_website(profile):
    # Set the browser options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Run the browser in headless mode
    # Instantiate the webdriver (replace with the correct webdriver for your browser)
    browser = webdriver.Chrome(options=options)

    width = 1920
    height = 2000
    browser.set_window_size(width, height)
    
    browser.get(f'{SCRAPE_URL}{profile}/overview')

    time.sleep(10)

    element = browser.find_element(By.CLASS_NAME, 'filters')
    grids = element.find_elements(By.TAG_NAME, 'ul')
    grid = grids[2].find_elements(By.TAG_NAME, 'li')
    try:
        grid[1].click()
    except WebDriverException:
        print("Element is not clickable")
    # print(grid[1].get_attribute('innerHTML'))
    time.sleep(10)

    # with open("output.txt", "w") as file:
    #     # Write data to the file
    #     file.write(addPlayer.get_attribute('outerHTML'))

    container = browser.find_elements(By.CLASS_NAME, 'container')
    
    browser.execute_script("window.scrollBy(0,500)","")
    width = 1920
    height = 2000
    browser.set_window_size(width, height)

    # Take a screenshot of the page and save it to disk
    container[0].screenshot('screenshot.png')

    # Quit the browser
    browser.quit()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await tree.sync()

@tree.command(name="rank", description="Show Rocket League Ranks")
async def rank(ctx, player_name:str):
    await ctx.response.defer()
    await scrape_website(player_name)
    file = discord.File('./screenshot.png', filename="screenshot.png")
    embed = discord.Embed(title="Rank", description="I found the following competitive ranks.", color=discord.Color.purple())
    embed.add_field(name='\nHead Up!', value='Use the `/link` slash command to save a default account.', inline=False)
    embed.set_image(url="attachment://screenshot.png")
    await ctx.followup.send(file=file, embed=embed)
    # await ctx.response.send_message(file=file, embed=embed)

client.run(DISCORD_BOT_TOKEN)

# kilroy_2