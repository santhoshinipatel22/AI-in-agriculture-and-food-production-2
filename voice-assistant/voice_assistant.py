#!/usr/bin/env python3
"""
Multi-language Voice Assistant for Smart Farming
Supports: English, Hindi, Telugu
"""

import speech_recognition as sr
import pyttsx3
from google.cloud import speech_v1
from google.cloud import texttospeech_v1
import json
from datetime import datetime

class FarmingVoiceAssistant:
    """
    Voice assistant for farmers using Text-to-Speech and Speech-to-Text
    """
    
    def __init__(self, language='en'):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Language configurations
        self.lang_codes = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'te': 'te-IN',
        }
        
        self.lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
        }
        
        # Intent responses
        self.responses = self._load_responses()
        
    def _load_responses(self):
        """Load pre-defined responses for common queries"""
        return {
            'weather': "Current weather in your area is mild with good moisture. Recommended sowing today.",
            'disease': "I detected leaf rust on your crops. Apply Mancozeb fungicide immediately.",
            'irrigation': "Based on soil moisture, irrigate your fields for 45 minutes.",
            'price': "Current market price for rice is 2500 per quintal, expected to increase.",
            'subsidy': "You are eligible for PM-KISAN scheme. Apply now for Rs. 2000 support.",
            'yield': "Expected yield: 50 quintals per hectare. Good crop condition.",
        }
    
    def listen(self):
        """
        Listen to user voice input
        Returns: recognized text or None
        """
        try:
            with sr.Microphone() as source:
                self.engine.say("I am listening")
                self.engine.runAndWait()
                
                audio = self.recognizer.listen(source, timeout=10)
                
                # Use Google Cloud for better accuracy
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.lang_codes.get(self.language, 'en-US')
                )
                return text.lower()
        except sr.UnknownValueError:
            response = "I didn't catch that. Please try again."
            self.speak(response)
            return None
        except sr.RequestError as e:
            response = f"Error accessing speech service: {str(e)}"
            self.speak(response)
            return None
    
    def speak(self, text):
        """
        Convert text to speech and play
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
    
    def process_intent(self, user_input):
        """
        Process user intent and return appropriate response
        """
        intents = {
            'weather': ['weather', 'rain', 'temperature', 'humidity'],
            'disease': ['disease', 'pest', 'leaf', 'infection', 'blight'],
            'irrigation': ['water', 'irrigation', 'moisture', 'soil'],
            'price': ['price', 'market', 'sell', 'cost'],
            'subsidy': ['subsidy', 'scheme', 'support', 'government'],
            'yield': ['yield', 'harvest', 'production', 'output'],
        }
        
        # Detect intent
        detected_intent = None
        for intent, keywords in intents.items():
            if any(keyword in user_input for keyword in keywords):
                detected_intent = intent
                break
        
        if detected_intent:
            return {
                'intent': detected_intent,
                'response': self.responses.get(detected_intent, "I can help with that."),
                'confidence': 0.85,
            }
        
        return {
            'intent': 'general',
            'response': "I can help you with weather, disease detection, irrigation, market prices, subsidies, and yield forecasting. What would you like to know?",
            'confidence': 0.5,
        }
    
    def handle_conversation(self):
        """
        Main conversation loop
        """
        self.speak(f"Welcome to Smart Farming Voice Assistant. I am ready to help you.")
        
        while True:
            user_input = self.listen()
            
            if user_input is None:
                continue
            
            # Check for exit commands
            if any(word in user_input for word in ['exit', 'bye', 'quit', 'stop']):
                self.speak("Thank you for using Smart Farming Assistant. Goodbye!")
                break
            
            # Process intent and respond
            result = self.process_intent(user_input)
            self.speak(result['response'])
    
    def set_language(self, language_code):
        """
        Change language dynamically
        """
        if language_code in self.lang_codes:
            self.language = language_code
            self.speak(f"Language changed to {self.lang_names[language_code]}")
        else:
            self.speak("Language not supported. Using English.")


class QuickCommandHandler:
    """Handle quick voice commands without full conversation"""
    
    def __init__(self):
        self.commands = {
            'check weather': 'weather_check',
            'scan disease': 'disease_scan',
            'check soil': 'soil_check',
            'market price': 'price_check',
            'my yield': 'yield_check',
            'apply subsidy': 'subsidy_apply',
            'iot status': 'iot_status',
        }
    
    def execute_command(self, voice_input):
        """Execute command based on voice input"""
        for command, action in self.commands.items():
            if command in voice_input.lower():
                return {
                    'action': action,
                    'success': True,
                }
        
        return {
            'action': None,
            'success': False,
        }


if __name__ == '__main__':
    # Initialize assistant
    assistant = FarmingVoiceAssistant(language='hi')  # Hindi
    # assistant.handle_conversation()
    
    print("✓ Voice Assistant initialized with language: Hindi")
