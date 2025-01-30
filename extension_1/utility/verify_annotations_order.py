import json
import os
def verifica_start_end(json_path):

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    errori = []


    for video_idx, video in enumerate(data.get("videos", [])):
        for clip_idx, clip in enumerate(video.get("clips", [])):
            if clip.get("clip_start_sec", 0) >= clip.get("clip_end_sec", 0):
                errori.append({
                    "video_index": video_idx,
                    "clip_index": clip_idx,
                    "clip_start_sec": clip.get("clip_start_sec"),
                    "clip_end_sec": clip.get("clip_end_sec")
                })

            for annotation_idx, annotation in enumerate(clip.get("annotations", [])):
                for query_idx, query in enumerate(annotation.get("language_queries", [])):
                    if query.get("clip_start_sec", 0) >= query.get("clip_end_sec", 0):
                        errori.append({
                            "video_index": video_idx,
                            "clip_index": clip_idx,
                            "annotation_index": annotation_idx,
                            "query_index": query_idx,
                            "clip_start_sec": query.get("clip_start_sec"),
                            "clip_end_sec": query.get("clip_end_sec")
                        })

    if errori:
        print("Sono stati trovati errori:")
        for errore in errori:
            print(errore)
    else:
        print("Tutti i clip e le annotazioni hanno start_sec < end_sec.")

current = os.getcwd()

input_file = os.path.join(current, "extension_1/llm/nlq_like_annotations.json")

verifica_start_end(input_file)
