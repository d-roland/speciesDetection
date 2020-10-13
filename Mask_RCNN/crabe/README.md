# Fine-tune Mask-RCNN to detect Segonzacia mesatlantica crabs

## Model setup and training
First step is to create a folder dedicated to the new class (here "crabe") inside the "sample" folder at the root of the Mast_RCNN repository.\
Inside this new folder, three key elements have to be 


## Data preparation
...


## Model training
A few important parameters can be adjusted inside the [crabe.py](https://github.com/d-roland/speciesDetection/blob/main/Mask_RCNN/crabe/crabe.py) file, such as which parts of the network we want to train (heads only, or whole network - lines 208 to 220), the number of epoch for each (lines 212 and 219), optional data augmentation (lines 194 to 201), number of images per GPU (line 65), etc.

Once everything is in place, we can launch the training:
```python
python crabe.py train --dataset=dataset_folder --weights=coco
```

## Model evaluation
...
