#!/usr/bin/python2

import swiftclient
import os, sys
import requests
import json
import pprint

data = file("../tokens.json")
tokens = json.load(data)

file_path = os.path.abspath(sys.argv[1])
file_name = os.path.basename(sys.argv[1])

# Fetching infos on the filename
episode = file(file_path);
episode_size = os.stat(file_path).st_size
episode_content = episode.read(episode_size)

# Uploading to Mixcloud
print "Uploading of " + file_name + " on Mixcloud started...";

files = {"mp3": open(file_path)}
url = "https://api.mixcloud.com/upload/"
params = {"access_token": tokens["mixcloud"]["test_token"]}
data = {"name": "Test API"}

r = requests.post(url, data=data, params=params, files=files)

if (r.status_code == 200):
    print "Upload to Mixcloud succeeded!"
else:
    print "Upload to Mixcloud failed with error code " + str(r.status_code) + " (" + r.reason + ")"
    exit(1)

# Connection

# Additional options
options = {}
options['tenant_id'] = tokens["openstack"]["tenant_id"]
options['region_name'] = tokens["openstack"]["region_name"]

client = swiftclient.client.Connection(tokens["openstack"]["auth_url"], tokens["openstack"]["username"], tokens["openstack"]["password"], 5, None, None, False, 1, 64, tokens["openstack"]["tenant_name"], options, '2')

# Uploading file
print "Uploading of " + file_name + " on OpenStack started..."
try:
    client.put_object("podcasts", file_name, episode_content, episode_size, None, None, "audio/mpeg")
except swiftclient.exceptions.ClientException as e:
    print "Error: Server responded to the PUT request on " + e.http_path + " with " + str(e.http_status) + " " + e.http_reason
    exit(1)

print "Upload to OpenStack succeeded!"
