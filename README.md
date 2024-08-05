# Sheet Counter

## Overview
Sheet Counter is a Streamlit application designed to count the number of sheets in a given video or image. The app uses computer vision techniques to detect and count horizontal lines, which represent sheets in the input media.

## Features
- Upload a video or image to the app.
- Process the uploaded media to count the number of sheets.
- Display the frame with the most sheets detected.
- Supports various video formats (mp4, avi, mov) and image formats (jpg, jpeg, png).

## Installation
1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd <project-directory>
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```
2. Open your web browser and go to `http://localhost:8501`.
3. Upload a video or image file.
4. Click the "Process Video" button to start the sheet counting process.
5. View the results and the frame with the most sheets detected.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Pillow](https://python-pillow.org/)