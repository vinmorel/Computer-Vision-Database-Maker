import os
import glob
import dlib
import time

# Init folders
sample_folder = "/Users/VincentMorel/Desktop/github/Cards_Tracking/Cards/Sample"
test_folder = "/Users/VincentMorel/Desktop/github/Cards_Tracking/Cards/Test"


# load models
predictor = dlib.shape_predictor("predictor4_poker_best.dat")
detector = dlib.simple_object_detector("detectorc80.svm")

n = 0

# load test images
win = dlib.image_window()
for f in glob.glob(os.path.join(test_folder, "*.jpg")):
    n += 1
    img = dlib.load_rgb_image(f)
    time.sleep(3)
    win.clear_overlay()
    win.set_image(img)
    
    im = Image.open(f)
    
    
    print("For image file : {}".format(f))
    # Ask the detector to find the bounding boxes of each face. 
    dets = detector(img, 0)
    print("Number of cards detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {}.Part 3: {},Part 4: {} ...".format(shape.part(0),
                                                                        shape.part(1),
                                                                        shape.part(2),
                                                                        shape.part(3)))
        # Draw the face landmarks on the screen.
        win.add_overlay(shape)
    win.add_overlay(dets)
    
    dlib.hit_enter_to_continue()

