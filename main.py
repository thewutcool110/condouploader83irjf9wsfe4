import discord
import requests
import unblacklister
import random
import time
import json
from discord.ext import commands
from linkvertise import LinkvertiseClient

# Loading names from the file
with open('names.txt', 'r') as f:
    names = [l.strip() for l in f.readlines()]

lvclient = LinkvertiseClient()
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
tok = ""  # Place your Discord token here

client.remove_command('help')


@client.event
async def on_ready():
    print("Online")


@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
async def upload(ctx):
    print("Someone executed the command")
    Loadingw = await ctx.send("Loading the command, please wait.")

    time.sleep(1)
    cleanCookies()

    with open("./cookies.txt", "r") as f:
        lines = f.readlines()
        cookie = lines[-1].strip()

    userId = requests.get("https://users.roblox.com/v1/users/authenticated", headers={'User-Agent': 'Roblox'},
                          cookies={'.ROBLOSECURITY': str(cookie)})

    if userId.status_code != 200:
        print("Failed to get User ID. Status code: " + str(userId.status_code))
        print("More info: " + userId.text)
        emb = discord.Embed(title="Sorry, this cookie has been banned!", description="Try again later.")
        await Loadingw.edit(embed=emb)
        return

    token_response = requests.post("https://auth.roblox.com/v2/login", headers={"X-CSRF-TOKEN": ""},
                                   cookies={".ROBLOSECURITY": cookie})

    if 'x-csrf-token' not in token_response.headers:
        print("CSRF Token not found in the response.")
        emb = discord.Embed(title="Error obtaining CSRF token!",
                            description="Couldn't obtain CSRF token from Roblox API.")
        await Loadingw.edit(embed=emb)
        return

    token = token_response.headers['x-csrf-token']

    cookies = {".ROBLOSECURITY": str(cookie)}
    headers = {"x-csrf-token": token, "user-agent": "Roblox/WinInet", "content-type": "application/json"}

    url = "https://apis.roblox.com/universes/v1/universes/create"
    payload = {"templatePlaceId": 95206881}
    response = requests.post(url, json=payload, headers=headers, cookies=cookies)

    if response.status_code != 200:
        print("Failed to create universe. Status code: " + str(response.status_code))
        print("More info: " + response.text)
        emb = discord.Embed(title="Failed to create game!", description="Try again later.")
        await Loadingw.edit(embed=emb)
        return

    emb = discord.Embed(title="Your game is being uploaded!", description="Your condo will be available shortly!")
    emb.color = discord.Color.blue()
    emb.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1208223884961128528/1209258184393359452/RYPL.gif?ex=65e64472&is=65d3cf72&hm=c5074e71901cee89228e4f95da5a909fac0aa25c02512114e8fa20846e69cef3&")
    Loadinga = await Loadingw.edit(embed=emb)

    game = {"RootPlaceId": response.json()["rootPlaceId"], "UniverseId": response.json()["universeId"]}

    print(f"Uploading as {userId.json()['name']} with token {token}, place {game['RootPlaceId']} and universe {game['UniverseId']}.")

    x = requests.patch(f"https://develop.roblox.com/v2/universes/{game['UniverseId']}/configuration",
                       data=json.dumps(
                           {"name": random.choice(names), "description": random.choice(names),
                            "universeAvatarType": "MorphToR6", "allowPrivateServers": True,
                            "privateServerPrice": 0, "permissions": {"IsThirdPartyPurchaseAllowed": True,
                                                                     "IsThirdPartyTeleportAllowed": True,
                                                                     "IsHttpsEnabled": True,
                                                                     "AllowStudioAccessToAPI": True}}),
                       headers=headers, cookies=cookies)

    if x.status_code != 200:
        print("Failed to set universe configuration. Status code: " + str(x.status_code))
        print("More info: " + x.text)
        emb = discord.Embed(title="Failed to set game configuration!", description="Try again later.")
        await Loadinga.edit(embed=emb)
        return

    time.sleep(1)

    url = f"https://develop.roblox.com/v2/places/{game['RootPlaceId']}/"
    config = {"name": random.choice(names), "description": random.choice(names), "maxPlayerCount": 100}
    x = requests.patch(url, data=json.dumps(config), headers=headers, cookies=cookies)

    if x.status_code != 200:
        print("Failed to set server size." + str(x.status_code))
        print("More info: " + x.text)
        emb = discord.Embed(title="Failed to set server size!", description="Try again later.")
        await Loadinga.edit(embed=emb)
        return

    time.sleep(1)

    url = f"https://develop.roblox.com/v1/universes/{game['UniverseId']}/activate"
    x = requests.post(url, data="[]", headers=headers, cookies=cookies)

    if x.status_code != 200:
        print("Failed to make universe public. Status code: " + str(x.status_code))
        print("More info: " + x.text)
        emb = discord.Embed(title="Failed to make game public!", description="Try again later.")
        await Loadinga.edit(embed=emb)
        return

    time.sleep(0.75)

    url = f"https://data.roblox.com/Data/Upload.ashx?assetid={game['RootPlaceId']}"
    headers = {"x-csrf-token": token, "user-agent": "Roblox/WinInet"}
    count = 0
    time.sleep(2)

    x = requests.post(url, data=bytearray(open("nigloo.rbxl", "rb").read()), headers=headers, cookies=cookies)

    emb = discord.Embed(title="Your game has been uploaded!", description="Check your DMs for your condo link!")
    emb.color = discord.Color.blue()
    emb.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1208223884961128528/1209258184393359452/RYPL.gif?ex=65e64472&is=65d3cf72&hm=c5074e71901cee89228e4f95da5a909fac0aa25c02512114e8fa20846e69cef3&")
    await Loadinga.edit(embed=emb)

    gameUrl = lvclient.linkvertise(651745, "https://www.roblox.com/games/" + str(game['RootPlaceId']))
    emb = discord.Embed(title="To play the game join it!.", description=f"Game: {gameUrl} Key: FunkoPop ")
    emb.color = discord.Color.blue()
    emb.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/1208223884961128528/1209258184393359452/RYPL.gif?ex=65e64472&is=65d3cf72&hm=c5074e71901cee89228e4f95da5a909fac0aa25c02512114e8fa20846e69cef3&")
    await ctx.author.send(embed=emb)


def cleanCookies():
    with open("./cookies.txt", "r") as f:
        lines = f.readlines()
    filtered = []
    for line in lines:
        cookie = line.strip()
        if not getUserId(cookie):
            continue
        filtered.append(line)
    with open("./cookies.txt", "w") as f:
        f.writelines(filtered)


def getXsrf(cookie):
    response = requests.post("https://auth.roblox.com/v2/login", headers={
        "X-CSRF-TOKEN": ""
    }, cookies={
        ".ROBLOSECURITY": cookie
    }).headers["x-csrf-token"]
    return response


def getUserId(cookie):
    xsrf = getXsrf(cookie)
    try:
        response = requests.get("https://users.roblox.com/v1/users/authenticated", headers={
            "x-csrf-token": xsrf,
            "User-Agent": "Roblox/WinINet"
        }, cookies={
            ".ROBLOSECURITY": cookie
        }).json()["id"]
    except Exception as e:
        return False
    return response


def filterFile():
    filteredData = []
    with open("./cookies.txt", "r+") as f:
        for line in f:
            parts = line.split(":")
            if len(parts) >= 4:
                filteredData.append(f"{parts[2].strip()}:{parts[3].strip()}")
        f.seek(0)
        f.truncate(0)
        for line in filteredData:
            f.write(f"{line}\n")
    return


filterFile()
client.run(tok)
