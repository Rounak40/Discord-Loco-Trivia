try:
    import requests
    import json
    import asyncio
    from dhooks import Webhook, Embed
    from datetime import datetime
    from pytz import timezone
    import pytz
    import time
    import discord
    from discord.ext.commands import Bot
    from discord.ext import commands
except Exception as e:
    print(str(e))

# input all datas

self_token = "self token"

loco_bearer_token = "Bearer token Example: xxxxxxxxxxxxxxxxxxxxxx"

webhook_url = "Discord webhook url"

Crowd_channels = ["xxxxxxxxxx","xxxxxxxxxxxxx"]

#############################


global counter1,counter2,counter3
counter1,counter2,counter3 = 0,0,0
global oldata
oldata = None
indianist = timezone('Asia/Kolkata')
client = discord.Client()

def getuser():
    req = requests.get("https://jsonblob.com/api/jsonBlob/5a7661d6-7fd5-11e9-8d0e-6fe578ed4135")
    try:
        data = req.json()
    except:
        data = {
        }
    return data


try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
    
async def fetch_data(oldata):
    global counter1,counter2,counter3
    print("Connected With Socket!")
    print("Welcome here! This is an alternative socket of Loco Trivia made by Rounak in Python!")
    while True:
        data = getuser()
        if data != oldata:
            if data["type"] == "starting":
                print('Game is Starting within 5m!')
                hook.send('Game is Starting within 5m!')
            elif data["type"] == "Question":
                question = data["q"]
                question_no = data["qnum"]
                options = [data["o1"],data["o2"],data["o3"]]
                embed = Embed(title=f"Q{str(question_no)} out of 10", description=question,color=0x4286f4)
                embed.add_field(name="Options", value=f"1. {options[0]}\n2. {options[1]}\n3. {options[2]}")
                embed.set_thumbnail(url="https://imgur.com/qeac0Ik.png")
                hook.send(embed=embed)
                counter1,counter2,counter3 = 0,0,0
                await asyncio.sleep(6)
                maxans = max(counter1,counter2,counter3)
                if maxans == counter1:
                    embed2 = Embed(title="**__Crowd:__**", description=":one:",color=0x4286f4)
                elif maxans == counter2:
                    embed2 = Embed(title="**__Crowd:__**", description=":two:",color=0x4286f4)
                else:
                    embed2 = Embed(title="**__Crowd:__**", description=":three:",color=0x4286f4)
                hook.send(embed=embed2)
                counter1,counter2,counter3 = 0,0,0
            elif data["type"] == "QuestionSummary":
                correct = data["correct"]
                embed = Embed(title="Loco Trivia", description="Question Summary",color=0x4286f4)
                embed.add_field(name="Correct Answer", value=correct )
                embed.set_thumbnail(url="https://imgur.com/qeac0Ik.png")
                hook.send(embed=embed)
            elif data["type"] == "GameSummary":
                number_of_winners = data["winners"]
                payout = data["payout"]
                embed = Embed(title="Loco Trivia", description=f"Game Summary",color=0x4286f4)
                embed.add_field(name="Winners", value=number_of_winners)
                embed.add_field(name="Payout", value="₹"+str(payout))
                embed.set_thumbnail(url="https://imgur.com/qeac0Ik.png")
                hook.send(embed=embed)
                break
            elif data["type"] == "waiting":
                title = data["game"]
                print(f"Next Game: {title}")
                hook.send(f"Next Game: {title}")
        oldata = data

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    client.loop.create_task(live_handling())

@client.event
async def on_message(message):
    global counter1,counter2,counter3

    if message.channel.id in Crowd_channels:
        content = message.content
        if "1" in content:
            if "n1" in content or "not1" in content:
                counter1 -= 800
            elif "apg" in content:
                counter1 += 850
            elif "?" in content:
                counter1 += 750
            else:
                counter1 += 800
        if "2" in content:
            if "n2" in content or "not2" in content:
                counter2 -= 800
            elif "apg" in content:
                counter2 += 850
            elif "?" in content:
                counter2 += 750
            else:
                counter2 += 800
        if "3" in content:
            if "n3" in content or "not3" in content:
                counter3 -= 800
            elif "apg" in content:
                counter3 += 850
            elif "?" in content:
                counter3 += 750
            else:
                counter3 += 800
                
loop = asyncio.get_event_loop()

async def live_handling():
    while not client.is_logged_in:
        time.sleep(10)
    while True:
        response_data = requests.get("http://api.getloconow.com/v1/contests/",headers={'Authorization': f"Bearer {loco_bearer_token}"}).json()
        if "invalid_grant" in response_data:
            print("Bearer token is not Valid!!")
            break
        re_time = indianist.localize(datetime.fromtimestamp(int(response_data['start_time']/1000))).replace(tzinfo=None)-datetime.now().replace(tzinfo=None)
        sec = re_time.seconds
        if sec <= 600:
            print("Game is Live")
            await fetch_data(oldata)
        print("Game not live sleeping for 5 min!")
        await asyncio.sleep(300)
        if not client.is_logged_in:
            return  

loop = asyncio.get_event_loop()
loop.create_task(client.start(self_token,bot=False))

while True:
    try:
        try:
            loop.run_forever()
        finally:
            loop.stop()
    except Exception as e:
       print("Event loop error:", e)
       
