import json
import uuid
import sounddevice as sd
import wave
import os
from word2number import w2n
from openai import OpenAI
from playsound import playsound

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
    os.remove(speech_file_path)
    print(f"Playing: {question_text}")

def record_audio(filename, duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())
    print("Recording complete")

def get_user_response():
    audio_path = f"response_{uuid.uuid4()}.wav"
    record_audio(audio_path)
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"  # Explicitly set the language to English
        )
    os.remove(audio_path)
    print("Response:", transcript.text)  # Debugging line to inspect the response structure
    return transcript.text

def validate_age(age_text):
    try:
        cleaned_text = age_text.replace('.', '').strip().lower()
        age = w2n.word_to_num(cleaned_text)
        if age > 0:
            return age
    except Exception as e:
        print(f"Error converting age: {e}")
    return None

if __name__ == "__main__":
    manager = UserProfileManager()

    # Ask and collect user profile data
    while True:
        ask_question("What is your name?")
        name = get_user_response().strip()
        if name:
            break
        print("Invalid input. Please try again.")

    while True:
        ask_question("What is your age?")
        age_text = get_user_response().strip()
        age = validate_age(age_text)
        if age is not None:
            break
        print("Invalid age. Please enter a valid number.")

    while True:
        ask_question("Tell me about something that you like")
        hobbies = get_user_response().strip()
        if hobbies:
            hobbies = [hobbies.strip()]
            break
        print("Invalid input. Please try again.")

    while True:
        ask_question("What do you want to learn?")
        learning_preferences = get_user_response().strip()
        if learning_preferences:
            learning_preferences = [learning_preferences.strip()]
            break
        print("Invalid input. Please try again.")

    # Create a new user profile
    profile = UserProfile(name, age, hobbies, learning_preferences)
    manager.add_profile(profile)

    # Save profiles to a file
    manager.save_profiles_to_file('user_profiles.json')

    # Load profiles from a file (for testing)
    manager.load_profiles_from_file('user_profiles.json')
    for p in manager.profiles:
        print(p.to_dict())
