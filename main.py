import tkinter as tk
from tkinter import filedialog, Text, RIGHT, Y, messagebox
from tkinter.ttk import Progressbar
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
import cv2
from PIL import Image, ImageTk
import numpy as np
import statistics

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        self.video_frame = tk.Label(root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        self.canvas = tk.Canvas(self.video_frame, width=600, height=400)
        self.canvas.pack()

        self.text_frame = tk.Frame(root)
        self.text_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        self.text_area = Text(self.text_frame, wrap='word', state='disabled', width=40, height=25)
        self.text_area.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_area['yscrollcommand'] = self.scrollbar.set

        self.file_button = tk.Button(root, text="Choose Video", command=self.open_video)
        self.file_button.grid(row=1, column=0, pady=10)

        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(row=2, column=0, pady=10)

        self.all_frames_line_midpoints = []
        self.most_sheets_frame = None

    def open_video(self):
        self.video_source = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if not self.video_source:
            return

        self.vid = cv2.VideoCapture(self.video_source)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.delay = 5
        if not self.vid.isOpened():
            messagebox.showerror("Error", "Unable to open the video file.")
        else:
            self.stop = False
            self.print_text("Video opened successfully.")
            self.sheets = []
            self.play_video()

    def play_video(self):
        if not self.vid or not self.vid.isOpened():
            messagebox.showwarning("Warning", "No video has been opened.")
            return

        self.stop = False
        self.print_text("Playing video: " + self.video_source)
        self.frame_number = 0
        self.update_frame()

    def stop_video(self):
        self.stop = True

    def preprocess_frame(self, frame):

        # Increase contrast
        alpha = 1.25  # Contrast control (1.0-3.0)
        beta = 0    # Brightness control (0-100)
        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        return adjusted

    def get_sheet_count(self, image):
        # Preprocess the frame
        preprocessed_image = self.preprocess_frame(image)

        # Edge detection using Canny edge detector
        edges = cv2.Canny(preprocessed_image, 25, 100, apertureSize=3)  # 50, 150

        # Detect lines using Probabilistic Hough Transform
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

        # If no lines are detected, return 0
        if lines is None:
            return 0, image
        else:
            # Filter out non-horizontal lines
            horizontal_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y1 - y2) < 1:  # Adjust this threshold if needed
                    horizontal_lines.append(line[0])

            if not horizontal_lines:
                return 0, image
            else:
                # Convert lines to a format suitable for DBSCAN (use the y-coordinate of the midpoint of each line)
                line_midpoints = []
                for line in horizontal_lines:
                    x1, y1, x2, y2 = line
                    midpoint_y = (y1 + y2) // 2
                    line_midpoints.append([midpoint_y])

                self.all_frames_line_midpoints.append(line_midpoints)

                line_midpoints = np.array(line_midpoints)

                # Use DBSCAN to cluster the line midpoints
                clustering = DBSCAN(eps=2, min_samples=2).fit(line_midpoints)

                # Get the number of unique clusters
                num_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)

                # Draw the detected lines on the image for visualization
                line_image = np.copy(image)
                for line in horizontal_lines:
                    x1, y1, x2, y2 = line
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 255), 1)

                return num_clusters, line_image

    def update_frame(self):
        if self.vid and not self.stop:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (600, 400))

                result = self.get_sheet_count(frame)
                num_sheets = result[0]
                frame = result[1]

                if len(self.sheets) > 0:
                    if num_sheets >= max(self.sheets):
                        self.most_sheets_frame = frame

                self.print_text(f'Sheets: {num_sheets}')

                self.sheets.append(num_sheets)
                cv2.putText(frame,
                            f'Sheets: {num_sheets}',
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2)

                image = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
                self.canvas.image_tk = image_tk

                self.progress['value'] = (self.frame_number / self.total_frames) * 100
                self.frame_number += 1

                self.root.after(self.delay, self.update_frame)
            else:
                self.vid.release()
                self.canvas.image_tk = None
                self.print_text("Video has ended.")
                self.print_text(f"Sheets: {max(self.sheets)}")
                cv2.imshow("Frame with most sheets", self.most_sheets_frame)

    def print_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def terminate(self):
        self.stop = True
        self.vid.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.protocol("WM_DELETE_WINDOW", player.terminate)
    root.mainloop()
