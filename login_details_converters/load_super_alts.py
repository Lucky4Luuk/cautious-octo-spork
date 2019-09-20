# For people who got their alts from superalts x)

import json

login_details = []

print("Loading login details...")

with open("super_alts_login.txt") as f :
    lines = f.readlines()

print("Processing lines...")
for line in lines :
    split_string = line.split(":")
    login = {}
    login["email"] = split_string[0].rstrip()
    login["passwd"] = split_string[1].rstrip()
    if len(split_string) == 3 : #If you download the login details from superalts, this third variable is never included, but perhaps people want to add the username
        login["name"] = split_string[2].rstrip()
    else :
        login["name"] = "Unknown"
    login_details.append(login)

print("Writing login details")
f = open("login_details.json", "a") #Creates the file if it doesn't exist yet
f.close()
with open("login_details.json", "r+") as f :
    f.truncate() #Empty the file
    f.write(json.dumps(login_details, indent=4, sort_keys=True))

print("Done!")
