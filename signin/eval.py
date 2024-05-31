from . import vehicle_count
from . import frame
from . import signals
import cv2


# Example usage:
# image_path = r'C:\Users\KIIT\Downloads\Vehicle Detection System\data\demo9.jpg'  # Path to the image
# number = count_vehicles(image_path)

def main():
    video_path1 = r'C:\Users\KIIT\Downloads\vehicle-count\data\vid1.avi'
    video_path2 = r'C:\Users\KIIT\Downloads\vehicle-count\data\vid2.avi'
    video_path3 = r'C:\Users\KIIT\Downloads\vehicle-count\data\vid3.avi'
    video_path4 = r'C:\Users\KIIT\Downloads\vehicle-count\data\vid4.avi'
    # frame_number = 5500
    frame_number = 2
    lane = {}

    vid = [video_path1, video_path2, video_path3, video_path4]

    for i in range(4):
        frame1, saved_file_path = frame.get_frame(vid[i], frame_number)
        number = vehicle_count.count_vehicles('temp.jpg')
        lane[i + 1] = number

    signals.manage_traffic_lights(lane)


def evaluate(vid):
    # frame_number = 5500
    frame_number = 2
    lane = {}


    for i in range(4):
        frame1, saved_file_path = frame.get_frame(vid[i], frame_number)
        number = vehicle_count.count_vehicles('temp.jpg')
        lane[i + 1] = number

    signals.manage_traffic_lights(lane)


if __name__ == "__main__":
    main()
