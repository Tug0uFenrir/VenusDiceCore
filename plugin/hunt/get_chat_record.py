import json
import os
import requests
def get_chat_record(group_id,count):
        payload = json.dumps({
            "group_id": group_id,
            "count": count
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn_api = requests.post("http://localhost:3000/get_group_msg_history", headers=headers, data=payload)
        resp = conn_api.json()
        return resp
