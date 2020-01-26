# Labelled Database Maker for Computer Vision

> The aim of this project was to create a labelled image dataset automatically, rather than by hand, that could be used to train a model for object detection and landmark recognition. This method is a work-around to creating a labelled image dataset by hand, which can be a very long and tedious process.

> This particular program generates images of playing cards on various backgrounds, with different positions and perspectives. It keeps track of the bounding box as well as the four corner coordinates of the cards, so that images are automatically labelled when it comes time to train the model.   

## Results 

Here is a sample of the generated database : 

<p align="center">
  <img src="/Showcase/Sample.jpg">
 </p>
 
These may not look like it, but they are generated images, not pictures taken by hand. You can have a look at [/Database](/Database) for a closer look at these, where you might detect some signs that they are not real. 

The associated labels are saved in [/XMLs](/XMLs).

I trained an [object detection model](http://dlib.net/train_object_detector.py.html) in conjunction with a [shape detection model](http://dlib.net/train_shape_predictor.py.html) using dlib 19.19. The trained models' predictions were suprisingly good using real images : 

<p align="center">
  <img src="/Results/Pred2.png">
 </p>

You can see that the positions of the four corners of the card are predicted quite accurately, and the model detects that there is a card on the image. You can have a look at [/Results](/Results) for more test results. 

## How it works

The program randomly picks a card and a background image from a set of available pictures ([/Cards](/Cards), [/Backgrounds](/Backgrounds)). It applies a number of rotations, perspectives, and position transformations to the card while keeping track of the corner and bounding box coordinates. Images are created until the disered sample size is reached. 

Example of a card transformation : 

Raw Image | Transformed Image
------------ | -------------
![Raw](/Showcase/Source_1.png) | ![Transformed](/Showcase/Card_transform.png)

## Running it on your machine

You can use your own card and background images by replacing those in [/Cards](/Cards) and [/Backgrounds](/Backgrounds) to your own. You will need to use the Dlib python templates (linked in the Results section) to train and test your models. During training, you need to copy and paste the labelled information from [/XMLs/Box_points.txt](/XMLs) to the corresponding train and test XMLs templates provided.

You will also need the following libraries :
- [dlib 19.19](https://anaconda.org/conda-forge/dlib)
- [Pillow 7.0.0](https://anaconda.org/conda-forge/pillow)
- [Numpy 1.17.5](https://anaconda.org/conda-forge/numpy)


## Acknowledgments

Thank you to 
[DeepLearning.ai](https://www.youtube.com/watch?v=rRB9iymNy1w),
[Luca Anzalone](https://medium.com/datadriveninvestor/training-alternative-dlib-shape-predictor-models-using-python-d1d8f8bd9f5c),
[Dlib](http://dlib.net/), and many more for inspiration and guidance. 


