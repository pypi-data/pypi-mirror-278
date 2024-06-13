import requests
import os
from dotenv import load_dotenv
from typing import Optional, Dict


load_dotenv()

host = "https://api.dooray.com"
token = os.environ.get("DOORAY_TOKEN")
header = {"Authorization": f"{token}", "Content-Type": "application/json"}


def dooray_get(end_point: str, params: Dict) -> Optional[Dict]:
    response = requests.get(host + end_point, headers=header, params=params)
    if response.status_code == 200:
        print("GET 요청 성공")
        return response.json()
    else:
        print("GET 요청 실패:", response.status_code, response.text)
        return None
