# Labelled Database Maker for Computer Vision

> The aim of this project was to create a labelled image dataset automatically, rather than by hand, that could be used to train a model for object detection and landmark recognition. This method is a work-around to creating a labelled image dataset by hand, which can be a very long and tedious process.

> This particular program generates images of playing cards on various backgrounds, with different positions and perspectives. It keeps track of the bounding box as well as the four corner coordinates of the cards, so that images are automatically labelled when it comes time to train the model.   

## Results 

Here is a sample of the generated database : 

<p align="center">
  <img src="/Showcase/Sample.jpg">
 </p>
 
These may not look like it, but they are generated images, not pictures taken by hand. You can have a look at [/Database](/Database) for a closer look at these, where you might detect some signs that they are not real. 

The associated labels are saved in [/XMLs](/XMLs) in the file "Box_points.txt".

I trained an [object detection model](http://dlib.net/train_object_detector.py.html) in conjunction with a [shape detection model](http://dlib.net/train_shape_predictor.py.html) using [dlib 19.19](https://anaconda.org/conda-forge/dlib). The trained models' predictions were suprisingly good using real images : 

<p align="center">
  <img src="/Results/Pred2.png">
 </p>

You can see that the position of the four corners of the card is predicted quite accurately, and the model detects that there is a card on the image. You can have a look at [/Results](/Results) for more prediction results. 

## How it works

The program randomly picks a card and a background image from a set of available raw pictures ([/Cards](/Cards), [/Backgrounds](/Backgrounds)). It applies a number of rotations, perspectives, and position transformations to the card whilst keeping track of the corner and bounding box coordinates. This process is repeated until the disered sample size is reached. 

Example of a card tranformation : 

Raw Image | Transformed Image
------------ | -------------
![Raw](/Showcase/Source_1.png) | ![Transformed](/Showcase/Card_transform.png)

 
