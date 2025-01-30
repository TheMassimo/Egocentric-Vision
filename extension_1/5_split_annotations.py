import json
import random
import os

def split_videos(input_file, train_file, val_file, test_file, train_ratio, val_ratio, test_ratio):

    assert abs(train_ratio + val_ratio + test_ratio - 1) < 1e-6, "the sum of the ratios needs to be 1"

    with open(input_file, 'r') as f:
        data = json.load(f)

    videos = data.get('videos', [])
    total_videos = len(videos)

    if total_videos < 4:
        raise ValueError("There are not enough videos to subdivide the dataset")


    subset_size = total_videos // 1
    videos = videos[:subset_size]
    random.shuffle(videos)


    train_count = int(len(videos) * train_ratio)
    val_count = int(len(videos) * val_ratio)
    test_count = len(videos) - train_count - val_count 


    train_videos = videos[:train_count]
    val_videos = videos[train_count:train_count + val_count]
    test_videos = videos[train_count + val_count:]

    for video in train_videos:
        video['split'] = 'train'
    for video in val_videos:
        video['split'] = 'val'
    for video in test_videos:
        video['split'] = 'test'

    with open(train_file, 'w') as f:
        json.dump({"videos": train_videos}, f, indent=4)
    with open(val_file, 'w') as f:
        json.dump({"videos": val_videos}, f, indent=4)
    with open(test_file, 'w') as f:
        json.dump({"videos": test_videos}, f, indent=4)

    print(f"dataset subdivided in train ({len(train_videos)}), val ({len(val_videos)}) e test ({len(test_videos)}).")

current = os.getcwd()


data_input_file = os.path.join(current, "extension_1/llm/FINAL_5.json")
train_output_file = os.path.join(current, "extension_1/llm/train_nlq_like_annotations.json")  
val_output_file = os.path.join(current, "extension_1/llm/val_nlq_like_annotations.json")  
test_output_file = os.path.join(current, "extension_1/llm/test_nlq_like_annotations.json")

train_ratio = 0.6  
val_ratio = 0.2    
test_ratio = 0.2  

split_videos(data_input_file, train_output_file, val_output_file, test_output_file, train_ratio, val_ratio, test_ratio)
