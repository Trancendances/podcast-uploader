# Trancendances podcasts uploader

This uploader (currently WIP) aims at providing an easy tool for podcasters to automatically upload their podcast to both Mixcloud and OpenStack.

## Configuration

In order to run this project correctly, you'll need a file named `tokens.json` at the root of the project's tree, omitted in this repository for obvious reasons, which should look like this:
```json
{
    "openstack": {
        "auth_url": "https://auth.cloud.ovh.net/v2.0/",
        "username": "YOUR_OPENSTACK_USERNAME",
        "password": "YOUR_OPENSTACK_PASSWORD",
        "region_name": "SBG1",
        "tenant_id": "YOUR_OPENSTACK_TENANT_ID",
        "tenant_name": "YOUR_OPENSTACK_TENANT_ID"
    },
    "mixcloud": {
        "prod_token": "A_MIXCLOUD_ACCESS_TOKEN",
        "test_token": "A_MIXCLOUD_ACCESS_TOKEN"
    }
}
```
For testing reasons, we have 2 Mixcloud accounts. The `prod_token` access token refers to our main one ("Trancendances") while the `test_token` one refers to another account which only exists for testing purposes. For now, the uploader isn't ready for production, so the Python script is set to use the test token by default.
