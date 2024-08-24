# import json
# import os
#
# class ProgressTracker:
#     def __init__(self, student_name, progress_directory="progress_data"):
#         self.student_name = student_name
#         self.progress_directory = progress_directory
#         if not os.path.exists(progress_directory):
#             os.makedirs(progress_directory)
#         self.progress_file = os.path.join(self.progress_directory, f"{self.student_name}_progress.json")
#
#     def load_progress(self):
#         if os.path.exists(self.progress_file):
#             with open(self.progress_file, 'r') as file:
#                 return json.load(file)
#         return {}
#
#     def save_progress_page(self, lesson_name, lesson_data):
#         progress_data = self.load_progress()
#
#         # Determine the lesson number based on existing lessons
#         lesson_number = len(progress_data) + 1
#         lesson_key = f"part_{lesson_number}"
#
#         # Add the new lesson data under the lesson number
#         progress_data[lesson_key] = {"lesson_name": lesson_name, "data": lesson_data}
#
#         # Save the updated progress to the same file
#         try:
#             with open(self.progress_file, 'w') as file:
#                 json.dump(progress_data, file, indent=4)
#             print(f"Progress page saved to {self.progress_file}")
#         except Exception as e:
#             print(f"Failed to save progress: {e}")
#
#     def update_progress(self, lesson, correct, explanation="", interaction_details=None, lesson_summary=""):
#         lesson_data = {
#             'lesson_summary': lesson_summary,
#             'correct': correct,
#             'attempts': 1,
#             'explanations': [explanation] if explanation else [],
#             'details': [{
#                 "interaction_details": interaction_details.get('interaction_details', []),
#                 "student_questions": interaction_details.get('student_questions', [])
#             }] if interaction_details else []
#         }
#
#         self.save_progress_page(lesson, lesson_data)
#

import json
import os
import re


class ProgressTracker:
    def __init__(self, student_name, progress_directory="progress_data"):
        self.student_name = student_name
        self.progress_directory = progress_directory
        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

        # Determine the lesson number based on existing files in the directory
        self.lesson_number = self.determine_lesson_number()

        # Include lesson number in the file name
        self.progress_file = os.path.join(self.progress_directory,
                                          f"{self.student_name}_lesson_{self.lesson_number}_progress.json")

        # Initialize progress data
        self.current_progress = self.load_progress()

        # Determine the starting part number based on existing parts in the file
        self.current_part_number = len(self.current_progress) + 1

    def determine_lesson_number(self):
        # Determine the lesson number based on existing files in the directory
        existing_files = [f for f in os.listdir(self.progress_directory) if f.startswith(self.student_name)]
        if existing_files:
            # Extract the highest lesson number from existing files
            lesson_numbers = [int(re.search(r'_lesson_(\d+)_progress', f).group(1)) for f in existing_files if
                              re.search(r'_lesson_(\d+)_progress', f)]
            return max(lesson_numbers) + 1
        return 1

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as file:
                return json.load(file)
        return {}

    def save_progress_page(self, lesson_name, lesson_data):
        # Load existing progress data
        progress_data = self.load_progress()

        # Add the new lesson data under the current part number
        lesson_key = f"part_{self.current_part_number}"
        progress_data[lesson_key] = {"lesson_name": lesson_name, "data": lesson_data}

        # Save the updated progress to the file
        try:
            with open(self.progress_file, 'w') as file:
                json.dump(progress_data, file, indent=4)
            print(f"Progress page saved to {self.progress_file}")
        except Exception as e:
            print(f"Failed to save progress: {e}")

        # Increment the part number for the next part of the same lesson
        self.current_part_number += 1

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


