from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime, timezone
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io
import os
import json

app = FastAPI()

# MongoDB connection (เปลี่ยน <db_password> เป็นรหัสผ่านจริงของคุณ)
client = MongoClient("mongodb+srv://phirapont:2kFL3F8A4XrVGrRA@cluster0.dqfmomu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["video_analyzer"]
collection = db["analyze_results"]

# อนุญาตให้ frontend (React) เชื่อมต่อ (ถ้าเป็น dev ใช้ allow_all ไปก่อน)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # เปลี่ยนเป็น URL frontend จริงถ้าขึ้น prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_to_google_drive(file: UploadFile):
    # ใช้ Service Account จาก Environment Variable
    SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_ID = '13o10S0P_ofqzHrl8WjRqvttbD4NbxXW-'  # ใส่ folder id ของคุณ

    # โหลด credentials จาก env
    service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # อ่านไฟล์จาก UploadFile เป็น binary
    file_stream = io.BytesIO(file.file.read())

    file_metadata = {
        'name': file.filename,
        'parents': [FOLDER_ID]
    }
    media = MediaIoBaseUpload(file_stream, mimetype=file.content_type)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    file_id = uploaded_file.get('id')
    # สร้าง share link
    share_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    drive_path = f"/content/drive/MyDrive/ai-video-analyzer/videos/{file.filename}"

    # ตั้งค่าให้ anyone with the link view ได้
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    return drive_path, share_link

@app.post("/analyze")
async def analyze_video(
    video: UploadFile = File(...),
    expected_topic: str = Form(...)
):
    # อัปโหลดไฟล์และรับ path + share link
    drive_path, share_link = upload_to_google_drive(video)

    result = {
        "score": 0.8,
        "suggestion": "พูดตรงประเด็นดีแล้ว"
    }

    print("กำลังจะ insert ลง MongoDB")
    try:
        collection.insert_one({
            "filename": video.filename,
            "expected_topic": expected_topic,
            "drive_path": drive_path,
            "share_link": share_link,
            "score": result["score"],
            "suggestion": result["suggestion"],
            "created_at": datetime.now(tz=timezone.utc)
        })
        print("Insert สำเร็จ")
    except Exception as e:
        print("MongoDB insert error:", e)

    return {
        "message": f"ได้รับไฟล์ {video.filename} แล้ว",
        "drive_path": drive_path,
        "share_link": share_link,
        "result": result
    }

if __name__ == "__main__":
    try:
        print("Databases:", client.list_database_names())
        print("เชื่อมต่อ MongoDB สำเร็จ")
    except Exception as e:
        print("เชื่อมต่อ MongoDB ไม่สำเร็จ:", e)
