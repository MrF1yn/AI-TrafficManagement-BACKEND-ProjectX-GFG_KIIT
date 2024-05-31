import cv2
import os

def get_frame(video_path, frame_number, width=800, height=600):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Set the frame number to read
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame at the specified frame number
    success, frame = video_capture.read()
    # Resize the frame
    if success:

        frame = cv2.resize(frame, (width, height))

        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Save the resized frame as 'temp.jpg' in the script directory
        temp_file_path = os.path.join(script_dir, 'temp.jpg')
        cv2.imwrite('temp.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # print(f"Resized frame saved as: {temp_file_path}")

    # Release the video capture object
    video_capture.release()

    # Check if the frame was read and resized successfully
    if success:
        return frame, temp_file_path  # Return the frame and the file path
    else:
        return None, None

# Example usage:
# def main():
#     video_path = r'C:\Users\KIIT\Downloads\vehicle-count\data\vid2.avi'
#     frame_number = 0
#
#     # Call the function to get the frame
#     frame, saved_file_path = get_frame(video_path, frame_number)
#
#     if frame is not None:
#         cv2.imshow('Resized Frame', frame)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#         print(f"Frame saved as: {saved_file_path}")
#     else:
#         print('Error: Failed to retrieve frame.')
#
# if __name__ == "__main__":
#     main()