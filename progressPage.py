import json
import os

class ProgressTracker:
    def __init__(self, student_name, progress_file="student_progress.json"):
        self.student_name = student_name
        self.progress_file = progress_file
        self.progress_data = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as file:
                return json.load(file).get(self.student_name, {})
        return {}

    def save_progress(self):
        all_progress = {}
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as file:
                all_progress = json.load(file)

        all_progress[self.student_name] = self.progress_data
        with open(self.progress_file, 'w') as file:
            json.dump(all_progress, file, indent=4)

    def update_progress(self, lesson, correct, explanation=""):
        if lesson not in self.progress_data:
            self.progress_data[lesson] = {'correct': 0, 'attempts': 0, 'explanations': []}

        self.progress_data[lesson]['correct'] += correct
        self.progress_data[lesson]['attempts'] += 1

        if explanation:
            self.progress_data[lesson]['explanations'].append(explanation)

        self.save_progress()

    def get_progress_summary(self):
        summary = {}
        for lesson, data in self.progress_data.items():
            correct_ratio = data['correct'] / data['attempts'] if data['attempts'] > 0 else 0
            summary[lesson] = {
                'correct_ratio': correct_ratio,
                'total_attempts': data['attempts']
            }
        return summary
