import torch
import easyocr
import io
import numpy as np
from PIL import Image
import os
import boto3
import asyncio
from datetime import datetime
import pytz


async def Image_Model(image):
    # Open the image using Pillow
    img = Image.open(image)
    # Model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    path = r'/home/ec2-user/warehouse_apis/qzense_APIs/DjangoAPIs/model/best.pt'
    model = torch.hub.load("WongKinYiu/yolov7","custom",f"{path}",trust_repo=True)

    # Inference
    results = model(img)

    # set confidence threshold
    conf_thresh = 0.2
    boxes = results.xyxy[0][results.xyxy[0][:, 4] > conf_thresh, :4]  # get boxes with confidence > conf_thresh

    box = tuple(boxes[0].tolist())  # convert NumPy array to tuple
    cropped_image = img.crop(box)

    # Convert the image to a NumPy array
    image_array = np.asarray(cropped_image)
    #  Extract text from the cropped image using easyocr library
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_array, detail = 0)

    string = ""
    for something in result:
        string += something
        
    return string

def current_datetime(format):
    IST = pytz.timezone('Asia/Kolkata')
    datetime_utc = datetime.now(IST)
    datetime_string = str(datetime_utc.strftime('%Y%m%d%H%M%S')) + '.' + format.lower()
    datetime_object = datetime_utc.strftime('%Y-%m-%d %H:%M:%S')
    
    return datetime_object, datetime_string
    
    

async def upload_to_s3(image):
    
    img = Image.open(image)
    format = img.format
    
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    access_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    
    # session = boto3.Session(
    # aws_access_key_id = access_key,
    # aws_secret_access_key= access_secret_key,
    # region_name = 'ap-south-1'
    # )
    # print(img.format)
    # s3 = session.resource('s3')
    client = boto3.resource('s3',
                          aws_access_key_id = access_key,
                          aws_secret_access_key = access_secret_key,
                          region_name = 'ap-south-1')
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    # Key='media/%s' % img.name
    # s3.Bucket(bucket_name).put_object(Key="sample.jpeg", Body=img_byte_arr)
    # Uploading to S3
    entry_datetime , image_name = current_datetime(format)
    object = client.Object(bucket_name, image_name)
    object.put(Body=img_byte_arr)
    
    # await asyncio.sleep(0)
    return entry_datetime, image_name

    
async def execute(image):
    # Create tasks to execute concurrently
    task_predict = asyncio.create_task(Image_Model(image))
    task_other = asyncio.create_task(upload_to_s3(image))
    
    # Wait for tasks to complete
    predictions = await task_predict
    entry_datetime, image_name = await task_other
    
    return predictions, entry_datetime, image_name
