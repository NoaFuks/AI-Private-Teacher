import json
import os
import requests

class ParentProgressPage:
    def __init__(self, progress_directory="progress_data", output_file="children_progress_summary.json", api_key=None):
        self.progress_directory = progress_directory
        self.output_file = output_file
        self.api_key = "sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp"
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

        if (performance_ratio == 1):
            return "Excellent performance! The child answered all questions correctly and demonstrated a strong understanding of the material."
        elif (performance_ratio >= 0.75):
            return "Good performance! The child answered most questions correctly and is grasping the key concepts well."
        elif (performance_ratio >= 0.5):
            return "Fair performance. The child has a basic understanding of the material but may need some additional review to reinforce key concepts."
        else:
            return "Needs improvement. The child struggled with the material and would benefit from extra practice or review."


    def summarize_child_progress(self, student_name):
        progress_data = self.get_child_progress(student_name)
        if not progress_data:
            return f"No progress data available for {student_name}."

        correct_answers = 0
        incorrect_answers = 0
        total_questions = 0
        topics_covered_set = set()  # Using a set to store unique topics

        # Iterate through all the lessons to accumulate data
        for lesson_data in progress_data:
            segments = lesson_data.get('segments', [])
            print(f"Processing {len(segments)} segments in this lesson.")  # Debugging output
            for segment in segments:
                # Check and update question correctness data
                if segment.get('correct') is not None:
                    total_questions += 1
                    if segment['correct']:
                        correct_answers += 1
                    else:
                        incorrect_answers += 1

                # Extract and summarize the segment summary
                segment_summary = segment.get('lesson_summary', '').strip()
                print(f"Processing segment summary: '{segment_summary}'")  # Debugging output

                # Filter out non-informative summaries
                if segment_summary and "lesson segment" not in segment_summary.lower() and "completed" not in segment_summary.lower():
                    summarized_topic = self.summarize_topic(segment_summary)
                    topics_covered_set.add(summarized_topic)  # Add to set to ensure uniqueness

        # Convert set back to a list for ordered display
        topics_covered = list(topics_covered_set)

        print(f"Total segments processed: {len(topics_covered)}")  # Debugging output

        # Calculate percentages
        correct_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        incorrect_percentage = 100 - correct_percentage

        # Generate AI opinion on performance
        ai_opinion = self.generate_ai_opinion(correct_answers, total_questions)

        summary = {
            "Correct Percentage": f"{correct_percentage:.2f}%",
            "Incorrect Percentage": f"{incorrect_percentage:.2f}%",
            "Total Questions": total_questions,
            "Topics Covered": topics_covered,  # Return the summarized topics
            "AI Opinion": ai_opinion
        }

        return summary

    def summarize_topic(self, summary):
        # Check if the summary can be shortened manually
        words = summary.split()
        if len(words) <= 3:
            return summary  # Already 3 words or less
        else:
            # Send a request to the AI to summarize it in 2-3 words
            prompt = f"Summarize the following topic in 3-4 words: {summary} write what the subject of the summery (math, english and etc.) and then write what exactly form this subject"
            summarized_topic = self.request_ai_summary(prompt)
            return summarized_topic

    def request_ai_summary(self, prompt):
        if not self.api_key:
            return "Summary unavailable"  # Fallback if no API key is provided
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 10  # Limit to a short response
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return "Summary unavailable"  # Fallback if the request fails


