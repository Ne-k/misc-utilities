import requests
import sys
import time


def check_schedule():
    url = "https://synergy-parstuvue.wlwv.k12.or.us/Service/PXPCommunication.asmx/ProcessWebServiceRequest"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "synergy-parstuvue.wlwv.k12.or.us"
    }
    data = {
        "userID": "<lastname><firstInitial>@wlhs.wlwv.k12.or.us",
        "password": "<Password>",
        "skipLoginLog": "true",
        "parent": "false",
        "webServiceHandleName": "PXPWebServices",
        "methodName": "StudentClassList",
        "paramStr": "<Parms><childIntID>0</childIntID></Parms>"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_content = response.content.decode('utf-8')

        if "No class schedule" in response_content:
            print("Error: No class schedule found.")
        else:
            print("Response received:")
            print(response_content)

            discord_webhook_url = "https://discord.com/api/webhooks/1273502986164899891/Y4OT8yvm5HDEbiGVTGoRrzx4WBWsK2NW5Br2yN-x1KY5GTjNTZmaRINnjQ0eHeNnXXeW"
            discord_data = {
                "embeds": [
                    {
                        "title": "Schedules released",
                        "description": "The class schedules have been released.",
                        "color": 3066993  # You can change the color if you like
                    }
                ],
                "content": "<@&1031419171323531274> may or may not be a false positive since this has never been "
                           "successfully tested before :3"
            }

            discord_response = requests.post(discord_webhook_url, json=discord_data)

            if discord_response.status_code == 204:
                print("Successfully posted to Discord webhook.")
            else:
                print(f"Failed to post to Discord webhook: {discord_response.status_code}")

            # Terminate the script
            sys.exit()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")


while True:
    check_schedule()
    time.sleep(120)
