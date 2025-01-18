import json
from datetime import datetime
import os

# Ottieni il percorso corrente
current = os.getcwd()

# File di input e di output
input_file = os.path.join(current, "extension_1/llm/combined_10_questions.json")
final_output_file = os.path.join(current, "extension_1/llm/nlq_like_annotations.json")  # File JSON di output finale

# Struttura di base per il file finale
final_data = {
    "version": "1",
    "date": datetime.now().strftime("%y%m%d"),
    "description": "NLQ Annotations (val)",
    "manifest": "s3://ego4d-consortium-sharing/public/v1/full_scale/manifest.csv",
    "videos": []
}

MEAN_DURATION = 4.8 * 2  # Durata media di un evento
i=0
# Funzione per convertire i dati
with open(input_file, "r") as infile:
    input_data = json.load(infile)

    for video_id, video_data in input_data.items():
        video_entry = {
            "video_uid": video_id,
            "clips": []
        }

        # Estrai clip e annotazioni
        narration_pass = video_data.get("narration_pass_1", {})
        narrations = narration_pass.get("narrations", [])

        if not narrations:
            continue  # Salta se non ci sono narrations

        # Determina il video start e end sec dai timestamps delle narrations
        video_start_sec = narrations[0].get("timestamp_sec", 0)  # Primo timestamp
        video_end_sec = narrations[-1].get("timestamp_sec", 0) + MEAN_DURATION  # Ultimo timestamp + durata media
        video_start_frame = narrations[0].get("timestamp_frame", 0)  # Primo timestamp
        video_end_frame = narrations[-1].get("timestamp_frame", 0) + (MEAN_DURATION*30)  # Ultimo timestamp + durata media
        clip_entry = {
            "clip_uid": i,
            "video_start_sec": video_start_sec,
            "video_end_sec": video_end_sec,
            "video_start_frame": video_start_frame,
            "video_end_frame": video_end_frame,
            "clip_start_sec": video_start_sec,
            "clip_end_sec": video_end_sec,
            "clip_start_frame": video_start_frame,
            "clip_end_frame": video_end_frame,  # Supponendo 30 fps
            "annotations": []
        }
        i+=1
        # Aggiungi ogni narration come annotation nel clip
        # Raggruppa narrations per annotation_uid
        annotations_grouped = {}

        for narration in narrations:
            annotation_uid = narration.get("annotation_uid")
            if annotation_uid not in annotations_grouped:
                annotations_grouped[annotation_uid] = {
                    "language_queries": [],
                    "annotation_uid": annotation_uid
                }

            # Aggiungi la query alla lista
            annotations_grouped[annotation_uid]["language_queries"].append({
                "clip_start_sec": narration.get("timestamp_sec", 0),
                "clip_end_sec": narration.get("timestamp_sec", 0) + MEAN_DURATION,
                "video_start_sec": narration.get("timestamp_sec", 0),
                "video_end_sec": narration.get("timestamp_sec", 0) + MEAN_DURATION,
                "video_start_frame": narration.get("timestamp_frame", 0),
                "video_end_frame": narration.get("timestamp_frame", 0) + (MEAN_DURATION * 30),
                "template": "Query generated from narration",
                "query": narration.get("Query", ""),
                "slot_x": "",
                "verb_x": "",
                "raw_tags": [
                    narration.get("Query", "")
                ]
            })

        clip_entry["annotations"] = list(annotations_grouped.values())
        video_entry["clips"].append(clip_entry)
        final_data["videos"].append(video_entry)

# Scriviamo il file finale
with open(final_output_file, "w") as outfile:
    json.dump(final_data, outfile, indent=4)

print(f"File generato con successo: {final_output_file}")
