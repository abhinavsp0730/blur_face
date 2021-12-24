You Need  ```Python 3.6``` to run this Project. \
After installing Python,
1. Run ``` pip install -r requirements.txt ``` 
2. Run ``` uvicorn app:app ```
The server has started at http://127.0.0.1:8000 \
and you can do a post request in ``` http://127.0.0.1:8000/predict``` using a json format like this \
{"url:"your_image_url"} 
e.g,
```
{"url":"https://media.istockphoto.com/photos/group-portrait-of-a-creative-business-team-standing-outdoors-three-picture-id1146473249?k=20&m=1146473249&s=612x612&w=0&h=9Ki3nKs4Su-_YRMc6__iuWnHLhpp58ULOsz4l9PT6tw="}
```
and after this you'll recieve a resonse with blur_face image and \
the number of face in it. \
e.g, 
```
{
    "img_url": "https://manraap.s3.ap-south-1.amazonaws.com/d7c84902-64d5-11ec-baee-567d9c903b9d.jpg",
    "face_detected": 8
}
```
