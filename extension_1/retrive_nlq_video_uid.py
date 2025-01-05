import os
import json

# Percorsi dei file JSON
current = os.getcwd()
file_paths = [
    os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_test_unannotated.json"),
    os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_train.json"),
    os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_val.json"),
]

# File di output
output_file = os.path.join(current, "extension_1/combined_nlq_video_uids.json")

# Insieme per raccogliere tutti i video_uid (evita duplicati)
video_uids = set()
duplicati = []  # Lista per i duplicati

# Itera sui file JSON
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Accedi alla lista "videos"
        if "videos" in data:
            for video in data["videos"]:
                if "video_uid" in video:
                    video_uid = video["video_uid"]
                    if video_uid in video_uids:
                        # Aggiungi ai duplicati se già presente
                        duplicati.append(video_uid)
                    else:
                        video_uids.add(video_uid)

# Scrive i risultati in un unico file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(list(video_uids), f, indent=4)

print(f"Valori unici di video_uid salvati in: {output_file}")

# Controlla e stampa i duplicati
if duplicati:
    print(f"Duplicati trovati ({len(set(duplicati))} unici):")
    print(set(duplicati))
else:
    print("Nessun duplicato trovato.")
