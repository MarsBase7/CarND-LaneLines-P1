# **Finding Lane Lines on the Road** 

[//]: # (Image References)
[image0]: ./img0_solidYellowCurve2.png
[image1]: ./img1_solidWhiteRight_hough.png
[image2]: ./img2_solidWhiteRight_draw.png
[image3]: ./img3_solidWhiteRight_line.png

This is a brief writeup report of Self-Driving Car Engineer P1.

![alt text][image0]

---
   

## **Describe the pipeline**

The pipeline of [P1](./P1.ipynb) consisted of **6** steps:
1. Grayscale the image
2. Gaussian smoothing
3. Canny edges
4. Region of interest
5. Hough transform
6. Draw the lines

> **Grayscale the image**

The first step is to conver the images to grayscale by `cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)` .

> **Gaussian smoothing**

Then, apply Gaussian smoothing `cv2.GaussianBlur(GRAY_img, (kernel_size, kernel_size), 0)` on the grayscale image with a proper kernel_size `5` .

> **Canny edges**

After that, apply the Canny transform `cv2.Canny(Gaus_img, low_threshold, high_threshold)` on the Gaussian smoothing image with low_threshold `50` and high_threshold `150` .

> **Region of interest**

Because of the actual image or video scences, the interest region is a quadrilateral with the ceiling vertices `±3%` near the middle x coordinate and about `60%` of the y coordinate, the bottom vertices are on the x coordinate.

> **Hough transform**

There are some parameters for Hough space grid:

- a `rho` of `2` pixels and `theta` of 1 degree (`pi/180` radians). 
- a `threshold` of `30`, meaning at least 30 points in image space need to be associated with each line segment. 
- a `min_line_length` of `50` pixels, and `max_line_gap` of `20` pixels.

![alt text][image1] 

> **Draw the lines**

In order to draw a single line on the left and right lanes, the draw_lines() function was modified and two sub functions was defined to support, line_filter() and line_cal(). The main modifying ideas contain:

- seperate left lines or right lines by slope `(y2 - y1)/(x2 - x1)`
- find out the main pot and the main slope of each side lines, where their slope diff between `±0.1` to average.
- draw the two single solid lines, which pass through the main pot and have the main slope, inside the ROI(region of interest).

![alt text][image2] ![alt text][image3]

BTW, the modifying above can work on all test images and videos beside the challenge one. 
So, the final modifying on draw_lines() was updating the slope filter, which discard the lines with slope between `±0.5`(those are irrelevant lines, such as shadows on hood). 
Finally, **the code can work on the _challenge.mp4_ not too bad.**
   
## **Shortcomings**

- Sensitive to interference factors, such as shadows, reflections, and so on.
- The ROI is fixed, which can not adapt the change of the driving vision automatically.
- Big calculation amount, which might impact real-time detection.   

## **Possible improvements**

- Use deep learning algorithm to detect lane lines.
- Consider the status of the lines in a few frames passed to stablilize the slope change.
- Use the calculus to find or draw the curve lines more precisely.