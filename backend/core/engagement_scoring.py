class EngagementScorer:
    def __init__(self, visual_weight=0.6, audio_weight=0.4):
        self.visual_weight = visual_weight
        self.audio_weight = audio_weight

    def calculate_score(self, visual_data: dict, audio_data: dict) -> dict:
        """
        Transforms fused multimodal signals into interpretable engagement scores.
        """
        # Visual scoring: Presence and movement duration
        presence_ratio = visual_data.get("presence_ratio", 1.0)
        visual_score = min(100, max(0, presence_ratio * 100))

        # Audio scoring: Speech vs silence and noise floor
        speech_ratio = audio_data.get("speech_ratio", 0.0)
        # Moderate speech indicates healthy interaction
        if 0.2 <= speech_ratio <= 0.7:
            audio_score = 90
        elif speech_ratio > 0.7:
            audio_score = 75  # Potential disturbance/excess noise
        else:
            audio_score = 60  # Passive listening/silence

        # Fused total engagement calculation
        total_score = (visual_score * self.visual_weight) + (audio_score * self.audio_weight)

        if total_score >= 80:
            level = "High"
        elif total_score >= 60:
            level = "Medium"
        else:
            level = "Low"

        return {
            "engagement_score": round(total_score, 2),
            "engagement_level": level,
            "visual_component": round(visual_score, 2),
            "audio_component": round(audio_score, 2)
        }