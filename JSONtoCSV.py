import csv
import json
import os, random, shutil
import progressbar


targets = [
    "call",
    "dislike",
    "fist",
    "four",
    "like",
    "mute",
    "ok",
    "one",
    "palm",
    "peace",
    "rock",
    "stop",
    "stop_inverted",
    "three",
    "two_up",
    "two_up_inverted",
    "three2",
    "peace_inverted",
    "no_gesture"
]
def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

ANNOTATION_PATH = "./dataset/sub/ann_subsample/"
DATASET_PATH = "./dataset/sub/"
PREPARED_DATASET_PATH = "./dataset/sub/prepared_dataset/"

count = 0
for gesture in targets:
    if gesture == "no_gesture":
        continue
    print("Processing gesture: " + gesture)
    total = []
    with open(f"{ANNOTATION_PATH}{gesture}.json", "r") as f:
        data = json.load(f)
        for key, value in data.items():
            file = find_file(DATASET_PATH + '/' + gesture, key + ".jpg")
            if file is None:
                print("File not found: " + gesture)
                continue
    #         # print(key, value)
            arr_labels = []
            arr_bboxes = []
            for labels in value['labels']:
                arr_labels.append(labels)
            for bboxes in value['bboxes']:
                arr_bboxes.append(bboxes) 

            for i in range(len(arr_labels)):
                if arr_labels[i] in targets:
                    xmin = arr_bboxes[i][0]
                    ymin = arr_bboxes[i][1]
                    xmax = arr_bboxes[i][2]
                    ymax = arr_bboxes[i][3]
                    total.append(['TRAIN', key+'.jpg', arr_labels[i], xmin, ymin, xmax, ymax, file])
        random.shuffle(total)
        widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]
        bar = progressbar.ProgressBar(max_value=len(total), 
                              widgets=widgets).start()
        count += len(total)
        coppied = []
        for i in range(len(total)):
            bar.update(i)
            filepath = 'train/' + total[i][1]
            if i < int(len(total) * 0.8):
                if(total[i][1] not in coppied):
                    shutil.copy(f'{total[i][7]}', PREPARED_DATASET_PATH+'train')
                    coppied.append(total[i][1])
            else:
                if(total[i][1] not in coppied):
                    shutil.copy(f'{total[i][7]}', PREPARED_DATASET_PATH+'test')
                    coppied.append(total[i][1])
                total[i][0] = 'TEST'
                filepath = 'test/' + total[i][1]
            with open(f"{PREPARED_DATASET_PATH}ann.csv", "a") as f:
                        writer = csv.writer(f)
                        writer.writerow([total[i][0], filepath, total[i][2], total[i][3], total[i][4], total[i][5], total[i][6]])
                        f.close()
                    

# find a specific file in a directory

