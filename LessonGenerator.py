import fitz  # PyMuPDF
from UserProfile import UserProfileManager
import requests
import os
import json
import re


class LessonGenerator:
    def __init__(self, user_profile, api_key):
        self.user_profile = user_profile
        self.api_key = api_key

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

    def generate_lesson(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return "No text extracted from the PDF."

        segments = self.split_text_into_segments(text)
        lesson_content = ""

        for segment in segments:
            teaching_segment = self.create_teaching_segment(segment)
            lesson_content += teaching_segment + "\n"
            print(teaching_segment + "\n")

            example_segment = self.create_example_segment(segment)
            lesson_content += example_segment + "\n"
            print(example_segment + "\n")

            example_question_segment, example_answer = self.create_example_question_segment(segment)
            lesson_content += example_question_segment + "\n"
            print(example_question_segment + "\n")

            question_segment, correct_answer = self.create_question_segment(segment)
            lesson_content += question_segment + "\n"
            print(question_segment + "\n")

            student_answer = self.get_student_response()
            feedback = self.provide_feedback(student_answer, correct_answer)
            lesson_content += feedback + "\n"
            print(feedback + "\n")

        return lesson_content

    def split_text_into_segments(self, text, max_length=300):
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

    def create_teaching_segment(self, segment):
        prompt = f"Teach the following content in a simple and engaging manner suitable for a {self.user_profile.age}-year-old student:\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=150)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def create_example_segment(self, segment):
        prompt = f"Provide an example based on the following content to help a {self.user_profile.age}-year-old student understand better:\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=100)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def create_example_question_segment(self, segment):
        prompt = f"Create an example question and answer based on the following content to help a {self.user_profile.age}-year-old student understand better how to answer questions. Consider the student's learning preferences: {', '.join(self.user_profile.learning_preferences)}.\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=150)
        example_question_answer = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if 'Answer:' in example_question_answer:
            example_question, example_answer = example_question_answer.split('Answer:', 1)
            return example_question.strip(), example_answer.strip()
        else:
            return example_question_answer, "No answer provided"

    def create_question_segment(self, segment):
        prompt = f"Create a question based on the following content suitable for a {self.user_profile.age}-year-old student. The subject of the question should be based on their learning preferences: {', '.join(self.user_profile.learning_preferences)}.\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=100)
        question_answer = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if 'Answer:' in question_answer:
            question, correct_answer = question_answer.split('Answer:', 1)
            return question.strip(), correct_answer.strip()
        else:
            return question_answer, "No answer provided"

    def get_student_response(self):
        return input("Please answer the question above and press Enter to continue: ").strip()

    def provide_feedback(self, student_answer, correct_answer):
        if correct_answer == "No answer provided":
            feedback = "No correct answer was provided for this question."
        elif student_answer.lower() == correct_answer.lower():
            feedback = "Correct! Well done."
        else:
            feedback = f"Incorrect. The correct answer is: {correct_answer}"
        return feedback

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
    manager = UserProfileManager()
    manager.load_profiles_from_file('user_profiles.json')

    user_profile = manager.profiles[0]  # Just an example to use the first profile
    api_key = "sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp"  # Replace with your actual OpenAI API key

    # Path to the folder containing PDF files
    pdf_folder_path = r"C:\Users\Noa fuks\OneDrive\IDC\Third Year B\From Idea To Reality App Using AI tools\Project\DataBase"

    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the specified directory.")
    else:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder_path, pdf_file)
            generator = LessonGenerator(user_profile, api_key)
            lesson = generator.generate_lesson(pdf_path)
            print(f"Lesson generated from {pdf_file}:\n")
            print(lesson)
            print("\n" + "=" * 80 + "\n")









