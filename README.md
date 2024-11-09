
# AI Private Teacher App

## Overview

The AI Private Teacher App is a web application designed to deliver personalized lessons, track student progress, and provide insights for parents. It generates lessons from uploaded PDFs, incorporates student hobbies, and provides feedback on their learning. Both the frontend and backend work together to offer this functionality.

---

## Features

### Frontend

- **Landing Page**: Entry point with links to the Profile Page, Lesson Generation Page, and Progress Page.
- **Profile Page**: Allows students to input their name, age, hobbies, and learning preferences.
- **Lesson Generation**: Generates lessons based on uploaded PDFs, tracks progress, and uses speech recognition for answering questions.
- **Parent Progress Page**: Provides an overview of the student's performance, including correct and incorrect answer percentages, topics covered, and AI feedback. It also tracks student feelings during the lesson.

### Backend

- **PDF Handling**: Extracts text from uploaded PDFs and divides it into lesson segments.
- **Lesson Generation**: Generates personalized lessons based on student profiles, including hobbies and learning preferences.
- **Progress Tracking**: Tracks progress for each student, including answers, questions, and overall performance.
- **AI Integration**: Uses OpenAI to generate lesson content, questions, and feedback.
- **Student Profile Management**: Saves and manages student profiles, including name, age, hobbies, and learning preferences.

---

## Folder Structure

Here is the folder structure of the project, as seen in the provided image:

```
.
├── ai-private-teacher
│   ├── ai-teacher-backend
│   │   ├── DataBase
│   │   ├── app
│   │   │   ├── __pycache__
│   │   │   ├── lesson_generator.py
│   │   │   ├── main.py
│   │   │   ├── parent_progress_page.py
│   │   │   └── progress_page.py
│   │   ├── profiles
│   │   ├── progress_data
│   │   ├── requirements.txt
│   ├── public
│   ├── src
│   │   ├── pages
│   │   │   ├── LandingPage.js
│   │   │   ├── LessonGenerationPage.js
│   │   │   ├── ParentProgressPage.js
│   │   │   └── ProfilePage.js
│   ├── .gitignore
│   ├── README.md
│   └── package-lock.json
```

---

## Installation

### Frontend

1. Navigate to the `ai-private-teacher` folder.
2. Install the frontend dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`.

### Backend

1. Navigate to the `ai-teacher-backend` folder.
2. Install the backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

The backend will be available at `http://localhost:8000`.

---

## API Endpoints

### `/api/upload-pdf`
Uploads a PDF to generate lessons based on the content.

### `/api/save-profile`
Saves the student profile information, including name, age, hobbies, and learning preferences.

### `/api/generate-lesson`
Generates lesson segments and questions based on the uploaded PDF and student profile.

### `/api/validate-answer`
Validates the student's answer to a question and provides feedback.

### `/api/get-progress`
Retrieves the progress data for a specific student.

### `/api/save-progress`
Saves the progress of a student during a lesson, including answers, questions, and feelings.

---

## Technologies Used

### Frontend
- **React** for the frontend.
- **Bootstrap** for styling.

### Backend
- **FastAPI** for the backend framework.
- **PyMuPDF** for extracting text from PDF files.
- **OpenAI** for generating lesson content and questions.
- **JSON** for saving and retrieving student profiles and progress data.

---

