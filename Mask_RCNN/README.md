# Local installation of Matterport's Mask_RCNN implementation

## Clone Mask_RCNN repository

```python
git clone https://github.com/matterport/Mask_RCNN.git
```

## Install all required dependencies

```python
cd Mask_RCNN
pip install -r requirements.txt
```

## Download pre-trained weights
These weights have to be installed at the root of the cloned Mask_RCNN repository

```python
wget https://github.com/matterport/Mask_RCNN/releases/download/v2.1/mask_rcnn_balloon.h5
```
