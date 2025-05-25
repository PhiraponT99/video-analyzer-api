from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    # Demo: ตอบกลับ mock ก่อน
    return {
        "score": 80,
        "suggestion": "ควรเพิ่มเนื้อหาในหัวข้อ X อีกหน่อย"
    }
