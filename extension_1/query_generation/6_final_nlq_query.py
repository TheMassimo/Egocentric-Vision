import json
import os

def accorpa_queries(input_data, N):
    """
    Accorpa i language_queries in gruppi di N e aggiorna i valori minimi e massimi rilevanti.

    Args:
        input_data (dict): Dati JSON caricati.
        N (int): Dimensione del gruppo per accorpamento.

    Returns:
        dict: Dati JSON modificati.
    """
    for video in input_data.get("videos", []):
        for clip in video.get("clips", []):
            for annotation in clip.get("annotations", []):
                language_queries = annotation.get("language_queries", [])

                # Accorpa i language_queries in gruppi di N
                grouped_queries = []
                for i in range(0, len(language_queries), N):
                    group = language_queries[i:i + N]

                    # Calcola i valori minimi e massimi
                    new_clip_start_sec = min(query["clip_start_sec"] for query in group)
                    new_clip_end_sec = max(query["clip_end_sec"] for query in group)
                    new_video_start_sec = min(query["video_start_sec"] for query in group)
                    new_video_end_sec = max(query["video_end_sec"] for query in group)
                    new_video_start_frame = min(query["video_start_frame"] for query in group)
                    new_video_end_frame = max(query["video_end_frame"] for query in group)

                    merged_query = {
                        "clip_start_sec": new_clip_start_sec,
                        "clip_end_sec": new_clip_end_sec,
                        "video_start_sec": new_video_start_sec,
                        "video_end_sec": new_video_end_sec,
                        "video_start_frame": new_video_start_frame,
                        "video_end_frame": new_video_end_frame,
                        "template": "Query generated from narration",
                        "query": " | ".join(q["query"] for q in group),
                        "slot_x": "",
                        "verb_x": "",
                        "raw_tags": [tag for q in group for tag in q["raw_tags"]]
                    }
                    grouped_queries.append(merged_query)

                annotation["language_queries"] = grouped_queries

    return input_data

def aggiorna_clips(input_data):
    """
    Aggiorna i valori delle clips basandosi sui language_queries accorpati.

    """
    for video in input_data.get("videos", []):
        for clip in video.get("clips", []):
            all_queries = [query for annotation in clip.get("annotations", []) for query in annotation.get("language_queries", [])]

            if all_queries:
                clip["video_start_sec"] = min(query["video_start_sec"] for query in all_queries)
                clip["video_end_sec"] = max(query["video_end_sec"] for query in all_queries)
                clip["video_start_frame"] = min(query["video_start_frame"] for query in all_queries)
                clip["video_end_frame"] = max(query["video_end_frame"] for query in all_queries)
                clip["clip_start_sec"] = min(query["clip_start_sec"] for query in all_queries)
                clip["clip_end_sec"] = max(query["clip_end_sec"] for query in all_queries)
                clip["clip_start_frame"] = min(query["video_start_frame"] for query in all_queries)
                clip["clip_end_frame"] = max(query["video_end_frame"] for query in all_queries)

    return input_data

def combina_con_chunks(input_data, chunks_data):

    for video in input_data.get("videos", []):
        video_uid = video.get("video_uid")
        if video_uid in chunks_data:
            chunks = chunks_data[video_uid]
            chunk_index = 0

            for clip in video.get("clips", []):
                for annotation in clip.get("annotations", []):
                    for query in annotation.get("language_queries", []):
                        if chunk_index < len(chunks):
                            query["query"] = chunks[chunk_index]
                            chunk_index += 1

    return input_data

input_file_nlq = "nlq_like_annotations_50.json"
input_file_chunks = os.path.join("all_in_one_narrations", "merged_chunks.json")
output_file = "FINAL.json"

with open(input_file_nlq, "r") as f:
    data = json.load(f)

with open(input_file_chunks, "r") as f:
    chunks_data = json.load(f)


first_id = next(iter(chunks_data))  
length_of_elements = len(chunks_data[first_id]) 
N = int(50/length_of_elements) 

print("N ====> ",N)


merged_data = accorpa_queries(data, N)
updated_data = aggiorna_clips(merged_data)
combined_data = combina_con_chunks(updated_data, chunks_data)

with open(output_file, "w") as f:
    json.dump(merged_data, f, indent=4)

print(f"File processato e salvato in {output_file}")
