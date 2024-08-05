import streamlit as st
from sklearn.cluster import DBSCAN
from PIL import Image
import cv2
import numpy as np
import os

if "most_sheets_frame" not in st.session_state:
    st.session_state.most_sheets_frame = None

def preprocess_frame(frame):

        # Adjusting contrast
        alpha = 1.25
        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=0)

        return adjusted

def get_sheet_count(image):
        preprocessed_image = preprocess_frame(image)

        # Edge detection using Canny edge detector
        edges = cv2.Canny(preprocessed_image, 25, 100, apertureSize=3)  # 50, 150

        # Detecting lines using PHT
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        # minLineLength=100
        # threshold=100

        # If no lines are detected, return 0
        if lines is None:
            print('Number of sheets detected: 0')
        else:
            # Filtering out non-horizontal lines
            horizontal_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y1 - y2) < 2:
                    horizontal_lines.append(line[0])

            if not horizontal_lines:
                return 0
            else:
                # y-coordinate of the midpoint of each line for DBSCAN
                line_midpoints = []
                for line in horizontal_lines:
                    x1, y1, x2, y2 = line
                    midpoint_y = (y1 + y2) // 2
                    line_midpoints.append([midpoint_y])

                line_midpoints = np.array(line_midpoints)

                # Using kNN to find the optimal value of epsilon for frame 0
                # if self.frame_number == 50:
                #     largest_distance = pkd(line_midpoints, 5)
                #     self.frame_number += 1
                # else:
                #     self.frame_number += 1

                # DBSCAN to cluster the line midpoints
                clustering = DBSCAN(eps=2, min_samples=2).fit(line_midpoints) # eps=10
                num_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)

                line_image = np.copy(image)
                for line in horizontal_lines:
                    x1, y1, x2, y2 = line
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 255), 1)

                # self.print_text(f'Sheets: {num_clusters}')
                return num_clusters, line_image

def main():
    st.markdown("<h1 style='text-align: center;'>Sheet Counter 🔍</h1>", unsafe_allow_html=True)

    st.markdown("""So you want to know how many sheets are there in your video/image? 🤔
                You are at the right place! Just upload your video/image and let the magic happen! 🎩
                If you wanna see the code for this app, visit the [repo](https://github.com/soumyadeepbose/sheet-counter). ✨""")

    uploaded_file = st.file_uploader("Choose a video (with sheets of course 😉)...", type=["mp4", "avi", "mov", ".jpg", ".jpeg", ".png"])
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if 'video' in file_type:

            # Saving the uploaded file to fixed location
            input_path = os.path.join("uploaded_video.mp4")
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            cap = cv2.VideoCapture(input_path)

            # fps = cap.get(cv2.CAP_PROP_FPS)
            # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # output_path = "media\\processed_video.mp4"
            # out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

            if st.button("Process Video"):
                sheets = []
                frame_num = 0

                progress_bar = st.progress(0)

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (600, 400))
                    num_sheets, line_frame = get_sheet_count(frame)
                    sheets.append(num_sheets)

                    if len(sheets) > 0:
                        if num_sheets >= max(sheets):
                            st.session_state.most_sheets_frame = line_frame

                    # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                    # out.write(processed_frame)

                    frame_num += 1
                    progress_bar.progress(frame_num / frame_count)

                cap.release()
                # out.release()
                os.remove(input_path)

                if sheets:
                    max_sheets = max(sheets)
                    st.markdown(f"""
                        <div style="font-size:24px; font-weight:bold;">
                            </br><center>Number of sheets in the video is {max_sheets}</center></br>
                        </div>
                        """, unsafe_allow_html=True)
                    # st.write(f"**Mean number of sheets detected: `{max_sheets}`**")
                    st.image(st.session_state.most_sheets_frame, caption="Frame with most sheets, i.e. "+str(max_sheets)+" sheets.")
                    st.session_state.most_sheets_frame = None
                    # st.write(f"{sheets}")
                else:
                    st.write("No sheets detected.")

                # st.video("media\\processed_video.mp4")

        elif 'image' in file_type:
            image = Image.open(uploaded_file)
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            num_sheets, line_image = get_sheet_count(image)
            st.markdown(f"""
                <div style="font-size:24px; font-weight:bold;">
                    </br><center>Number of sheets in the image is {num_sheets}</center></br>
                </div>
                """, unsafe_allow_html=True)
            height, width, _ = line_image.shape
            height = int(height * 0.33)
            width = int(width * 0.33)
            line_image = cv2.resize(line_image, ((width), (height)))
            st.image(line_image, caption=f"Image has {num_sheets} sheets.")

        else:
            st.error("Please upload a valid video or image file.")

if __name__ == "__main__":
    main()
