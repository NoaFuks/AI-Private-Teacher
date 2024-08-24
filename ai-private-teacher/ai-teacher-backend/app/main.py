from fastapi import FastAPI, Request, HTTPException
from app.lesson_generator import LessonGenerator
from app.parent_progress_page import ParentProgressPage
from app.progress_page import ProgressTracker
import os
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories for storing profiles, progress, and PDFs
PROFILE_DIR = './profiles'
PROGRESS_DIR = './progress_data'
PDF_DIR = './DataBase'  # Directory containing PDF lessons

# Ensure the directories exist
os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

@app.post("/api/save-profile")
async def save_profile(request: Request):
    try:
        profile_data = await request.json()
        # Save the profile to a JSON file named by the student's name
        profile_path = os.path.join(PROFILE_DIR, f"{profile_data['name'].lower().replace(' ', '_')}_profile.json")
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=4)
        return {"message": "Profile saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {e}")

@app.post("/api/generate-lesson")
async def generate_lesson(request: Request):
    try:
        profile_data = await request.json()
        student_name = profile_data.get("name")

        profile_path = os.path.join(PROFILE_DIR, f"{student_name.lower().replace(' ', '_')}_profile.json")
        if not os.path.exists(profile_path):
            raise HTTPException(status_code=404, detail=f"Profile for student '{student_name}' not found.")

        with open(profile_path, 'r') as profile_file:
            student_profile = json.load(profile_file)

        api_key = "sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp"  # Add your OpenAI key here
        progress_tracker = ProgressTracker(student_name=student_name, progress_directory=PROGRESS_DIR)
        lesson_generator = LessonGenerator(user_profile=student_profile, api_key=api_key, progress_tracker=progress_tracker)

        pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
        if not pdf_files:
            raise HTTPException(status_code=404, detail="No PDF files found in the specified directory.")

        pdf_path = os.path.join(PDF_DIR, pdf_files[0])

        # Generate the lesson content and questions
        lesson_data = lesson_generator.generate_lesson_in_segments(pdf_path)
        return lesson_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {e}")

@app.post("/api/handle-question")
async def handle_question(request: Request):
    try:
        data = await request.json()
        student_question = data.get("question")
        lesson_generator = LessonGenerator({}, api_key="sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp", progress_tracker=None)
        answer = lesson_generator.handle_student_question(student_question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to handle question: {e}")

@app.post("/api/validate-answer")
async def validate_answer(request: Request):
    try:
        data = await request.json()
        student_answer = data.get("student_answer")
        correct_answer = data.get("correct_answer")
        explanation = data.get("explanation")

        if student_answer.strip().lower() == correct_answer.strip().lower():
            feedback = "Correct! Well done!"
            return {"correct": True, "feedback": feedback}
        else:
            feedback = f"Incorrect. The correct answer is: {correct_answer}. {explanation}"
            return {"correct": False, "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate answer: {e}")

@app.get("/api/get-progress")
async def get_progress(student_name: str):
    try:
        # Initialize the ParentProgressPage to get student progress
        parent_page = ParentProgressPage(progress_directory=PROGRESS_DIR)
        summary = parent_page.summarize_child_progress(student_name)

        if summary:
            return summary
        else:
            raise HTTPException(status_code=404, detail="Progress data not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Progress data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve progress: {e}")


@app.post("/api/save-progress")
async def save_progress(request: Request):
    try:
        progress_data = await request.json()
        student_name = progress_data.get("student_name", "unknown")

        # Initialize ProgressTracker and save progress
        progress_tracker = ProgressTracker(student_name=student_name, progress_directory=PROGRESS_DIR)
        progress_tracker.update_progress(
            lesson=progress_data.get("lesson"),
            correct=progress_data.get("correct"),
            explanation=progress_data.get("explanation", ""),
            interaction_details=progress_data.get("interaction_details"),
            lesson_summary=progress_data.get("lesson_summary", "")
        )

        return {"message": "Progress saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save progress: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
