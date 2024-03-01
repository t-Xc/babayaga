import requests
import json
import tls_client

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Firefox";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

requests = tls_client.Session(client_identifier="chrome112",)

response1 = requests.get('https://api.prizepicks.com/projections')

prizepicks = response1.json()

request = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines")

underdog = request.json()

udlist = []
pplist = []
matchingnames = []

for appearances in underdog["over_under_lines"]:
    underdog_title = ' '.join(appearances["over_under"]["title"].split()[1:2])
    UDdisplay_stat = f"{appearances['over_under']['appearance_stat']['display_stat']}"
    UDstat_value = f"{appearances['stat_value']}"
    if UDdisplay_stat =='Kills on Map 1' or UDdisplay_stat == 'Kills on Map 1+2' or UDdisplay_stat== 'Kills in Game 1+2':
        uinfo = {"Name": underdog_title.lower(), "Stat": UDdisplay_stat, "Line": UDstat_value}
        udlist.append(uinfo)

for included in prizepicks['included']:
    PPname_id = included['id']
    PPname = included['attributes']['name'] 
    for data1 in prizepicks['data']:
        PPid = data1['relationships']['new_player']['data']['id']
        PPprop_value = data1['attributes']['line_score']
        PPprop_type = data1['attributes']['stat_type']
        if PPname_id == PPid and PPprop_type == 'MAPS 1-2 Kills' or PPprop_type == 'Map 1 Kills':
            ppinfo ={"Name": PPname.lower(), "Stat": PPprop_type, "Line": PPprop_value}
            pplist.append(ppinfo)

for udn in udlist:
    for ppn in pplist:
        if udn["Name"] == ppn["Name"]:
            final = {"Name": udn["Name"] , "Stat": udn["Stat"],"Underdog->": udn["Line"], "Prizepicks->": ppn["Line"] }
            matchingnames.append(final)
            print(final)
