import os, csv, json, collections, random, shutil
from argparse import ArgumentParser
from PIL import Image
import pandas as pd

parser = ArgumentParser()
parser.add_argument('-d', '--data_dir', default="/home/jupyter/object-detection/Mask_RCNN/samples/crabe/dataset/Crabes_annotations/2014-2015/Thomas\ Day", type=str,help='directory containing annotation file')
parser.add_argument('-i', '--image_dir', default="/home/jupyter/object-detection/Mask_RCNN/samples/crabe/dataset/momar_2014-2015", type=str,help='directory containing images')
parser.add_argument('-o', '--output_dir', default="/home/jupyter/object-detection/Mask_RCNN/samples/crabe/dataset/", type=str,help='output directory to store the dataset')
args = parser.parse_args()

input_dir = os.path.normpath(args.data_dir) if args.data_dir else os.getcwd()
print('Working in {}'.format(input_dir))
image_dir = os.path.normpath(args.image_dir) if args.image_dir else os.getcwd()
output_dir = os.path.normpath(args.output_dir) if args.output_dir else os.getcwd()

print("Creating boxes as squares around the center of expert annotations")

#First iteration over files to convert txt to csv
for file in os.listdir(input_dir):
    f = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    if extension == '.txt':
        read_file = pd.read_csv(os.path.join(input_dir, f + '.txt'), sep="\t")
        read_file.to_csv(os.path.join(input_dir, f + '.csv'), index=None)
        print('Converted {} from txt to csv'.format(file))

#Second iteration to extract relevant data from all csv files
imgs_list = []
data = collections.defaultdict(dict)
for file in os.listdir(input_dir):
    f = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    if extension == '.csv':    
        with open(os.path.join(input_dir, file), encoding='latin-1', errors = 'ignore') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                full_label = row['Label']
                label = full_label.split(":")
                imgs_list.append(str(label[1]) + '.jpg')
                img_filename = str(label[1]) + '.jpg'
                img_full_path = os.path.join(image_dir,str(label[1]) + '.jpg')
                
                #keeping only examples for which we have both annotation and image
                try:
                    img_size = os.path.getsize(img_full_path)
                except:
                    continue
                label_size = img_filename + str(img_size)
                
                #filling the first 2 fields of JSON format: filename and size
                data[label_size]['filename'] = img_filename
                data[label_size]['size'] = img_size
                
                #recreating the polygons as squares around central X-Y coordinates
                try:
                    im = Image.open(img_full_path)
                    im_width, im_height = im.size
                except:
                    im_width = 0
                    im_height = 0
                PADDING = 25
                x_corner_up_left = max(0,round(float(row['X'])-PADDING))
                x_corner_down_left = max(0,round(float(row['X'])-PADDING))
                x_corner_down_right = min(round(float(row['X'])+PADDING),im_width)
                x_corner_up_right = min(round(float(row['X'])+PADDING),im_width)
                all_points_x = [x_corner_up_left,x_corner_down_left,x_corner_down_right,x_corner_up_right]
                y_corner_up_left = max(round(float(row['Y'])-PADDING),0)
                y_corner_down_left = min(round(float(row['Y'])+PADDING),im_height)
                y_corner_down_right = min(round(float(row['Y'])+PADDING),im_height)
                y_corner_up_right = max(round(float(row['Y'])-PADDING),0)
                all_points_y = [y_corner_up_left,y_corner_down_left,y_corner_down_right,y_corner_up_right]
                
                #filling the 2 last requested fields of JSON format: regions and file_attributes
                new_region = {"shape_attributes":{"name":"polygon","all_points_x":all_points_x,"all_points_y":all_points_y},"region_attributes":{"type":"crabe"}}
                if 'regions' not in data[label_size]:
                    data[label_size]['regions'] = collections.defaultdict()
                    data[label_size]['regions'][0] = new_region
                else:
                    new_key = len(data[label_size]['regions'])
                    data[label_size]['regions'][new_key] = new_region
                data[label_size]["file_attributes"] = {}
        print('Processed {}'.format(file))

        
# Split data into train & val subdictionaries before dumping into JSON format
num_train = int(len(data.keys())*4/5)
train_data = dict(random.sample(data.items(), num_train))
print("Number of training examples: {}".format(int(len(train_data.keys()))))
val_data = {k:v for k,v in data.items() if k not in train_data.keys()}
print("Number of validation examples: {}".format(int(len(val_data.keys()))))


with open(os.path.join(input_dir, "annotations_json.json"), "w") as json_file:
    json.dump(data, json_file, indent=2)
    
with open(os.path.join(input_dir, "train_annotations.json"), "w") as json_file:
    json.dump(train_data, json_file, indent=2)

with open(os.path.join(input_dir, "val_annotations.json"), "w") as json_file:
    json.dump(val_data, json_file, indent=2)

    
# Extract image filenames for both train and val annotated examples and copy corresponding images into new folders
print('Creating training folder')
train_images_list = []
for k,v in train_data.items():
    train_images_list.append(train_data[k]['filename'])

train_folder = os.path.join(output_dir,'train')
if os.path.exists(train_folder):
    shutil.rmtree(train_folder)
os.makedirs(train_folder)

shutil.copy(os.path.join(input_dir, "train_annotations.json"), os.path.join(train_folder, "via_region_data.json"))

for f in train_images_list:
    try:
        shutil.copy(os.path.join(image_dir,f), train_folder)
    except:
        print("Couldn't find image: {}".format(f))
        
print('Creating validation folder')
val_images_list = []
for k,v in val_data.items():
    val_images_list.append(val_data[k]['filename'])

val_folder = os.path.join(output_dir,'val')
if os.path.exists(val_folder):
    shutil.rmtree(val_folder)
os.makedirs(val_folder)

shutil.copy(os.path.join(input_dir, "val_annotations.json"), os.path.join(val_folder, "via_region_data.json"))

for f in val_images_list:
    try:
        shutil.copy(os.path.join(image_dir,f), val_folder)
    except:
        print("Couldn't find image: {}".format(f))