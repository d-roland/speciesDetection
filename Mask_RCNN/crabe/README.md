# Fine-tune Mask-RCNN to detect Segonzacia mesatlantica crabs

## Model setup and training
First step is to create a folder dedicated to the new class (here "crabe") inside the "sample" folder at the root of the Mast_RCNN repository.\
Inside this new folder, three key elements have to be 


## Data preparation
Expert and citizen data come both in CSV files containing image name and annotations of each specimen, but their respective formats differ.\
Also, some images come with multiple annotations of the same specimen (when more than one citizen annotated the image), requiring to select a single set of annotations.\
Lastly, we needed to ensure that we feed our model only with images containing annotations.\

To easily convert the input files into JSON formats recognized by Mask_RCNN implementation, and tick the last 2 requirements mentioned above, we created some scripts doing the whole job.

For expert images and annotations, execute the following:
```python
python prepare_dataset_expert.py -d folder_containing_annotations_CSV_files -i folder_containing_corresponding_images -o output_folder_to_store_dataset
```

For citizen images and annotations, execute the following:
```python
python prepare_dataset_citizen.py -d folder_containing_annotations_CSV_files -i folder_containing_corresponding_images -o output_folder_to_store_dataset -m real
```
The "-m" option for the citizen script can take two values: either real (we use the original bounding boxes created by the citizens) or padding (we create squared bounding boxes of 50 pixels side around the center of the original bounding box).


## Model training
A few important parameters can be adjusted inside the [crabe.py](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/crabe/crabe.py) file, such as which parts of the network we want to train (heads only, or whole network - lines 208 to 220), the number of epoch for each (lines 212 and 219), optional data augmentation (lines 194 to 201), number of images per GPU (line 65), etc.

Once everything is in place, we can launch the training:
```python
python crabe.py train --dataset=dataset_folder --weights=coco
```

## Model evaluation
Matterport implementation of Mask_RCNN comes with handy notebooks to evaluate, or even inspect our models (and weights).

For evaluation, we very slighlty adapted the original notebook to create [evaluate-crabe.ipynb](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/crabe/evaluate-crabe.ipynb).
