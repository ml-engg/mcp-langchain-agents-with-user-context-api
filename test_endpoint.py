# Databricks notebook source
import requests

url = ""  # Adjust if running on a different host/port

payload = {
    "user_id": "",
    "query": ""
}

headers = {"Authorization": ""}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())


# COMMAND ----------



# COMMAND ----------

import requests

url = ""  # Adjust if needed

headers = {
    "Content-Type": "application/json",
    "Authorization": ""  # Add token if needed
}

user_requests = [
    {"user_id": "", "query": ""},
    {"user_id": "", "query": ""},
    {"user_id": "", "query": ""},
    {"user_id": "", "query": ""}
]


# COMMAND ----------

import requests
import concurrent.futures

def send_request(payload):
    try:
        response = requests.post(url, json=payload, headers=headers)
        return f"{payload['user_id']} → {response.status_code} → {response.json().get('result', '')[:80]}"
    except Exception as e:
        return f"{payload['user_id']} →  {str(e)}"

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(send_request, user_requests))

for res in results:
    print(res)

