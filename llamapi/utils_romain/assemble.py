import os
import ffmpeg
import json

data = []

with open("random-secret-game.json", 'r') as f:
    data = json.load(f)

# Dossier contenant les vidéos de jeu
video_folder = "secret-game-data/"

# Liste des noms de fichiers vidéo de jeu
#video_files = sorted([f for f in os.listdir(video_folder) if f.endswith(".mp4")])

# Durée du décompte et de la musique
guess_duration = 14
music_duration = 7

# Création de la liste des vidéos de jeu concaténées
segments = []

def formatName(fileName):
    # remove extension and replace _ by space
    return fileName.split(".")[0].replace("_", " ")

input_count_video = (
    ffmpeg.input("countdown_final.mp4")
    .video
)

for video in data:
    video_path = os.path.join(video_folder, video["filename"])
    name = video["title"] + " - " + video["name"]
    #name = formatName(video_file)


    input_asset_video = (
        ffmpeg.input(video_path, t=music_duration, r=25)
        .video
        .filter("scale", size='hd1080', force_original_aspect_ratio="increase")
        .filter("setsar", 1)
    )

    input_asset_video = ffmpeg.drawtext(input_asset_video, text=name, x=50, y=50, fontsize=48, fontcolor="white", box=1, boxcolor="black@0.5", boxborderw=5, fontfile="Minecraft.ttf")

    input_audio = ffmpeg.input(video_path, ss=0, t=guess_duration + music_duration).audio
    input_video = ffmpeg.concat(input_count_video, input_asset_video, n=2, v=1, unsafe=1)

    segments.append(input_video)
    segments.append(input_audio)


ffmpeg.concat(*segments, v=1, a=1).output("output.mp4").run(overwrite_output=True)