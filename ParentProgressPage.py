import json
import os

class ParentProgressPage:
    def __init__(self, progress_directory="progress_data", output_file="children_progress_summary.json"):
        self.progress_directory = progress_directory
        self.output_file = output_file
        if not os.path.exists(progress_directory):
            raise FileNotFoundError(f"The progress directory '{progress_directory}' does not exist.")

    def get_child_progress(self, student_name):
        progress_file = os.path.join(self.progress_directory, f"{student_name}_progress.json")
        if not os.path.exists(progress_file):
            print(f"No progress file found for {student_name}.")
            return {}

        try:
            with open(progress_file, 'r') as file:
                progress_data = json.load(file)
                return progress_data
        except Exception as e:
            print(f"Failed to load progress for {student_name}: {e}")
            return {}

    def generate_ai_opinion(self, correct_answers, total_lessons):
        performance_ratio = correct_answers / total_lessons if total_lessons > 0 else 0

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
        correct_answers = sum(1 for lesson_info in progress_data.values() if lesson_info.get('data', {}).get('correct', 0) > 0)
        incorrect_answers = total_lessons - correct_answers
        topics_covered = [lesson_info.get('data', {}).get('lesson_summary', 'Unknown topic') for lesson_info in progress_data.values()]

        # Generate AI opinion on performance
        ai_opinion = self.generate_ai_opinion(correct_answers, total_lessons)

        summary = {
            "Total Lessons": total_lessons,
            "Correct Answers": correct_answers,
            "Incorrect Answers": incorrect_answers,
            "Topics Covered": list(set(topics_covered)),  # Removing duplicate topics
            "AI Opinion": ai_opinion
        }

        return summary

    def get_all_children_progress(self):
        children_progress = {}
        for file_name in os.listdir(self.progress_directory):
            if file_name.endswith('_progress.json'):
                student_name = file_name.replace('_progress.json', '')
                progress_summary = self.summarize_child_progress(student_name)
                if progress_summary:
                    children_progress[student_name] = progress_summary

        return children_progress

    def save_progress_to_json(self):
        summary = self.get_all_children_progress()

        if not summary:
            print("No data to save.")
            return

        try:
            with open(self.output_file, 'w') as file:
                json.dump(summary, file, indent=4)
            print(f"Progress summary saved to {self.output_file}")
        except Exception as e:
            print(f"Failed to save progress summary: {e}")


# Example usage:
if __name__ == "__main__":
    parent_page = ParentProgressPage()

    # Save progress summary for all children to a JSON file
    parent_page.save_progress_to_json()
