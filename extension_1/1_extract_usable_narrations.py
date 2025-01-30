import os
import json


def estrai_video_uids(file_paths):
    """
    extract the videos not used in the nlq annotations

    """
    video_uids = set()
    duplicati = []
    
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "videos" in data:
                for video in data["videos"]:
                    if "video_uid" in video:
                        video_uid = video["video_uid"]
                        if video_uid in video_uids:
                            duplicati.append(video_uid)
                        else:
                            video_uids.add(video_uid)
    
    return video_uids, duplicati


def salva_chunk_per_video_uid(file_path, output_dir, exclude_uids=None):
    """
    Extracts chunks from the narration file and saves them as separate files for each video_uid.
    Optionally, removes the video_uid provided in exclude_uids.

    """
    os.makedirs(output_dir, exist_ok=True)
    

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    

    for item_id, item_data in data.items():
        if exclude_uids and item_id in exclude_uids:
            continue  
        
        output_file = os.path.join(output_dir, f"{item_id}.json")
        with open(output_file, "w", encoding="utf-8") as output_f:
            json.dump({item_id: item_data}, output_f, indent=4)
        
        print(f"Chunk per ID {item_id} saved in: {output_file}")
    
    print("All chunks saved!")


def main():

    current = os.getcwd()
    video_uid_files = [
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_test_unannotated.json"),
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_train.json"),
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_val.json"),
    ]
    

    narration_file = os.path.join(current, "datasets/ego4d_data/v1/annotations/narration.json")
    
 
    chunk_output_dir = os.path.join(current, "extension_1/chunks_output")
    
    video_uids, duplicati = estrai_video_uids(video_uid_files)
    print(f"univoque UID extracted: {len(video_uids)}")
    if duplicati:
        print(f"Dups found ({len(set(duplicati))}): {set(duplicati)}")
    else:
        print("No dup found.")

    combined_output_file = os.path.join(current, "extension_1/combined_nlq_video_uids.json")
    with open(combined_output_file, "w", encoding="utf-8") as f:
        json.dump(list(video_uids), f, indent=4)
    print(f"univoque videos saved in: {combined_output_file}")

    print("chunk extraction...")
    salva_chunk_per_video_uid(narration_file, chunk_output_dir, exclude_uids=video_uids)


if __name__ == "__main__":
    main()
