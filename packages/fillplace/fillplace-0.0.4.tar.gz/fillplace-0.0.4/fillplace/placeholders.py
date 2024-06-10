import os
from collections import defaultdict
# from dotenv import load_dotenv
import google.generativeai as genai
# Load environment variables from .env file
# load_dotenv()

# Configure the Generative AI API with the key from .env file
# api_key = os.getenv("AIzaSyCPcJP36fwFW-gudrz4B8gDgaA57qF11p0")
genai.configure(api_key="AIzaSyCPcJP36fwFW-gudrz4B8gDgaA57qF11p0")
model = genai.GenerativeModel('gemini-1.5-flash')

class PlaceholderManager:
    def __init__(self):
        self.placeholders = defaultdict(dict)
        self.placeholders_types = {"city", "malename", "femalename", "indianaddress", "internationaladdress", "phone", "dateofbirth", "password", "indiancity", "indianstate"}

    def list_placeholders(self):
        return self.placeholders_types


    def generate_ai_content(self, prompt):
        response = model.generate_content(prompt)
        # Extract and return the first line of the response as the desired content
        return response.text.split('\n')[0].strip()

    def city(self):
        return self.generate_ai_content("Generate a single random city name.")

    def malename(self):
        return self.generate_ai_content("Generate a single random male's name.")

    def femalename(self):
        return self.generate_ai_content("Generate a single random female's name.")
    
    def indianaddress(self):
        return self.generate_ai_content("Create a fictional address for a fictional indian character in a novel. "
        "Ensure the address is not real. Format: Street Number, Street Name, City, State, ZIP Code.")
    
    def internationaladdress(self):
        return self.generate_ai_content("Create a fictional address for a fictional character in a novel. "
        "Ensure the address is not real. Format: Street Number, Street Name, City, State, ZIP Code.")

    def phone(self):
        return self.generate_ai_content("Generate a single random 12 digits start with +91.")
    
    def dateofbirth(self):
        return self.generate_ai_content("Generate a single random date of birth.")
    
    def password(self):
        return self.generate_ai_content("Generate a single random password.")

    def indiancity(self):
        return self.generate_ai_content("Generate a single random Indian city name.")
    
    def indianstate(self):
        return self.generate_ai_content("Generate a single random Indian state name.")

