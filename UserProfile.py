import json
from pathlib import Path
from openai import OpenAI
from playsound import playsound
import uuid

client = OpenAI(api_key="sk-proj-hOTTh1Qv8iNbIumiJ3S6T3BlbkFJcB15KrFMIjwvwamTTPPp")

class UserProfile:
    def __init__(self, name, age, hobbies, learning_preferences):
        self.name = name
        self.age = age
        self.hobbies = hobbies
        self.learning_preferences = learning_preferences

    # Save the profile to dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "hobbies": self.hobbies,
            "learning_preferences": self.learning_preferences
        }

class UserProfileManager:
    def __init__(self):
        self.profiles = []

    def add_profile(self, profile):
        self.profiles.append(profile)

    def save_profiles_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([profile.to_dict() for profile in self.profiles], file, indent=4)

    def load_profiles_from_file(self, filename):
        with open(filename, 'r') as file:
            profiles_data = json.load(file)
            self.profiles = [UserProfile(**data) for data in profiles_data]

def ask_question(question_text):
    speech_file_path = f"question_{uuid.uuid4()}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=question_text
    )
    response.stream_to_file(speech_file_path)
    playsound(str(speech_file_path))
    print(f"Playing: {question_text}")

if __name__ == "__main__":

    manager = UserProfileManager()

    # Ask and collect user profile data
    ask_question("Enter your name:")
    name = input("Enter your name: ")

    ask_question("Enter your age:")
    age = int(input("Enter your age: "))

    ask_question("Enter your hobbies (comma-separated):")
    hobbies = input("Enter your hobbies (comma-separated): ").split(',')

    ask_question("Enter your learning preferences (comma-separated):")
    learning_preferences = input("Enter your learning preferences (comma-separated): ").split(',')

    # Create a new user profile
    profile = UserProfile(name, age, hobbies, learning_preferences)
    manager.add_profile(profile)

    # Save profiles to a file
    manager.save_profiles_to_file('user_profiles.json')

    # Load profiles from a file (for testing)
    manager.load_profiles_from_file('user_profiles.json')
    for p in manager.profiles:
        print(p.to_dict())
