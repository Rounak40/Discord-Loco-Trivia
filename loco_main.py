import requests
import json
import asyncio
from dhooks import Webhook, Embed
from datetime import datetime
from pytz import timezone
import pytz
import time
indianist = timezone('Asia/Kolkata')
global oldata
oldata = None


# input all datas
loco_bearer_token = "Bearer token example: xxxxxxxxxxxxxxxxxxxx"
webhook_url = "Webhook Url"

#############################

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
def getuser():
    req = requests.get("https://jsonblob.com/api/jsonBlob/5a7661d6-7fd5-11e9-8d0e-6fe578ed4135")
    try:
        data = req.json()
    except:
        data = {
        }
    return data

def fetch_data(oldata):
    print("Connected With Socket!")
    print("Welcome here! This is an alternative socket of Loco Trivia made by Rounak in Python!")
    while True:
        data = getuser()
        if data != oldata:
           # print(data)
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
            elif data["type"] == "QuestionSummary":
                correct = data["correct"]
                embed = Embed(title="Loco Trivia", description="Question Summary",color=0x4286f4)
                embed.add_field(name="Correct Answer", value=correct)
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
                hook.send(f"Next Game: {title}")
        oldata = data
while True:
    response_data = requests.get("http://api.getloconow.com/v1/contests/",headers={'Authorization': f"Bearer {loco_bearer_token}"}).json()
    if "invalid_grant" in response_data:
        print("Bearer token is not Valid!!")
        break
    re_time = indianist.localize(datetime.fromtimestamp(int(response_data['start_time']/1000))).replace(tzinfo=None)-datetime.now().replace(tzinfo=None)    
    sec = re_time.seconds
    if sec <= 600:
        print("Game is Live")
        fetch_data(oldata)
    print("Game not live sleeping for 5 min!")
    time.sleep(300)    
