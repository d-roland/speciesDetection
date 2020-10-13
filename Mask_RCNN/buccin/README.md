# Fine-tune Mask-RCNN to detect Buccinidae gastropods

## Model setup and training
First step is to create a folder dedicated to the new class (here "buccin") inside the "sample" folder at the root of the Mast_RCNN repository.\
Inside this new folder, two key elements have to be created:

* a [bucccin.py](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/buccin/buccin.py) file, which is typically a copy of the original balloons.py file from the Mask_RCNN implementation, with all "balloons" mentions replaced by "buccin" ones.
* a dataset folder, which will contain two subsequent "train" and "val" folders containing the images and annotations to be used (see Data preparation below). 


## Data preparation
Citizen data come in CSV files containing image name and annotations of each specimen, but their format has to be adapted to be recognized by Mask_RCNN implementation.\
Also, some images come with multiple annotations of the same specimen (when more than one citizen annotated the image), requiring to select a single set of annotations.\
Lastly, we needed to ensure that we feed our model only with images containing annotations.

To tick the 3 requirements mentioned above, we created a script doing the whole job.

For citizen images and annotations, execute the following:
```python
python prepare_dataset_citizen.py -d folder_containing_annotations_CSV_files -i folder_containing_corresponding_images -o output_folder_to_store_dataset -m real_or_padding
```
The "-m" option can take two values: either real (we use the original bounding boxes created by the citizens) or padding (we create squared bounding boxes of 50 pixels side around the center of the original bounding box).\
The "-o" optionshould typically correspond to the "dataset" folder created above.\
Some examples of output JSON files are provided here for reference, inside the "train" and "val" folders.


## Model training
A few important parameters can be adjusted inside the [buccin.py](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/buccin/buccin.py) file, such as which parts of the network we want to train (heads only, or whole network - lines 208 to 220), the number of epoch for each (lines 212 and 219), optional data augmentation (lines 194 to 201), number of images per GPU (line 65), etc.

Once everything is in place, we can launch the training:
```python
python buccin.py train --dataset=dataset_folder --weights=coco
```

## Model evaluation
Matterport implementation of Mask_RCNN comes with handy notebooks to evaluate, or even inspect our models (and weights).

For evaluation, we very slighlty adapted the original notebook to create [evaluate-buccin.ipynb](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/buccin/evaluate-buccin.ipynb).
