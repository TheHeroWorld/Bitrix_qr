from fastapi import FastAPI
import base64
import os
import segno
from dotenv import load_dotenv
import aiohttp


load_dotenv()
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")

app = FastAPI()

@app.post("/bitr/")
async def root(text: str, uuid: str, password: str):
    print(PASSWORD)
    if password == PASSWORD:
        await generate_qr(text, uuid)
        
        

async def generate_qr(text, uuid):
    qr_code = segno.make_qr(text)
    name = f"qr_code{uuid}.png"
    qr_code.save(name)
    with open(name, "rb") as qr:
        qr_base64 =base64.b64encode(qr.read())
        await request_birt(qr_base64, uuid)
        print(PASSWORD, URL, qr_base64)
    os.remove(name)
    
    
    
async def request_birt(qr_base64, uuid):
        data = {
        "entityTypeId": "31",
        "id": uuid,
        "fields": {
            "ufCrm_SMART_INVOICE_1712655537962":["QR.png", qr_base64]
        }
    }
        async with aiohttp.ClientSession() as session:
            async with session.post(URL, data=data) as response:
                print(response)
                
