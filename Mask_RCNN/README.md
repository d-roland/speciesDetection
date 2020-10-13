# Local installation of Matterport Mask_RCNN implementation

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

The next step is to edit the code for the custom classes we want to create. This happens in the respective "buccin" and "crabe" folders, which have to be placed in the "sample" folder under Mask_RCNN root.
