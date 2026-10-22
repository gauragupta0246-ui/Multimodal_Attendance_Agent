import uvicorn
from fastapi import FastAPI
from backend.core.camera_service import CameraService
from backend.core.face_recognition import FaceRecognizer
from backend.core.audio_analysis import AudioAnalyzer
from backend.core.engagement_scoring import EngagementScorer
from backend.core.teacher_profiles import TeacherProfileService

app = FastAPI(title="Multimodal Attendance & Engagement Agent")

camera_svc = CameraService()
face_rec = FaceRecognizer()
audio_ana = AudioAnalyzer()
scorer = EngagementScorer()
teacher_svc = TeacherProfileService()

@app.get("/")
def root():
    return {"status": "Multimodal Attendance Agent Pipeline Active"}

@app.get("/api/teacher-profile/{teacher_id}")
def get_teacher_profile(teacher_id: str):
    return teacher_svc.get_profile(teacher_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)