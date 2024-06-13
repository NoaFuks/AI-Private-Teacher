import fitz  # PyMuPDF
from UserProfile import UserProfileManager
import requests
import os
import json


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
            lesson_content += self.create_teaching_segment(segment) + "\n"
            for hobby in self.user_profile.hobbies:
                lesson_content += self.create_hobby_related_question(hobby, segment) + "\n\n"

        return lesson_content

    def split_text_into_segments(self, text, segment_length=300):
        words = text.split()
        segments = [' '.join(words[i:i + segment_length]) for i in range(0, len(words), segment_length)]
        return segments

    def create_teaching_segment(self, segment):
        prompt = f"Teach the following content in a simple and engaging manner suitable for a {self.user_profile.age}-year-old student:\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=150)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def create_hobby_related_question(self, hobby, segment):
        prompt = f"Based on the following content:\n\n{segment}\n\nCreate a question involving {hobby} suitable for a {self.user_profile.age}-year-old student. The subject of the question should be based on their learning preferences: {', '.join(self.user_profile.learning_preferences)}."
        response = self._call_openai_api(prompt, max_tokens=100)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

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

#sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp