# TODO: Build your pipeline that will draw lane lines on the test_images

# find the end point of the left line or right line
def find_line_end(x1, y1, x2, y2, line_end):
    if y1 = min(y1, y2, line_end[1]):
        line_end = (x1, y1)
    elif y2 = min(y1, y2, line_end[1]):
        line_end = (x2, y2)
    return line_end

# modify the "draw_lines" function to make lines connected
def draw_lines_connect(img, lines, color=[255, 0, 0], thickness=2):
# get the average slope of lines and find the vertex of the connect line
    left_lines_slope = []
    right_lines_slope = []
    left_line_end = (0, img.shape[0])   #start from the left bottom corner
    right_line_end = (img.shape[1], img.shape[0])   #start from the right bottom corner
    for line in lines:
        for x1,y1,x2,y2 in line:
            one_slope = ((y2 - y1) / (x2 - x1))
            if one_slope > 0:
                left_lines_slope.append(one_slope)
                left_line_end = find_vertex(x1, y1, x2, y2, left_line_end)
            else:
                right_lines_slope.append(one_slope)
                right_line_end = find_vertex(x1, y1, x2, y2, right_line_end)
    left_slope_avg = sum(left_lines_slope) / len(left_lines_slope)
    right_slope_avg = sum(right_lines_slope) / len(right_lines_slope)
# compute the start point of the two lines
    x_left_start = int(img.shape[0] - left_line_end[1] + left_slope_avg * left_line_end[0])
    left_line_start = (x_left_start, img.shape[0])
    x_right_start = int(img.shape[0] - right_line_end[1] + right_slope_avg * right_line_end[0])
    right_line_start = (x_right_start, img.shape[0])
# draw the two connected lines
    cv2.line(img, left_line_start, left_line_end, color, thickness)
    cv2.line(img, right_line_start, right_line_end, color, thickness)

# modify the "hough_lines" function to use draw_lines_connect
def hough_lines_connect(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines_connect(line_img, lines)
    return line_img

def pipeline(img_name):
# Read in and grayscale the image
    image = mpimg.imread(img_name)
    gray = grayscale(image)
    imshape = image.shape

# Define a kernel size and apply Gaussian smoothing
    kernel_size = 5
    blur_gray = gaussian_blur(gray, kernel_size)

# Define our parameters for Canny and apply
    low_threshold = 50
    high_threshold = 150
    edges_img = canny(blur_gray, low_threshold, high_threshold)

#create vertices of a quadrilateral to select
    left_bottom = (0,imshape[0])
    left_ceiling = (int(imshape[1] * 0.47), int(imshape[0] * 0.6))
    right_ceiling = (int(imshape[1] * 0.53), int(imshape[0] * 0.6))
    right_bottom = (imshape[1],imshape[0])
    vertices = np.array([[left_bottom, left_ceiling, right_ceiling, right_bottom]], dtype=np.int32)

#create a masked edges image using cv2.fillPoly()
    masked_edges_img = region_of_interest(edges_img, vertices)

# Define the Hough transform parameters
    rho = 2
    theta = np.pi/180
    threshold = 30
    min_line_len = 40
    max_line_gap = 20

# Output "lines" is an array containing endpoints of detected line segments
    lines = hough_lines_connect(masked_edges_img, rho, theta, threshold, min_line_len, max_line_gap)

# Draw the lines on the image
    lanelines_img = weighted_img(lines, image) 
    plt.imshow(lanelines_img)


# then save them to the test_images_output directory.

# image_files = os.listdir("test_images/")
pipeline(img_name)
