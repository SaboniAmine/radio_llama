import os
import subprocess
import boto3
import requests
from datetime import datetime

from starlette.responses import FileResponse

from llamapi.domain.program import Program
from llamapi.infra.repositories.programs import SqlAlchemyRepository
from llamapi.domain.narrator import get_script, get_speech
from llamapi.domain.assemble import generate_radio


class ProgramGenerationService:
    def __init__(self, program_repository: SqlAlchemyRepository):
        self.program_repository = program_repository
        self.spotify_url = "https://api.spotify.com/v1/recommendations"
        self.access_token = os.getenv("SPOTIFY_ACCESS_TOKEN", "BQDHNbRC7CnOguX9yQDgxeE-20_sD9prtbWLxZVSz74uBv3HTsB-31Ecdh-iaHomNPP2yP2BQ8YpvKNO6E4bk_d3g_Mese5sWsV4HN-7iPcfvbRiCOs")
        self.output_file = "output.mp3"

    def generate_program(self, program: Program):

        now = datetime.now()

        genres = program.genre
        print("Getting Recommendations...")
        tracks = self.get_recommendations(genres)
        if tracks is None:
            print("No recommendations found")
            return

        print("Recommendations:")
        print(tracks)

        output_folder = "assets/"

        print("Downloading tracks...")
        tracks = self.download_tracks(tracks, output_folder)

        print("Tracks downloaded:")
        print(tracks)

        ## Get the metadata of the musics

        ## Generate Voice Tracking text

        tone = "angry"

        scripts = []

        print("Generating intro script...")
        # intro script
        intro_data = {
            "tone": tone,
            "inspiration": genres,

            "track_list": ",".join([track["name"] for track in tracks]),
            "duration": "6 seconds",
        }
        intro_script = get_script("intro", intro_data)
        scripts.append(intro_script)

        print("Generating Transitions...")
        # iterate over the tracks to generate the transition scripts
        for i in range(1, len(tracks)):
            track1 = tracks[i - 1]["name"]
            track2 = tracks[i]["name"]

            transition_data = {
                "tone": tone,
                "inspiration": genres,

                "previous_track": track1,
                "next_track": track2,

                "duration": "5 seconds",
            }
            transition_script = get_script("transition", transition_data)
            scripts.append(transition_script)
            print(f"Transition {i} generated")

        print("Generating outro script...")
        outro_data = {
            "tone": tone,
            "inspiration": genres,

            "track_list": ",".join([track["name"] for track in tracks]),

            "duration": "6 seconds",
        }
        outro_script = get_script("outro", outro_data)
        scripts.append(outro_script)

        ## Generate Voice Tracking Voice for each script
        speech_file_paths = []

        print("Generating Voice Tracking...")

        for script in scripts:
            speech_file_path = get_speech(script)
            speech_file_paths.append(speech_file_path)
            print(f"Speech file generated: {speech_file_path}")

        ## create order of files to assemble, by filepath
        # Order will be: music, voice tracking, music, voice tracking, ...

        # intro: speech_file_paths[0]
        # outro: speech_file_paths[len - 1]

        ordered_files = []

        # insert intro
        ordered_files.append(speech_file_paths[0])

        for i in range(len(tracks)):
            ordered_files.append(tracks[i]["path"])
            ordered_files.append(speech_file_paths[i + 1])

        # insert outro
        ordered_files.append(speech_file_paths[len(speech_file_paths) - 1])

        ## Assemble the radio

        self.output_file = "/tmp/output.mp3"

        print("Generating radio...")
        generate_radio(ordered_files, self.output_file)

        print("Radio generated: " + self.output_file)

        print("Took " + str(datetime.now() - now))

        return True

    def get_all_programs(self) -> FileResponse:
        response = FileResponse(self.output_file)
        return response

    def get_recommendations(self, genre):
        parameters = {
            "limit": 3,
            "seed_genres": genre,  ## stringify list sperated by comma
        }
        # Make the request to the Spotify API
        response = requests.get(self.spotify_url,
                                headers={"Authorization": f"Bearer {self.access_token}"},
                                params=parameters)

        recommendations = None
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the recommendations from the response
            recommendations = response.json()
            # Process the recommendations as needed
            # ...
        else:
            print("Failed to retrieve recommendations")
            return None

        tracks = []
        # get data from recommendantions
        for track in recommendations["tracks"]:
            tracks.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "url": track["external_urls"]["spotify"],
            })

        return tracks

    def download_tracks(self, tracks, output_folder):
        valid_tracks = []
        for track in tracks:
            spotify_url = track["url"]
            status = subprocess.call(["spotdl", spotify_url, "--output", f"{output_folder}" + "{title}"])

            if status == 0:
                track["path"] = f"{output_folder}{track['name']}.mp3"
                valid_tracks.append(track)

        return valid_tracks
