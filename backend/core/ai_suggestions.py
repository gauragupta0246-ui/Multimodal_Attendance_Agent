import os
from groq import Groq

class AISuggestionEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "gsk_dummy_key")
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception:
            self.client = None

    def generate_suggestions(self, session_data: dict) -> dict:
        prompt = f"""
        Based on fused multimodal inputs:
        - Student Engagement: {session_data.get('engagement_score', 'Medium')}
        - Audio State: {session_data.get('audio_status', 'Normal')}
        Give teaching assistant suggestions.
        """
        try:
            if not self.client or self.api_key == "gsk_dummy_key":
                raise ValueError("Client offline")

            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert AI teaching assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=200
            )
            response = completion.choices[0].message.content
            return self._parse_response(response)
        except Exception as e:
            print(f"AI suggestion Error: {e}")
            return self._fallback_suggestions(session_data)

    def _parse_response(self, response: str) -> dict:
        return {
            "suggestions": response,
            "status": "generated"
        }

    def _fallback_suggestions(self, session_data: dict) -> dict:
        return {
            "suggestions": "Encourage more student interaction and verify all cameras are active.",
            "status": "fallback"
        }