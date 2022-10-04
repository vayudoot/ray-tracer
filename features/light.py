from __future__ import annotations

class Light:
    def __init__(self, position: Tuple, intensity: Color):
        self.position = position
        self.intensity = intensity

    def __eq__(self, other):
        return (isinstance(other, Light) and
                self.position == other.position and
                self.intensity == other.intensity)

    def __str__(self):
        return f"Light: {{Position: {self.position}, Intensity: {self.intensity}}}"
