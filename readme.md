# Video Analyzer API

API สำหรับวิเคราะห์วิดีโอและบันทึกผลลง MongoDB  
เชื่อมต่อกับหน้าเว็บ (React) ได้

## วิธีติดตั้งและใช้งาน

### 1. Clone โปรเจกต์
```sh
git clone <repo-url>
cd video-analyzer-api
```

### 2. สร้างและเปิดใช้งาน virtual environment (แนะนำ)
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. ติดตั้ง dependencies
```sh
pip install -r requirements.txt
```

### 4. ตั้งค่า MongoDB Connection String
- แก้ไขไฟล์ `main.py` ที่บรรทัดนี้  
  ```python
  client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority")
  ```
- หรือใช้ environment variable เพื่อความปลอดภัย

### 5. รันเซิร์ฟเวอร์
```sh
uvicorn main:app --reload
```

### 6. ทดสอบ API
- เรียก `POST /analyze` โดยส่งไฟล์วิดีโอและ expected_topic
- ผลลัพธ์จะถูกบันทึกลง MongoDB อัตโนมัติ

### 7. ตรวจสอบข้อมูลใน MongoDB
- ใช้ MongoDB Atlas หรือ MongoDB Compass เพื่อดูข้อมูลใน database `video_analyzer` collection `analyze_results`

---

## หมายเหตุ
- หากต้องการ deploy บน Heroku หรือ platform อื่น ให้ใช้ไฟล์ `Procfile` ที่เตรียมไว้
- หากต้องการเปลี่ยนชื่อ database หรือ collection สามารถแก้ไขใน `main.py` ได้เลย

---
```# Video Analyzer API

API สำหรับวิเคราะห์วิดีโอและบันทึกผลลง MongoDB  
เชื่อมต่อกับหน้าเว็บ (React) ได้

## วิธีติดตั้งและใช้งาน

### 1. Clone โปรเจกต์
```sh
git clone <repo-url>
cd video-analyzer-api
```

### 2. สร้างและเปิดใช้งาน virtual environment (แนะนำ)
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. ติดตั้ง dependencies
```sh
pip install -r requirements.txt
```

### 4. ตั้งค่า MongoDB Connection String
- แก้ไขไฟล์ `main.py` ที่บรรทัดนี้  
  ```python
  client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority")
  ```
- หรือใช้ environment variable เพื่อความปลอดภัย

### 5. รันเซิร์ฟเวอร์
```sh
uvicorn main:app --reload
```

### 6. ทดสอบ API
- เรียก `POST /analyze` โดยส่งไฟล์วิดีโอและ expected_topic
- ผลลัพธ์จะถูกบันทึกลง MongoDB อัตโนมัติ

### 7. ตรวจสอบข้อมูลใน MongoDB
- ใช้ MongoDB Atlas หรือ MongoDB Compass เพื่อดูข้อมูลใน database `video_analyzer` collection `analyze_results`

---

## หมายเหตุ
- หากต้องการ deploy บน Heroku หรือ platform อื่น ให้ใช้ไฟล์ `Procfile` ที่เตรียมไว้
- หากต้องการเปลี่ยนชื่อ database หรือ collection สามารถแก้ไขใน `main.py` ได้เลย

---