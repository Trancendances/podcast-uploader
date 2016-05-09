#!/usr/bin/python2
#Dasporal 

import swiftclient
import os, sys, mimetypes
import requests
import json
import pprint


data = file(os.path.join(sys.path[0], "../tokens.json"))
tokens = json.load(data)

if len(sys.argv) != 2 or len(sys.argv) != 3:
    print ("Usage: podcast_upload.py [audio file name]")
    exit(1)

# Fetching infos on the file path
file_path = os.path.abspath(sys.argv[1])
file_name = os.path.basename(sys.argv[1])

# Opening file
try:
    episode = open(file_path)
except IOError:
    print ("File ", file_path, " not found.")
    exit(1)

# Uploading to Mixcloud
print ("Uploading of ", file_name, " on Mixcloud started...")
# Filling the requests parameters
files = {"mp3": episode}
url = "https://api.mixcloud.com/upload/"
params = {"access_token": tokens["mixcloud"]["test_token"]}
data = {"name": "Test API"}
# API request
r = requests.post(url, data=data, params=params, files=files)
# Error handling
if (r.status_code == 200):
    print ("Upload to Mixcloud succeeded!")
else:
    print ("Upload to Mixcloud failed with error code ", str(r.status_code), " (", r.reason, ")")
    exit(1)

# OpenStack
# Setting options
options = {}
options['tenant_id'] = tokens["openstack"]["tenant_id"]
options['region_name'] = tokens["openstack"]["region_name"]
# Opening connection
client = swiftclient.client.Connection(tokens["openstack"]["auth_url"], tokens["openstack"]["username"], tokens["openstack"]["password"], 5, None, None, False, 1, 64, tokens["openstack"]["tenant_name"], options, '2')
# Getting infos on the file
episode_size = os.stat(file_path).st_size
episode_content = episode.read(episode_size)
# Uploading
print ("Uploading of ", file_name, " on OpenStack started...")
try:
    client.put_object("podcasts", file_name, episode_content, episode_size, None, None, "audio/mpeg")
except swiftclient.exceptions.ClientException as e:
    print ("Error: Server responded to the PUT request on ", e.http_path, " with ", str(e.http_status), " ", e.http_reason)
    exit(1)

print ("Upload to OpenStack succeeded!")
