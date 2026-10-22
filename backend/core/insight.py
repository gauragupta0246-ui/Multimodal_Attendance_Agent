import os
from groq import Groq

class InsightGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "gsk_dummy_key")
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception:
            self.client = None

    def generate_classroom_insight(self, session_data: dict) -> dict:
        prompt = f"""
        Analyze the following classroom session metrics and provide actionable insights:
        - Visual Presence: {session_data.get('presence_score', 0)}%
        - Audio/Speech Activity: {session_data.get('speech_ratio', 0)}
        - Average Noise Level: {session_data.get('noise_level_db', 0)} dB
        """
        try:
            if not self.client or self.api_key == "gsk_dummy_key":
                raise ValueError("Groq client not initialized")

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational AI assistant. Provide brief, professional, and actionable insights for educators."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.5,
                max_tokens=150,
            )
            response_text = chat_completion.choices[0].message.content
            return {
                "insight": response_text,
                "status": "success"
            }
        except Exception as e:
            # Fallback when API key is missing or offline
            return {
                "insight": "Class status is stable. Good visual attention observed with moderate participation.",
                "recommendation": "Maintain current pace.",
                "error": str(e)
            }