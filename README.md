# Deep-sea Species Detection

## Context and challenge
...
* Crab Segonzacia mesatlantica from the Lucky Strike vent field (Mid-Atlantic Ridge, 1700m below sea level). Below is a sample image with 3 expert annotations illustrated by squared bounding boxes:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_expert_annotations.png)
* Buccinidae gastropods from the Grotto hydrothermal edifice (Main Endeavour Field, Juan de Fuca Ridge, 2200m below sea level). Below is a samplke image with 11 citizen annotations:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_citizen_annotations.png)


## Approach
In order to perform object detection on custom specimens, we used [Matterport implementation of Mask-RCNN](https://github.com/matterport/Mask_RCNN). The base model is pretrained on Coco dataset, able to recognize 80 basic shapes. We fine-tuned it to detect our specific specimens.

As per the **metrics**, given we focused solely on object detection (approximate localization on images), we decided to focus on:
* **mAP** (mean Average Precision: mean proportion of our predictions that are correct): a strong mAP would imply less false positive, but may also imply that we miss some specimens.
* **Recall** (how good we find all the positives, eg all the annotated specimens). A strong Recall is interesting if we want to find the most specimens, at all cost (eg with false positives also).

It's worth noting that, in the case of object detection, these two metrics are computed for a certain threshold of **IoU** (Intersection over Union). The IoU represents the match between the predicted bounding box and the annotated one. Given the high variability of bounding box size and form between expert and citizen annotations, we decided to use two thresholds for the IoU: 0.5 (standard value) and 0.01 (high tolerance).

## Key results
...

## Next steps
* test [Yolov4](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects) for object detection (alternative model to Mask-RCNN)
* test [Rolo](https://github.com/Guanghan/ROLO) for object tracking

## Acknowledgments
A huge thank you to [Marjolaine Matabos](https://annuaire.ifremer.fr/cv/20350/en/), Benthic ecologist at the Laboratoire Environnement Profond (PDG-REM-EEP-LEP), for very spontaneously sharing annotated examples of various species, as well as research papers providing more context on the project.
