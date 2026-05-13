import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class GroqPersonalizer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=self.api_key)
        
        with open("prompts/personalization_prompt.txt", "r") as f:
            self.prompt_template = f.read()

    def generate_first_lines(self, df):
        print(f"Generating personalized lines for {len(df)} companies using {self.model}...")
        
        personalizations = []
        for index, row in df.iterrows():
            try:
                first_line = self._get_ai_line(row)
                personalizations.append(first_line)
            except Exception as e:
                print(f"Error generating line for {row['name']}: {e}")
                personalizations.append("Noticed your work in the composites space — curious about your CAMX showcase focus.")
                
        df['personalized_first_line'] = personalizations
        return df

    def _get_ai_line(self, row):
        prompt = self.prompt_template.format(
            company_name=row['name'],
            industry=row.get('industry', 'Manufacturing'),
            description=row.get('description', 'N/A'),
            categories=row.get('categories', 'N/A')
        )
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return completion.choices[0].message.content.strip().strip('"')

if __name__ == "__main__":
    # Test logic
    pass
