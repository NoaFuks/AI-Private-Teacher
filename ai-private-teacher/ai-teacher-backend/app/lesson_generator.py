import fitz  # PyMuPDF
import re
import requests
import json
import os
import random
from openai import OpenAI

class LessonGenerator:
    def __init__(self, user_profile, api_key, progress_tracker):
        self.user_profile = user_profile
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.progress_tracker = progress_tracker


    def extract_text_from_pdf(self, pdf_path):
        try:
            document = fitz.open(pdf_path)
            text = ""
            for page in document:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def generate_lesson_in_segments(self, pdf_path):
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                return {"lesson": "No text extracted from the PDF.", "questions": [], "ask_for_questions": False}

#             # Extract a dynamic lesson topic from the content
#             lesson_topic = self.extract_topic_from_content(text)
#
#             # Generate the lesson summary and detailed content
#             lesson_summary = f"Today's topic: {lesson_topic}."
#             lesson_content = lesson_summary + "\n\n"

            # Split the text into segments and generate corresponding questions for each segment
            segments = self.split_text_into_segments(text)
            lesson_segments = []
            all_questions = []

            for segment in segments:
                # Add segment to the list
                long_paragraph = self.create_long_paragraph(segment)
                lesson_segments.append(long_paragraph)

                # Generate corresponding questions
                personalized_question, correct_answer, explanation = self.create_personalized_question(long_paragraph)

                all_questions.append({
                    "question": personalized_question,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })

            # Return all lesson segments and questions
            return {"lesson_segments": lesson_segments, "questions": all_questions}

    def handle_student_question(self, student_question):
        prompt = f"Answer this student's question: {student_question}"
        response = self._call_openai_api(prompt, max_tokens=150)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def extract_topic_from_content(self, text):
        # Use a simple heuristic or NLP-based method to extract the main topic
        prompt = f"Extract the main topic from the following text:\n\n{text[:1000]}"  # Use the first 1000 characters
        response = self._call_openai_api(prompt, max_tokens=50)
        topic = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        return topic or "General Knowledge"

    def split_text_into_segments(self, text, max_length=500):
        sentences = re.split(r'(?<=[.!?]) +', text)
        segments = []
        current_segment = ""

        for sentence in sentences:
            if len(current_segment) + len(sentence) <= max_length:
                current_segment += " " + sentence
            else:
                segments.append(current_segment.strip())
                current_segment = sentence

        if current_segment:
            segments.append(current_segment.strip())

        return segments

    def create_long_paragraph(self, segment):
        learning_preferences = ', '.join(self.user_profile.get("learning_preferences", ["unknown learning preferences"]))
        age = self.user_profile.get("age", "unknown age")
        prompt = f"Generate a short but detailed and comprehensive paragraph from the following content suitable for a " \
                 f"{age}-year-old student with learning preferences: {learning_preferences}. " \
                 f"The paragraph should be informative, engaging, and cover the topic.:\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=300)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def create_personalized_question(self, long_paragraph):
        hobby = random.choice(self.user_profile.get("hobbies", ["unknown hobby"]))
        learning_preferences = ', '.join(self.user_profile.get("learning_preferences", ["unknown learning preferences"]))
        age = self.user_profile.get("age", "unknown age")
        prompt = f"Create a multiple choice (a-d) question related to {hobby} that incorporates the topic being " \
                 f"studied. Provide the correct answer (the answer should be only the correct answer letter) " \
                 f"and an explanation for the answer if the student is wrong " \
                 f"The question should be appropriate for a " \
                 f"{age}-year-old student with learning preferences: {learning_preferences}.\n\n" \
                 f"Here is the paragraph to base the question on:\n\n{long_paragraph}. " \
                 f"Here is an example of how it should look exactly:\n " \
                 f"Question: How many legs does a dog have?\n" \
                 f"1. 3\n" \
                 f"2. 4\n" \
                 f"3. 6\n" \
                 f"4. 8\n" \
                 f"Answer: 2" \
                 f"Explanation: Dogs have four legs, just like most mammals."
        response = self._call_openai_api(prompt, max_tokens=150)
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if 'Answer:' in content and 'Explanation:' in content:
            question, remainder = content.split('Answer:', 1)
            correct_answer, explanation = remainder.split('Explanation:', 1)
            return question.strip(), correct_answer.strip(), explanation.strip()
        else:
            return content, "No correct answer provided", "No explanation provided"

    def _call_openai_api(self, prompt, max_tokens):
        try:
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': max_tokens
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenAI API: {e}")
            return {}



# Example usage:
if __name__ == "__main__":
    from UserProfile import UserProfileManager
    from progressPage import ProgressTracker  # Make sure to import from the correct module

    manager = UserProfileManager()
    manager.load_profiles_from_file('user_profiles.json')

    user_profile = manager.profiles[0]  # Just an example to use the first profile
    api_key = "sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp"  # Replace with your actual OpenAI API key

    progress_tracker = ProgressTracker(student_name=user_profile.name)

    # Path to the folder containing PDF files
    pdf_folder_path = r".\DataBase"

    # Check if the directory exists
    if not os.path.exists(pdf_folder_path):
        print(f"The directory {pdf_folder_path} does not exist.")
    else:
        # List all PDF files in the folder
        pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]

        if not pdf_files:
            print("No PDF files found in the specified directory.")
        else:
            pdf_file = pdf_files[0]  # Pick the first PDF file for this session
            pdf_path = os.path.join(pdf_folder_path, pdf_file)
            generator = LessonGenerator(user_profile, api_key, progress_tracker)
            lesson = generator.generate_lesson(pdf_path)
            # for pdf_file in pdf_files:
            #     pdf_path = os.path.join(pdf_folder_path, pdf_file)
            #     # generator = LessonGenerator(user_profile, api_key)
            #     generator = LessonGenerator(user_profile, api_key, progress_tracker)
            #     lesson = generator.generate_lesson(pdf_path)
            #     # print(f"Lesson generated from {pdf_file}:\n")
            #     # print(lesson)
            print("\n" + "=" * 80 + "\n")


