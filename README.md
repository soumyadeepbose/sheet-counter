# Sheet Counter 🔍

## Overview
Sheet Counter is a Streamlit application designed to count the number of sheets in a given video or image. The app uses computer vision techniques to detect and count horizontal lines, which represent sheets in the input media. There are two versions of the app available: one built using Streamlit and the other using Tkinter. The Streamlit app is more user-friendly and provides a better user experience, while the Tkinter app is more lightweight and can be used for quick testing. I developed the tkinter app first, and then I decided to build a more user-friendly version using Streamlit. 😅

## Approach
The code first reads the input video frame by frame and increases contrast to make the horizontal lines more visible. The frame is then passed to the Canny Edge Detector to detect the edges, and then Probabilistic Hough Line Transform is used to get the lines representing the edges. The code then filters out the non-horizontal lines and then using the y coordinates of mid-points of the lines, DBSCAN performs clustering to group lines on similar y coordinates as distinct sheets. The number of clusters is then counted to get the number of sheets in the frame. 

## Installation and Setup

1. Clone the repository into a folder:
    ```sh
    git clone https://github.com/soumyadeepbose/sheet-counter.git
    ```
2. Navigate to the project directory, and install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Now run the streamlit app:
    ```sh
    streamlit run app.py
4. Alternatively, you can run the app using the following command:
    ```sh
    python main.py
    ```

## Usage for Streamlit App
1. Select the video or image file you want to upload.
2. Click the "Process Video" button to start the sheet counting process.
3. Grab a quick coffee and wait for the results to appear.
3. View the result and the frame with the most sheets detected.

## Usage for Tkinter App
1. Click on the "Choose Video" button to select the video file you want to upload. Please note that you can't use the Tkinter app for image processing.
2. Grab a quick coffee and wait a while.
3. The sheet counter will be displayed in the right text area.
4. The frame with the most sheets detected will be displayed as a new frame.

## Screenshots
![Tkinter App](readme_images/tkinter_app.png "Tkinter App")

## Main Requirements
- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Pillow](https://python-pillow.org/)

## Author
- [Soumyadeep Bose 😊](https://www.linkedin.com/in/soumyadeepbose)