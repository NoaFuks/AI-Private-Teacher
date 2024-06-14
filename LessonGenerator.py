import fitz  # PyMuPDF
import re
import requests
import json
import os
import random

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
            long_paragraph = self.create_long_paragraph(segment)
            lesson_content += long_paragraph + "\n\n"
            print(long_paragraph + "\n\n")

            example_question, example_answer = self.create_example_question(segment)
            lesson_content += example_question + "\n"
            lesson_content += example_answer + "\n\n"
            print(example_question + "\n")
            print(example_answer + "\n\n")

            # Insert a personalized question related to the student's learning preferences and hobbies
            personalized_question, correct_answer, explanation = self.create_personalized_question(segment)
            lesson_content += personalized_question + "\n\n"
            print(personalized_question + "\n\n")

            # Wait for student's answer before continuing
            student_answer = input("Please answer the personalized question: ")
            print(f"Student's answer: {student_answer}\n\n")

            # Provide feedback on the student's answer
            if student_answer.strip().lower() == correct_answer.strip().lower():
                print("Correct! Well done!\n\n")
                lesson_content += "Feedback: Correct! Well done!\n\n"
            else:
                print(f"Incorrect. The correct answer is: {correct_answer}\nExplanation: {explanation}\n\n")
                lesson_content += f"Feedback: Incorrect. The correct answer is: {correct_answer}\nExplanation: {explanation}\n\n"

            # Process the answer if needed, then continue with the next segment
            # For now, we'll just break after the first segment
            break

        return lesson_content

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
        prompt = f"Generate a detailed and comprehensive paragraph from the following content suitable for a {self.user_profile.age}-year-old student. The paragraph should be informative, engaging, and cover the topic extensively:\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=300)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    def create_example_question(self, segment):
        prompt = f"Create an example question and provide an answer with an explanation based on the following content to help a {self.user_profile.age}-year-old student understand better. Consider the student's learning preferences: {', '.join(self.user_profile.learning_preferences)}.\n\n{segment}"
        response = self._call_openai_api(prompt, max_tokens=150)
        example_question_answer = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if 'Answer:' in example_question_answer:
            example_question, example_answer = example_question_answer.split('Answer:', 1)
            return example_question.strip(), example_answer.strip()
        else:
            return example_question_answer, "No answer provided"

    def create_personalized_question(self, segment):
        hobby = random.choice(self.user_profile.hobbies)
        learning_preference = self.user_profile.learning_preferences[0]
        prompt = f"Create a question related to {hobby} that incorporates the topic being studied. Provide the correct answer and an explanation for the answer. The question should be appropriate for a {self.user_profile.age}-year-old student with a preference for {learning_preference}.\n\nHere is the segment to base the question on:\n\n{segment}"
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
    manager = UserProfileManager()
    manager.load_profiles_from_file('user_profiles.json')

    user_profile = manager.profiles[0]  # Just an example to use the first profile
    api_key = "sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp"  # Replace with your actual OpenAI API key

    # Path to the folder containing PDF files
    pdf_folder_path = r"C:\Users\Noa fuks\OneDrive\IDC\Third Year B\From Idea To Reality App Using AI tools\Idea-To-Reality-Project\DataBase"

    # Check if the directory exists
    if not os.path.exists(pdf_folder_path):
        print(f"The directory {pdf_folder_path} does not exist.")
    else:
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
