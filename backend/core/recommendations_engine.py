class RecommendationsEngine:
    def generate_realtime_recommendations(self, session_status: dict):
        """
        Rule-based recommendations for immediate feedback.
        Input: Session status dict (people, emotions, attention)
        Output: List of { type: 'alert'|'warning'|'info', message: str }
        """
        recs = []

        # 1. Low Attention Alert
        people = session_status.get('people', [])
        if people:
            avg_att = sum(p.get('attention', 0) for p in people) / len(people)

            # Individual check
            for p in people:
                if p.get('attention', 100) < 40:
                    recs.append({
                        'type': 'alert',
                        'message': f"Student {p.get('id', 'Unknown')} is distracted ({p.get('attention', 0)}%)."
                    })

            # 2. Global Attention Warning
            if len(people) >= 2 and avg_att < 60:
                recs.append({
                    'type': 'warning',
                    'message': f"Overall class attention is low ({round(avg_att, 1)}%). Consider an interactive activity."
                })
        else:
            recs.append({
                'type': 'info',
                'message': "No active participants detected in frame."
            })

        return recs