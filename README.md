# Deep-sea Species Detection

## Context and challenge
In order to study long-term temporal dynamics of vent communities, the Laboratoire Environnement Profond (Ifremer) leverages multidisciplinary seafloor observatories deployed in several target sites. The corresponding modules are equipped with cameras, programmed to record 20-min video sequences six times a day (02.00, 06.00, 10.00, 14.00, 18.00 and 22.00 UTC) with different zoom levels per sequence. Video sequences are later analyzed by experts to localize the species, and notably:
* Crab Segonzacia mesatlantica from the Lucky Strike vent field (Mid-Atlantic Ridge, 1700m below sea level). Below is a sample image with 3 expert annotations illustrated by squared bounding boxes:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_expert_annotations.png)
* Buccinidae gastropods from the Grotto hydrothermal edifice (Main Endeavour Field, Juan de Fuca Ridge, 2200m below sea level). Below is a samplke image with 11 citizen annotations:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_citizen_annotations.png)

These videos are a crucial source of information for assessing natural variability and ecosystem responses to increasing human activity in the deep sea. But manually reviewing and annotating video sequences is a tedious and time-consuming process for experts, particularly as the quantity of recorded data dramatically increased over the past years.\
Recently, some researchers developped [crowdsourcing initiatives](https://www.deepseaspy.com/) in order to leverage untrained volunteers and scale the annotation process. But the quality of these annotations has to be compared to expert ones.\
Given recent progress of Machine Learning algorithms, notably on object detection tasks, we decided to test some recent models on both expert and citizen annotations. 

## Approach
In order to perform object detection on custom specimens, we used [Matterport implementation of Mask-RCNN](https://github.com/matterport/Mask_RCNN). The base model is pretrained on Coco dataset, and able to recognize 80 basic shapes. We fine-tuned it to detect our specific specimens.

Some data preparation was required, as expert and citizen annotations come in different format. In order to get comparable data, we decided to recreate the bounding box of each annotation as a 50 pixels square around the center of each manual annotation. Also, we needed to ensure that we used only images with annotations in order to train the model.

As per the **metrics**, given we focused solely on object detection (approximate localization on images), we decided to focus on:
* **mAP** (mean Average Precision: mean proportion of our predictions that are correct): a strong mAP would imply less false positive, but may also imply that we miss some specimens.
* **Recall** (how good we find all the positives, eg all the annotated specimens). A strong Recall is interesting if we want to find the most specimens, at all cost (eg with false positives also).

It's worth noting that, in the case of object detection, these two metrics are computed for a certain threshold of **IoU** (Intersection over Union). The IoU represents the match between the predicted bounding box and the annotated one. Given the high variability of bounding box size and form between expert and citizen annotations, we decided to use two thresholds for the IoU: 0.5 (standard value) and 0.01 (high tolerance).

## Key results
After several rounds of training, of both the head and the internal layers of the Mask-RCNN model, we manage to obtain the following results:

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

## Next steps
* test [Yolov4](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects) for object detection (alternative model to Mask-RCNN)
* test [Rolo](https://github.com/Guanghan/ROLO) for object tracking

## Acknowledgments
A huge thank you to [Marjolaine Matabos](https://annuaire.ifremer.fr/cv/20350/en/), Benthic ecologist at the Laboratoire Environnement Profond (PDG-REM-EEP-LEP), for very spontaneously sharing annotated examples of various species, as well as research papers providing more context on the project.
