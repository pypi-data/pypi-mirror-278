import json
import requests
from msal import ConfidentialClientApplication

class MicrosoftTeams:
    def __init__(self, url: str):
        self.url = url

    def get_access_token_ropc(self, tenant_id, client_id, client_secret, username, password):
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]
        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret,
        )
        result = app.acquire_token_by_username_password(
            username=username,
            password=password,
            scopes=scope
        )
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Could not obtain access token: {result.get('error')}, {result.get('error_description')}")

    def get_team_id(self, access_token, team_name):
        url = "https://graph.microsoft.com/v1.0/groups"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        params = {
            '$filter': f"displayName eq '{team_name}' and resourceProvisioningOptions/Any(x:x eq 'Team')"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            teams = response.json().get('value', [])
            if teams:
                return teams[0]['id']
            else:
                raise Exception("Team not found.")
        else:
            raise Exception(f"Failed to get team ID: {response.status_code}, {response.text}")

    def get_channel_id(self, access_token, team_id, channel_name):
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            channels = response.json().get('value', [])
            for channel in channels:
                if channel['displayName'] == channel_name:
                    return channel['id']
            raise Exception("Channel not found.")
        else:
            raise Exception(f"Failed to get channel ID: {response.status_code}, {response.text}")

    def send_teams_message(self, access_token, team_id, channel_id, message):
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "body": {
                "content": message
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code == 201:
            return "Message sent successfully"
        else:
            raise Exception(f"Error sending message: {response.status_code}, {response.text}")