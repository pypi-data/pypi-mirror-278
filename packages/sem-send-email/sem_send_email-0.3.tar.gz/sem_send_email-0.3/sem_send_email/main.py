import requests, json


def send_email(title: str, channel: str, emails: list, message: str, url: str):
    results = []
    for mail in emails:
        body = {"service_name": f"{title}",
                    "channel": [{
                        "name": channel
                    }
                    ],
                    "user_email": mail,
                    "message": message

                    }
        response = requests.post(f"{url}", headers={'Content-Type': 'application/json'}, json=body)
        results.append(json.loads(response.content))
    return results
