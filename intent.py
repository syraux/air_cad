import time


class IntentManager:
    STATES = ["IDLE", "SELECTING", "DRAGGING", "CREATING"]

    def __init__(self):
        self.current_state = "IDLE"
        self.selected_object = None
        self.last_pinch_pos = None
        self.drag_offset = (0, 0)

    def update_intent(self, gesture, hand_pos_screen, scene_graph, camera_renderer):
        """
        Updates the state machine based on gestures and scene context.
        hand_pos_screen: (x, y) coordinates of the 'cursor' (e.g., pinch center)
        """

        # STATE: IDLE
        if self.current_state == "IDLE":
            if gesture == "PINCH":
                # Check for object selection
                hit_obj = self._raycast(hand_pos_screen, scene_graph, camera_renderer)
                if hit_obj:
                    self.selected_object = hit_obj
                    self.selected_object.selected = True
                    self.current_state = "DRAGGING"
                    self.last_pinch_pos = hand_pos_screen
                else:
                    self.current_state = "SELECTING"  # Or "CREATING" logic could go here
            elif gesture == "OPEN":
                # potentially clear selection if open palm for X seconds
                pass

        # STATE: DRAGGING
        elif self.current_state == "DRAGGING":
            if gesture == "PINCH":
                # Continue Dragging
                if self.selected_object and self.last_pinch_pos:
                    dx = hand_pos_screen[0] - self.last_pinch_pos[0]
                    dy = hand_pos_screen[1] - self.last_pinch_pos[1]

                    # Map Screen Delta to World Delta (Approximation)
                    # In a real system you'd unproject. Here we just scale down
                    scale_factor = 0.01
                    self.selected_object.position[0] += dx * scale_factor
                    self.selected_object.position[1] -= dy * scale_factor  # Y is inverted screen vs world

                    self.last_pinch_pos = hand_pos_screen
            else:
                # Released
                self.current_state = "IDLE"
                if self.selected_object:
                    self.selected_object.selected = False
                    self.selected_object = None

        # STATE: SELECTING (Empty pinch)
        elif self.current_state == "SELECTING":
            if gesture != "PINCH":
                self.current_state = "IDLE"

        return self.current_state

    def _raycast(self, screen_pos, scene, renderer):
        """
        Very simple 'hit test' based on screen-space proximity to object projection.
        Real raycasting is complex; this is a heuristic for the prototype.
        """
        if not screen_pos:
            return None

        closest_obj = None
        min_dist = 50.0  # Pixel threshold

        for obj in scene.get_objects():
            # Project object center to screen
            proj = renderer.project_point(obj.position)
            if proj:
                dx = screen_pos[0] - proj[0]
                dy = screen_pos[1] - proj[1]
                dist = (dx ** 2 + dy ** 2) ** 0.5

                if dist < min_dist:
                    min_dist = dist
                    closest_obj = obj

        return closest_obj
