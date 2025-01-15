import json
import os

current = os.getcwd()
filePath = os.path.join(current, "datasets/ego4d_data/ego4d.json")
# Leggi il file JSON

with open(filePath, "r") as file:
    data = json.load(file)

# Estrai tutti i video_uid
video_uids = [video["video_uid"] for video in data["videos"]]

# Conta gli elementi unici
unique_video_uids = set(video_uids)

# Stampa il numero di video_uid univoci
print(f"Numero di video_uid univoci: {len(unique_video_uids)}")
