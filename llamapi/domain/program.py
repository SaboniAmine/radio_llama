from typing import List, Any

from llamapi.domain.track import Track


class Program:
    tracklist: List[Track]
    name: str
    animator_profile: Any

    def __init__(self, tracklist: List[Track], name: str, animator_profile: Any):
        self.tracklist = tracklist
        self.name = name
        self.animator_profile = animator_profile

    def generate_radio(self, mood: str):
        return True
