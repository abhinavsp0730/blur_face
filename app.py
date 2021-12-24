import urllib.request
import os   
import cv2
import numpy as np
import uuid
import boto3
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def ranname():
    return str(uuid.uuid1())+".jpg"

s3_client = boto3.client('s3', 
                      aws_access_key_id="xxxxxxxx", 
                      aws_secret_access_key="xxxxxxx", 
                      region_name="xxxxx"
                      ) 
def upload(s3,name):
    bucket_name = 'manraap'
    content = open(name, 'rb')
    s3.put_object(
    Bucket=bucket_name, 
    Key= name, 
    Body=content)

def blur(url):
    rname = ranname()  
    urllib.request.urlretrieve(url, "local-filename.jpg")
    model = cv2.dnn.readNetFromCaffe('blur-face/libs/deploy.prototxt', 'blur-face/libs/res10_300x300_ssd_iter_140000.caffemodel')
    image = cv2.imread("local-filename.jpg")
    orig = image.copy()
    (h, w) = image.shape[:2]


    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    model.setInput(blob)
    detections = model.forward()
    count=0
    for i in range(0, detections.shape[2]):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        confidence = detections[0, 0, i, 2]
        
        if (confidence > 0.4):

            face = image[startY:endY, startX:endX]       
        
            kW = 6
            kH = int(h / int(5))
            if kW % 2 == 0:
                kW -= 1
            if kH % 2 == 0:
                kH -= 1
            
            image[startY:endY, startX:endX] = cv2.GaussianBlur(face, (kW, kH), -9)       
            count = count + 1 
    cv2.imwrite(rname, image)
    return rname, count

class Item(BaseModel):
    url: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predict")
async def create_item(item: Item):
    item_dict = item.dict()
    name, count= blur(item.url)
    upload(s3_client, name)
    os.remove("local-filename.jpg")
    os.remove(name)
    # put your aws s3 bucket url.
    img = "https://your-s3-buket-name.s3.ap-south-1.amazonaws.com/"+name
    return {"img_url": img, "face_detected": count}
