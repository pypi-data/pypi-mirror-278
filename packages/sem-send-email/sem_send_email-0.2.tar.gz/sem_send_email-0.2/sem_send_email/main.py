import requests


def send_email(title:str, channel:str, emails:list, message:str, url:str):
    result = {"status": False, "content": None}
    try:
        for mail in emails:
            body = {"service_name": f"{title}",
                        "channel": [{
                            "name": channel
                        }
                        ],
                        "user_email": mail,
                        "message": message

                        }
            requests.post(f"{url}", headers={'Content-Type': 'application/json'}, json=body)
        result["content"] = "Mail sent successfully"
        result["status"] = True
    except Exception as e:
        result["content"] = f"Mail could not sent, ERR:{str(e)}"
    finally:
        return result