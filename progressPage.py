import json
import os


class ProgressTracker:
    def __init__(self, student_name, progress_directory="progress_data"):
        self.student_name = student_name
        self.progress_directory = progress_directory
        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def load_progress(self, lesson_number=None):
        if lesson_number is None:
            # Load all lessons
            progress_files = sorted(os.listdir(self.progress_directory))
            progress_data = {}
            for filename in progress_files:
                with open(os.path.join(self.progress_directory, filename), 'r') as file:
                    lesson_data = json.load(file)
                    progress_data.update(lesson_data)
            return progress_data
        else:
            # Load a specific lesson by its number
            filename = f"{self.student_name}_lesson_{lesson_number}.json"
            file_path = os.path.join(self.progress_directory, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    return json.load(file)
            return {}

    def get_progress_summary(self):
        summary = {}
        progress_files = sorted(os.listdir(self.progress_directory))

        for filename in progress_files:
            with open(os.path.join(self.progress_directory, filename), 'r') as file:
                lesson_data = json.load(file)
                for lesson, data in lesson_data.items():
                    correct_ratio = data['correct'] / data['attempts'] if data['attempts'] > 0 else 0
                    summary[lesson] = {
                        'correct_ratio': correct_ratio,
                        'total_attempts': data['attempts']
                    }

        return summary

    def save_progress_page(self, lesson_name, lesson_data):
        # Create the file name based on the number of existing files in the directory
        existing_files = os.listdir(self.progress_directory)
        lesson_number = len(existing_files) + 1
        progress_page_filename = f"{self.student_name}_lesson_{lesson_number}.json"

        # Save the progress in a new file
        progress_page_path = os.path.join(self.progress_directory, progress_page_filename)

        try:
            with open(progress_page_path, 'w') as file:
                json.dump({lesson_name: lesson_data}, file, indent=4)
            print(f"Progress page saved as {progress_page_filename}")
        except Exception as e:
            print(f"Failed to save progress page {progress_page_filename}: {e}")

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

        # Save the updated progress to a new JSON file
        self.save_progress_page(lesson, lesson_data)
