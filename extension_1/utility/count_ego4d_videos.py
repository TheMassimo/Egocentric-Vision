import json
import os

current = os.getcwd()
filePath = os.path.join(current, "datasets/ego4d_data/v1/annotations/nlq_test_unannotated.json")


with open(filePath, "r") as file:
    data = json.load(file)

video_uids = [video["video_uid"] for video in data["videos"]]

unique_video_uids = set(video_uids)

print(f"Numero di video_uid univoci: {len(unique_video_uids)}")
