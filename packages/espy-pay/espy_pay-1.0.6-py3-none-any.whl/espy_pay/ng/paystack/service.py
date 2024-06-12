"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import requests
from espy_pay.ng.paystack.util import CONSTANTS
from espy_pay.ng.paystack.schema import Subaccount_Request
from espy_pay.general.schema import TranxDto

def init_tranx(data: TranxDto):
    url = f"{CONSTANTS.PAYSTACK_URL}initialize"
    headers = {
        "Authorization": CONSTANTS.AUTH,
        "Content-Type": "application/json"
    }
    data_dict = data.model_dump()
    if "callback_url" in data_dict:
        data_dict["callback_url"] = str(data_dict["callback_url"])
    response = requests.post(url, json=data_dict, headers=headers)
    return response.json()
def verify_tranx(reference: str):
    url = f"{CONSTANTS.PAYSTACK_URL}verify/{reference}"
    headers = {
        "Authorization": CONSTANTS.AUTH
    }
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_tranx(id: int = None):
    url = f"{CONSTANTS.PAYSTACK_URL}transaction"
    if id is not None:
        url += f"?id={id}"

    response = requests.get(url, headers={"Authorization": CONSTANTS.AUTH})
    return response.json()
def charge_tranx(data: TranxDto):
    url = f"{CONSTANTS.PAYSTACK_URL}transaction/charge_authorization"
    headers = {
        "Authorization": CONSTANTS.AUTH,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
def split_tranx(data: dict):
    url = f"{CONSTANTS.PAYSTACK_URL}split"
    content_type = "Content-Type: application/json"
    response = requests.post(url, headers={"Authorization": CONSTANTS.AUTH, "Content-Type": content_type}, data=data)
    return response.json()
def create_subaccount(data: Subaccount_Request):
    url = f"{CONSTANTS.PAYSTACK_URL}subaccount"
    response = requests.post(url, headers={"Authorization": CONSTANTS.AUTH, "Content-Type": "application/json"}, json=data)
    return response.json()
def update_subaccount(sub_account_code: str, data: Subaccount_Request):
    url = f"{CONSTANTS.PAYSTACK_URL}subaccount/{sub_account_code}"
    response = requests.put(url, headers={"Authorization": CONSTANTS.AUTH, "Content-Type": "application/json"}, json=data)
    return response.json()
def list_subaccount(sub_account_code: str = None):
    if sub_account_code is not None:
        url = f"{CONSTANTS.PAYSTACK_URL}subaccount/{sub_account_code}"
    else:
        url = f"{CONSTANTS.PAYSTACK_URL}subaccount"
    response = requests.get(url, headers={"Authorization": CONSTANTS.AUTH})
    return response.json()