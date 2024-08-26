# import json
# import os
#
#
# class ParentProgressPage:
#     def __init__(self, progress_directory="progress_data", output_file="children_progress_summary.json"):
#         self.progress_directory = progress_directory
#         self.output_file = output_file
#         if not os.path.exists(progress_directory):
#             raise FileNotFoundError(f"The progress directory '{progress_directory}' does not exist.")
#
#     def get_child_progress(self, student_name):
#         progress_files = [
#             os.path.join(self.progress_directory, f) for f in os.listdir(self.progress_directory)
#             if f.startswith(student_name) and f.endswith('_progress.json')
#         ]
#
#         if not progress_files:
#             print(f"No progress file found for {student_name}.")
#             return []
#
#         progress_data = []
#         try:
#             for file in progress_files:
#                 with open(file, 'r') as file_handle:
#                     progress_data.append(json.load(file_handle))
#             return progress_data
#         except Exception as e:
#             print(f"Failed to load progress for {student_name}: {e}")
#             return []
#
#     def generate_ai_opinion(self, correct_answers, total_questions):
#         performance_ratio = correct_answers / total_questions if total_questions > 0 else 0
#
#         if performance_ratio == 1:
#             return "Excellent performance! The child answered all questions correctly and demonstrated a strong understanding of the material."
#         elif performance_ratio >= 0.75:
#             return "Good performance! The child answered most questions correctly and is grasping the key concepts well."
#         elif performance_ratio >= 0.5:
#             return "Fair performance. The child has a basic understanding of the material but may need some additional review to reinforce key concepts."
#         else:
#             return "Needs improvement. The child struggled with the material and would benefit from extra practice or review."
#
#     def summarize_child_progress(self, student_name):
#         progress_data = self.get_child_progress(student_name)
#         if not progress_data:
#             return f"No progress data available for {student_name}."
#
#         total_lessons = len(progress_data)
#         correct_answers = 0
#         incorrect_answers = 0
#         total_questions = 0
#         topics_covered = []
#
#         for lesson_data in progress_data:
#             for segment in lesson_data.get('segments', []):
#                 if segment.get('correct') is not None:
#                     total_questions += 1
#                     if segment['correct']:
#                         correct_answers += 1
#                     else:
#                         incorrect_answers += 1
#                 topics_covered.append(segment.get('lesson_name', 'Unknown topic'))
#
#         # Generate AI opinion on performance
#         ai_opinion = self.generate_ai_opinion(correct_answers, total_questions)
#
#         summary = {
#             "Total Lessons": total_lessons,
#             "Total Questions": total_questions,
#             "Correct Answers": correct_answers,
#             "Incorrect Answers": incorrect_answers,
#             "Topics Covered": list(set(topics_covered)),  # Removing duplicate topics
#             "AI Opinion": ai_opinion
#         }
#
#         return summary
#
#     def get_all_children_progress(self):
#         children_progress = {}
#         for file_name in os.listdir(self.progress_directory):
#             if file_name.endswith('_progress.json'):
#                 student_name = '_'.join(file_name.split('_')[:-2])  # Extract the student's name
#                 progress_summary = self.summarize_child_progress(student_name)
#                 if progress_summary:
#                     children_progress[student_name] = progress_summary
#
#         return children_progress
#
#     def save_progress_to_json(self):
#         summary = self.get_all_children_progress()
#
#         if not summary:
#             print("No data to save.")
#             return
#
#         try:
#             with open(self.output_file, 'w') as file:
#                 json.dump(summary, file, indent=4)
#             print(f"Progress summary saved to {self.output_file}")
#         except Exception as e:
#             print(f"Failed to save progress summary: {e}")
#
#
# # Example usage:
# if __name__ == "__main__":
#     parent_page = ParentProgressPage()
#
#     # Save progress summary for all children to a JSON file
#     parent_page.save_progress_to_json()


import json
import os

class ParentProgressPage:
    def __init__(self, progress_directory="progress_data", output_file="children_progress_summary.json"):
        self.progress_directory = progress_directory
        self.output_file = output_file
        if not os.path.exists(progress_directory):
            raise FileNotFoundError(f"The progress directory '{progress_directory}' does not exist.")

    def get_child_progress(self, student_name):
        progress_files = [
            os.path.join(self.progress_directory, f) for f in os.listdir(self.progress_directory)
            if f.startswith(student_name) and f.endswith('_progress.json')
        ]

        if not progress_files:
            print(f"No progress file found for {student_name}.")
            return []

        progress_data = []
        try:
            for file in progress_files:
                with open(file, 'r') as file_handle:
                    progress_data.append(json.load(file_handle))
            return progress_data
        except Exception as e:
            print(f"Failed to load progress for {student_name}: {e}")
            return []

    def generate_ai_opinion(self, correct_answers, total_questions):
        performance_ratio = correct_answers / total_questions if total_questions > 0 else 0

        if performance_ratio == 1:
            return "Excellent performance! The child answered all questions correctly and demonstrated a strong understanding of the material."
        elif performance_ratio >= 0.75:
            return "Good performance! The child answered most questions correctly and is grasping the key concepts well."
        elif performance_ratio >= 0.5:
            return "Fair performance. The child has a basic understanding of the material but may need some additional review to reinforce key concepts."
        else:
            return "Needs improvement. The child struggled with the material and would benefit from extra practice or review."

    def summarize_child_progress(self, student_name):
        progress_data = self.get_child_progress(student_name)
        if not progress_data:
            return f"No progress data available for {student_name}."

        total_lessons = len(progress_data)
        correct_answers = 0
        incorrect_answers = 0
        total_questions = 0
        topics_covered = []

        for lesson_data in progress_data:
            for segment in lesson_data.get('segments', []):
                if segment.get('correct') is not None:
                    total_questions += 1
                    if segment['correct']:
                        correct_answers += 1
                    else:
                        incorrect_answers += 1
                topics_covered.append(segment.get('lesson_name', 'Unknown topic'))

        # Generate AI opinion on performance
        ai_opinion = self.generate_ai_opinion(correct_answers, total_questions)

        summary = {
            "Total Lessons": total_lessons,
            "Total Questions": total_questions,
            "Correct Answers": correct_answers,
            "Incorrect Answers": incorrect_answers,
            "Topics Covered": list(set(topics_covered)),  # Removing duplicate topics
            "AI Opinion": ai_opinion
        }

        return summary
