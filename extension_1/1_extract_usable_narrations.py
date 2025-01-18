import os
import json


def estrai_video_uids(file_paths):
    """
    Estrae i video_uid unici da una lista di file JSON.
    
    :param file_paths: Lista di percorsi ai file JSON.
    :return: Insieme di video_uid unici e lista dei duplicati.
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
    Estrae i chunk da un file JSON e li salva come file separati per ciascun video_uid.
    Opzionalmente rimuove i video_uid forniti da `exclude_uids`.
    
    :param file_path: Percorso del file JSON con i dati.
    :param output_dir: Directory di output per i chunk.
    :param exclude_uids: Insieme opzionale di video_uid da escludere.
    :return: Nessuno.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Carica i dati dal file JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Itera sugli ID e salva i chunk
    for item_id, item_data in data.items():
        if exclude_uids and item_id in exclude_uids:
            continue  # Salta gli ID da escludere
        
        output_file = os.path.join(output_dir, f"{item_id}.json")
        with open(output_file, "w", encoding="utf-8") as output_f:
            json.dump({item_id: item_data}, output_f, indent=4)
        
        print(f"Chunk per ID {item_id} salvato in: {output_file}")
    
    print("Processo completato. Tutti i chunk sono stati salvati.")


def main():
    # Percorsi dei file per estrarre i video_uid
    current = os.getcwd()
    video_uid_files = [
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_test_unannotated.json"),
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_train.json"),
        os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_val.json"),
    ]
    
    # Percorso del file narrations.json
    narration_file = os.path.join(current, "datasets/ego4d_data/v1/annotations/narration.json")
    
    # Directory di output per i chunk
    chunk_output_dir = os.path.join(current, "extension_1/chunks_output")
    
    # Estrarre i video_uid
    video_uids, duplicati = estrai_video_uids(video_uid_files)
    print(f"Video UID estratti: {len(video_uids)} unici")
    if duplicati:
        print(f"Duplicati trovati ({len(set(duplicati))} unici): {set(duplicati)}")
    else:
        print("Nessun duplicato trovato.")
    
    # Salva i video_uid estratti in un file
    combined_output_file = os.path.join(current, "extension_1/combined_nlq_video_uids.json")
    with open(combined_output_file, "w", encoding="utf-8") as f:
        json.dump(list(video_uids), f, indent=4)
    print(f"Valori unici di video_uid salvati in: {combined_output_file}")
    
    # Estrarre e salvare i chunk, escludendo i video_uid estratti in precedenza
    print("Inizio estrazione dei chunk...")
    salva_chunk_per_video_uid(narration_file, chunk_output_dir, exclude_uids=video_uids)


if __name__ == "__main__":
    main()
