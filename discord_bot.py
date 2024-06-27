import discord
from discord.ext import commands
import cloudscraper
from bs4 import BeautifulSoup

# Configuration des intents
intents = discord.Intents.default()

# Créer le bot sans intents spécifiques
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def portal(ctx, server: str, portal: str):
    url = 'https://www.vulbis.com/portal.php'
    data = {
        'server': server,
        'portal': portal
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')

    server_info = soup.find('span', style="float:left;")
    portal_info = soup.find('span', style="float:right;")

    if server_info:
        server_info = server_info.contents[1].strip()
    else:
        server_info = "N/A"

    position = "N/A"
    if portal_info:
        portal_text = portal_info.text.strip()
        if ': ' in portal_text:
            portal_parts = portal_text.split(': ')
            if len(portal_parts) > 1:
                position_part = portal_parts[1]
                if '[' in position_part and ']' in position_part:
                    position = position_part[position_part.find('[') + 1:position_part.find(']')]

    time_info = "N/A"
    time_info_tag = soup.find('b', text="Actualisé : ")
    if time_info_tag:
        time_info = time_info_tag.next_sibling.strip()

    embed = discord.Embed(title="Portal Information", color=discord.Color.blue())
    embed.add_field(name="Server", value=server_info, inline=False)
    embed.add_field(name="Portal", value=portal, inline=False)
    embed.add_field(name="Position", value=position, inline=False)
    embed.add_field(name="Updated", value=time_info, inline=False)

    await ctx.send(embed=embed)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run("MTI1NTg5NjY4MTA4NjU4Mjg4Ng.GNLMTK.b8HwQFFQuMBtTp5LQR98t_9n2ux0MkgMvGrBk8")
