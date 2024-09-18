from datetime import datetime
from src.recommendations import get_recommendations
from src.assemble import assemble_radio
from src.downloader import download_tracks
from src.narrator import get_script, get_speech


start_from_step = 0

def generate_radio():
    now = datetime.now()
    ## Get Recommendations

    genres = "pop,rock"
    tracks = []
    if start_from_step <= 0:
        print("Getting Recommendations...")
        tracks = get_recommendations(genres)
        if tracks is None:
            print("No recommendations found")
            exit(1)

        print("Recommendations:")
        print(tracks)

    ## Downloads the musics from the recommendations

    output_folder = "assets/music/"

    if start_from_step <= 1:
        print("Downloading tracks...")
        tracks = download_tracks(tracks, output_folder)

        print("Tracks downloaded:")
        print(tracks)

    ## Get the metadata of the musics

    ## Generate Voice Tracking text

    tone = "happy"

    scripts = []

    if start_from_step <= 2:
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
            track1 = tracks[i-1]["name"]
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

    speech_output_folder = "assets/speech/"

    if start_from_step <= 3:
        print("Generating Voice Tracking...")
        
        for script in scripts:
            speech_file_path = get_speech(script, speech_output_folder)
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

    output_file = "assets/outout/output.mp3"

    print("Generating radio...")
    generate_radio(ordered_files, output_file)

    print("Radio generated: " + output_file)

    print("Took " + str(datetime.now() - now))
    
    return output_file