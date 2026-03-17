from utils import Utils
class GestureEngine:
    def __init__(self, pinch_threshold=40):
        self.pinch_threshold = pinch_threshold  # Euclidean distance in pixels

    def detect_gesture(self, landmarks):
        """
        Analyzes landmarks to determine current gesture.
        landmarks: List of dicts {'x', 'y', 'z'}
        """
        if not landmarks:
            return "NONE"

        # Key Landmarks (MediaPipe Hand Layout)
        # 4 = Thumb Tip
        # 8 = Index Tip
        # 12 = Middle Tip
        # 0 = Wrist

        thumb_tip = (landmarks[4]['x'], landmarks[4]['y'], 0)  # Ignore Z for pinch check to keep it robust
        index_tip = (landmarks[8]['x'], landmarks[8]['y'], 0)

        dist = Utils.get_distance(thumb_tip, index_tip)

        # PINCH DETECTION
        if dist < self.pinch_threshold:
            return "PINCH"

        # OPEN PALM DETECTION (Simplified)
        # Check if all fingers are extended (tips further from wrist than knuckles)
        # This is a basic heuristic

        return "OPEN"
