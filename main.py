from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime, timezone

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

@app.post("/analyze")
async def analyze_video(
    video: UploadFile = File(...),
    expected_topic: str = Form(...)
):
    # ตัวอย่างข้อมูล mock
    result = {
        "score": 80,
        "suggestion": "ควรเพิ่มเนื้อหาในหัวข้อ X อีกหน่อย"
    }

    print("กำลังจะ insert ลง MongoDB")
    try:
        collection.insert_one({
            "filename": video.filename,
            "expected_topic": expected_topic,
            "score": result["score"],
            "suggestion": result["suggestion"],
            "created_at": datetime.now(tz=timezone.utc)
        })
        print("Insert สำเร็จ")
    except Exception as e:
        print("MongoDB insert error:", e)

    # ตอบกลับว่ารับไฟล์แล้ว
    return {
        "message": f"ได้รับไฟล์ {video.filename} แล้ว",
        "result": result
    }

if __name__ == "__main__":
    try:
        print("Databases:", client.list_database_names())
        print("เชื่อมต่อ MongoDB สำเร็จ")
    except Exception as e:
        print("เชื่อมต่อ MongoDB ไม่สำเร็จ:", e)
