# Deep-sea Species Detection

## Context and challenge
In order to study long-term temporal dynamics of vent communities, the Laboratoire Environnement Profond (Ifremer) leverages multidisciplinary seafloor observatories deployed in several target sites. The corresponding modules are equipped with cameras, programmed to record 20-min video sequences six times a day (02.00, 06.00, 10.00, 14.00, 18.00 and 22.00 UTC) with different zoom levels per sequence. Video sequences are later analyzed by experts (researchers) to localize the species, and notably:
* Crab Segonzacia mesatlantica from the Lucky Strike vent field (Mid-Atlantic Ridge, 1700m below sea level). Below is a sample image with 3 expert annotations illustrated by squared bounding boxes:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_expert_annotations.png)
* Buccinidae gastropods from the Grotto hydrothermal edifice (Main Endeavour Field, Juan de Fuca Ridge, 2200m below sea level). Below is a sample image with 11 citizen annotations:
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/sample_citizen_annotations.png)

These videos are a crucial source of information for assessing natural variability and ecosystem responses to increasing human activity in the deep sea. But manually reviewing and annotating video sequences is a tedious and time-consuming process for experts, particularly as the quantity of recorded data dramatically increased over the past years.\
Recently, some researchers developped [crowdsourcing initiatives](https://www.deepseaspy.com/) in order to leverage untrained volunteers and scale the annotation process. But the quality of these annotations has to be compared to expert ones.

Given recent progress of Machine Learning algorithms, notably on object detection tasks, we decided to test some renowned models on both expert and citizen annotations. 


## Approach
In order to perform object detection on custom specimens, we used [Matterport implementation of Mask-RCNN](https://github.com/matterport/Mask_RCNN). Althought this implementation allows more than object detection (namely, instance segmentation), its Keras and Tensorflow base is quite handy to use.\
The base model is pretrained on Coco dataset, and able to recognize 80 basic shapes. We used transfer learning to fine tune it to our specific specimens.

Some data preparation was required, as expert and citizen annotations come in different format. In order to get comparable data, we decided to recreate the bounding box of each annotation as a 50 pixels square around the center of each manual annotation. Also, we needed to ensure that we used only images with annotations in order to train the model.

As per the **metrics**, given we focused solely on object detection (approximate localization on images), we decided to measure:
* **mAP** (mean Average Precision: mean proportion of our predictions that are correct): a strong mAP would imply less false positive, but may also imply that we miss some specimens.
* **Recall** (how good we find all the positives, eg all the annotated specimens). A strong Recall is interesting if we want to find the most specimens, at all cost (eg with false positives also).

It's worth noting that, in the case of object detection, these two metrics are computed for a certain threshold of **IoU** (Intersection over Union). The IoU represents the match between the predicted bounding box and the annotated one. Given the high variability of bounding box size and form between expert and citizen annotations, we decided to use two thresholds for the IoU: 0.5 (standard value) and 0.01 (high tolerance).


## Key results
After several rounds of training, of both the head and the internal layers of the Mask-RCNN model, we manage to obtain the following results:

1. (Crabs) Model trained on 532 images with *expert* annotations from 2012-2013, 40 epoch head / 80 epoch all layers:

Test set | mAP | Recall
--- | --- | ---
134 images with expert annotations from 2012-2013 | 68% (IoU 0.5) to 72% (IoU 0.01) | 72% (IoU 0.5) to 75% (IoU 0.01)
95 images with citizen annotations | 12% (IoU 0.5) to 21% (IoU 0.01) | 18% (IoU 0.5) to 35% (IoU 0.01)

**Interpretation**: performance on test set (expert annotations) is not amazing but seems to have reached a plateau. Further fine tuning of hyperparameters may be required, as data augmentation didn't bring much improvement. Low performance on citizen annotations can be explained by three factors: difference between the two series of images (the citizen ones are more similar to expert images from 2014-2015), (lower) quality of citizen annotations, and also possible overfitting on training data.


2. (Crabs) Model trained on 448 images with *expert* annotations from 2014-2015, 30 epoch head / 60 epoch all layers:

Test set | mAP | Recall
--- | --- | ---
113 images with expert annotations from 2014-2015 | 73% (IoU 0.5) to 78% (IoU 0.01) | 77% (IoU 0.5) to 80% (IoU 0.01)
95 images with citizen annotations | 44% (IoU 0.5) to 48% (IoU 0.01) | 46% (IoU 0.5) to 51% (IoU 0.01)

**Interpretation**: performance on test set is quite satisfactory. Increasing training time a bit might bring a few additional points, as well as hyperparameters tuning. The model trained on expert data is good enough to be used as benchmark of the quality of citizen annotations: lower quality on these annotations reflects their lower quality.


3. (Crabs) Model trained on 377 images with *citizen* annotations, 30 epoch head / 60 epoch all layers:

Test set | mAP | Recall
--- | --- | ---
95 images with citizen annotations | 29% (IoU 0.5) to 36% (IoU 0.01) | 31% (IoU 0.5) to 38% (IoU 0.01)
113 images with expert annotations from 2014-2015 | 48% (IoU 0.5) to 53% (IoU 0.01) | 52% (IoU 0.5) to 55% (IoU 0.01)

**Interpretation**: a higher performance obtained on test images annotated by experts may again reflect the higher quality of their annotations.

Example of prediction on a 2014 image annotated by expert: ground truth in green, prediction in red, with score/IoU for each.
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/prediction_expert_2014.png)

4. (Buccins) Model trained on 2656 images with *citizen* annotations, 20 epoch head:

Test set | mAP | Recall
--- | --- | ---
664 images with citizen annotations | 42% (IoU 0.5) to 79% (IoU 0.01) | 51% (IoU 0.5) to 81% (IoU 0.01)
267 images with expert annotations | 28% (IoU 0.5) to 85% (IoU 0.01) | 42% (IoU 0.5) to 85% (IoU 0.01)

**Interpretation**: even with small training (just 20 epoch of network head), a high quality of prediction is obtained on the citizen annotations. This is not surprising given the strong contrast between specimens and the background of images. A longer training time may deliver even better results. However prediction performance drops when evaluating on expert annotations: this reveals the lower quality of citizen annotations (85% precision and recall with only 1% overlap between citizen and expert annotation), and the difficulty of citizen-trained model to generalize to accurate predictions. 


5. (Buccins) Model trained on 1061 images (zoom angle) with *expert* annotations, 30 epoch head:

Test set | mAP | Recall
--- | --- | ---
267 images with expert annotations | 91% (IoU 0.5) to 94% (IoU 0.01) | 92% (IoU 0.5) to 95% (IoU 0.01)
266 images with citizen annotations | 41% (IoU 0.5) to 78% (IoU 0.01) | 47% (IoU 0.5) to 94% (IoU 0.01)


**Interpretation**: thanks to high quality annotations and long training (30 epochs head + 30 epochs full network), the model get an almost perfect prediction performance on both metrics when evaluated on expert annotations. The drop in performance observed when evaluating on citizen annotations reveals the lower quality of these latter: 94% recall with IoU 1% but only 78% mean AP (many false positive created by citizens).

Example of prediction on an image annotated by citizen: ground truth in green, prediction in red, with score/IoU for each.\
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/prediction_citoyen_buccin.png)


## Next steps
* Leverage results and trained models to improve current annotation process
* Test [EfficientDet](https://github.com/xuannianz/EfficientDet) for object detection (alternative model to Mask-RCNN, higher performance on [Coco benchmark](https://paperswithcode.com/sota/object-detection-on-coco))
* Test application of trained models on object tracking


## Acknowledgments
A huge thank you to [Marjolaine Matabos](https://annuaire.ifremer.fr/cv/20350/en/), Benthic ecologist at the Laboratoire Environnement Profond (PDG-REM-EEP-LEP), for very spontaneously sharing annotated examples of various species, as well as research papers providing more context on the project.

Thanks also for the opportunity to spot a great Hydrolagus trolli :)
![alt text](https://github.com/d-roland/speciesDetection/raw/main/images/hydrolagus_trolli.png)

