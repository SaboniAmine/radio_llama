import os
import ffmpeg
import json

fade_duration = 1


def formatName(fileName):
    # remove extension and replace _ by space
    return fileName.split(".")[0].replace("_", " ")


def generate_radio(ordered_files, output_file):
    # Création de la liste des vidéos de jeu concaténées
    segments = []

    for idx, file_path in enumerate(ordered_files):
        if idx % 2 == 0:
            # here we have animator
            input_asset_audio = (
                ffmpeg.input(file_path)
                .audio
            )
        else:
            # here we have music
            input_asset_audio = (
                ffmpeg.input(file_path, t=10)
                .audio
            )
            # input_asset_audio.fade_out(fade_duration)
            # input_asset_audio.fade_out(fade_duration)

        # input_voice_tracking = (
        #     ffmpeg.input("voice-tracking.wav")
        #     .audio
        # )

        segments.append(input_asset_audio)
        # segments.append(input_voice_tracking)

    ffmpeg.concat(*segments, v=0, a=1).output(output_file).run(overwrite_output=True)

