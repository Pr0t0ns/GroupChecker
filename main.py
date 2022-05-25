from re import L
from tokenize import group
import httpx
import threading
import time 
import json
threads = 1
group_txt_position = 0
session_cookie = "RBXEventTrackerV2=CreateDate=5/25/2022 12:22:07 PM&rbxid=&browserid=134622368478; GuestData=UserID=-1510796024; _gcl_au=1.1.696737255.1653499329; RBXSource=rbx_acquisition_time=5/25/2022 12:32:43 PM&rbx_acquisition_referrer=&rbx_medium=Direct&rbx_source=&rbx_campaign=&rbx_adgroup=&rbx_keyword=&rbx_matchtype=&rbx_send_info=1; __utma=200924205.1725601436.1653499968.1653499968.1653499968.1; __utmc=200924205; __utmz=200924205.1653499968.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
def get_group():
    global group_txt_position
    file = open("groups.txt", "r+")
    data = file.readlines()
    file.close()
    current_line = 0
    for group in data:
        if current_line == group_txt_position:
            group_id = group
            group_txt_position += 1
            return group_id
        else:
            current_line += 1
    return data
def main():
    group_id = get_group()
    group_id = group_id.replace("https://www.roblox.com/groups/", "")
    group_id = group_id.replace("\n", "")
    api_url = f"https://groups.roblox.com/v1/groups/{group_id}"
    headers = {
        "cookie": session_cookie
    }
    group_request = httpx.get(api_url, headers=headers)
    if group_request.status_code == 404:
        print("Group Not Found!")
        return main()
    try:
        response = group_request.json()['owner']
        membercount = group_request.json()['memberCount']
    except KeyError:
        print("ratelimited sleeping!")
        time.sleep(240)
        print("KeyError Returning...")
        return main()
    if str(response) == "None":
       print(f"Found Group with id {group_id}\nMembers: {membercount}")
       file = open("found.txt", "r+")
       dataa = file.read()
       file.close()
       if f"https://www.roblox.com/groups/{group_id}/redirect" in dataa:
           print("Duplicate Group Found not adding to file!")
           return main()
       file = open("found.txt", "a+")
       file.write(f"https://www.roblox.com/groups/{group_id}/redirect" + "\n")
       file.close()
    else:
        print("Group already claimed")
    return main()

if __name__ == "__main__":
    for i in range(threads):
        threading.Thread(target=main).start()
