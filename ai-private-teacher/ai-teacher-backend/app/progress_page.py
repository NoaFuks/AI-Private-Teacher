import json
import os

class ProgressTracker:
    def __init__(self, student_name, progress_directory="progress_data"):
        self.student_name = student_name
        self.progress_directory = progress_directory
        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)
        self.progress_file = os.path.join(self.progress_directory, f"{self.student_name}_progress.json")

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as file:
                return json.load(file)
        return {}

    def save_progress_page(self, lesson_name, lesson_data):
        progress_data = self.load_progress()

        # Determine the lesson number based on existing lessons
        lesson_number = len(progress_data) + 1
        lesson_key = f"part_{lesson_number}"

        # Add the new lesson data under the lesson number
        progress_data[lesson_key] = {"lesson_name": lesson_name, "data": lesson_data}

        # Save the updated progress to the same file
        try:
            with open(self.progress_file, 'w') as file:
                json.dump(progress_data, file, indent=4)
            print(f"Progress page saved to {self.progress_file}")
        except Exception as e:
            print(f"Failed to save progress: {e}")

    def update_progress(self, lesson, correct, explanation="", interaction_details=None, lesson_summary=""):
        lesson_data = {
            'lesson_summary': lesson_summary,
            'correct': correct,
            'attempts': 1,
            'explanations': [explanation] if explanation else [],
            'details': [{
                "interaction_details": interaction_details.get('interaction_details', []),
                "student_questions": interaction_details.get('student_questions', [])
            }] if interaction_details else []
        }

        self.save_progress_page(lesson, lesson_data)

