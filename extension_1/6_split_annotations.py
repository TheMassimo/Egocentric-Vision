import json
import random
import os
def split_videos(input_file, train_file, val_file, test_file, train_ratio, val_ratio, test_ratio):
    # Controlla che i rapporti siano validi
    assert train_ratio + val_ratio + test_ratio == 1, "La somma dei rapporti deve essere uguale a 1."

    # Leggi il file JSON di input
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Estrai la lista dei video
    videos = data.get('videos', [])
    total_videos = len(videos)

    # Mescola i video casualmente
    random.shuffle(videos)

    # Calcola il numero di video per ciascuno split
    train_count = int(total_videos * train_ratio)
    val_count = int(total_videos * val_ratio)
    test_count = total_videos - train_count - val_count  # Resto per il test

    # Assegna i video agli split
    train_videos = videos[:train_count]
    val_videos = videos[train_count:train_count + val_count]
    test_videos = videos[train_count + val_count:]

    # Aggiungi la voce "split" a ciascun video
    for video in train_videos:
        video['split'] = 'train'
    for video in val_videos:
        video['split'] = 'val'
    for video in test_videos:
        video['split'] = 'test'

    # Salva ogni split in un file separato
    with open(train_file, 'w') as f:
        json.dump({"videos": train_videos}, f, indent=4)
    with open(val_file, 'w') as f:
        json.dump({"videos": val_videos}, f, indent=4)
    with open(test_file, 'w') as f:
        json.dump({"videos": test_videos}, f, indent=4)

    print(f"File JSON suddivisi in train ({train_count}), val ({val_count}) e test ({test_count}).")

# Configura i parametri
current = os.getcwd()

# File di input e di output
data_input_file = os.path.join(current, "extension_1/llm/nlq_like_annotations.json")
train_output_file = os.path.join(current, "extension_1/llm/train_nlq_like_annotations.json")  # File JSON di output finale
val_output_file = os.path.join(current, "extension_1/llm/val_nlq_like_annotations.json")  # File JSON di output finale
test_output_file = os.path.join(current, "extension_1/llm/test_nlq_like_annotations.json")  # File JSON di output finale
train_ratio = 0.6  # Proporzione di video per il train
val_ratio = 0.20  # Proporzione di video per il val
test_ratio = 0.20  # Proporzione di video per il test

# Esegui lo script
split_videos(data_input_file, train_output_file, val_output_file, test_output_file, train_ratio, val_ratio, test_ratio)