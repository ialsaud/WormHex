import os
import re
from signal import raise_signal
import numpy as np
import argparse
import json

# INFO 
#       Logo ASCII

wormhex_logo ="""
          --::--.   --::--:
         +.     =..=:     -:.-:
        .+.   . =::=.   . --:+++:
         .--::--:=+:--:::--:+++++:
             .:-+-===-:::-=++++++=
             .+++=+=+++++++++=++++
         .     :=+++++++++=::=+++=
      .=+=                :=+++++:
     =+++           -==+++++++++=
    =++++.         =+++++++++++=
   .++++++-..--:.  ++++++++++++   ....    ....
   .++++++-=+++++:.+-------=++.-=+++++=-=+++++++-.
    =+++++-+++++.=++++==+++++:=++++++=-+++++++++++:
     :=++++++++:-+++++++++++::+++++++++++++++++++++.
                =++++++++++- ::::::::=+++++++++++++=
              .=+-::::::-+++++++++++++++++==+++++++=
             .++++++++++++-=+++++++=-++++++.=++++++:
             -++++++++++++=.++++++++ ++++++.=+++++:
             -++++++++++++-:+++++++=:+++++=-++++-.
              =+++++++++++-++++++++=+++++=::::.
               .:-=====-:::-----:.   ..
__          __                         _    _
\ \        / /                        | |  | |
 \ \  /\  / /   ___   _ __  _ __ ___  | |__| |  ___ __  __
  \ \/  \/ /   / _ \ | '__|| '_ ` _ \ |  __  | / _ \\\\ \/ /
   \  /\  /   | (_) || |   | | | | | || |  | ||  __/ >  <
    \/  \/     \___/ |_|   |_| |_| |_||_|  |_| \___|/_/\_\\
"""

wormhex_info = "WormHex is a tool for the Retrieval of Social Media Evidence from Volatile Memory."
wormhex_creators = """
Creators:
    * Wadha Almatter
    * Nora Almubairik
    * Amani Alqarni
    * Ibrahim Alsaud
"""

# OPTIONS
#       Select Memory Dump file to process
#       Select Application to be targetted (WhatsApp, Twitter, Telegram)
#       #TODO select output format (string, CSV)

# OUTPUT
#       output as json dump
#       #TODO output CSV, string

def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    # return string   
    return str1  


def print_output(results, output="json"):
    # TODO Requires Arabic printing
    if(output == "string"):
        print(results) #TODO
    elif(output == "csv"):
        print("Not implimented") #TODO
    elif(output == "json"):
        print(json.dumps(results, indent=4))
    else:
        print("Not recognized output type") #TODO

def main():
    parser = argparse.ArgumentParser(description=wormhex_info)
    parser.add_argument("-f", "--file", type=str, help="Memory dump file", required=True)
    parser.add_argument("-t", "--target", type=str, nargs="?", help="Target application: 'whatsapp', 'twitter', or 'telegram'", required=True, choices=[
            "whatsapp","twitter","telegram"], default="whatsapp")
    parser.add_argument("-o", "--output", type=str, nargs="?", help="Output format of the results", required=True, choices=[
            "string","csv","json"], default="json")
    
    args = parser.parse_args()

    try:
        memfile = open(args.file, 'rb')
    except OSError:
        print("Could not open/read file:", args.file)
        exit(1)
    memfile.close()

    print(wormhex_logo+"\n"+wormhex_creators)

    print('********************RESULTS********************')

    pathname = args.file
    my_file_handle=open(pathname,encoding='unicode_escape')
    mem = my_file_handle.read()
    application=args.target

    # remove
    results = {}
    line=['********************']

    # Whatsaap: Extract Mobile Numbers (Regex)
    if application == 'whatsapp':

        mobiles = re.findall(r'\d{12}@s.whatsapp.net',mem)
        if mobiles != None:
            mobiles = np.unique(re.findall(r'\d{12}',listToString(mobiles)))
 
        results['Mobile Numbers'] = mobiles.tolist()
        print_output(results, args.output)

    # Twitter: Extract info (Regex)
    if application=='twitter':

        # Tweets               
        tweets_regex = re.findall(r'"full_text":.*?,',mem)
        tweets = [re.sub(r'"full_text":','',i)  for i in tweets_regex]
        results['Tweets'] = tweets

        # Accounts Names
        name_regex = re.findall(r'"name":".*?,',mem)
        results['Accounts Names'] = name_regex

        # Screen Names
        screenName_regex = re.findall(r'"screen_name":".*?,',mem)
        results['Screen Names'] = screenName_regex

        # Tweets timestamp
        Account_regex = re.findall(r'"created_at.*?,',mem)
        results["Tweets Timestamp"] = Account_regex

        # Normal followers count
        followers_regex = re.findall(r'normal_followers_count.*?,',mem)
        results['Follower Count'] = followers_regex
        
        print_output(results, args.output)

    # Telegram: Extract info (Regex)
    if application=='Telegram':
        print(['***There is no data***'])


    print('**********************END**********************')
    exit(0)
    # end main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise(e)
    