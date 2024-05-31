import time



# Function to change traffic lights based on congestion
def manage_traffic_lights(lanes):
    i = 1
    # Get the most congested lane
    most_congested_lane = max(lanes, key=lanes.get)

    for key, value in lanes.items():
        print(f"{key}: {value}")

    # Simulate changing traffic lights based on congestion
    for lane, congestion in lanes.items():
        if lane == most_congested_lane:
            print("Lane " + str(i) + ": Green")  # Set traffic light to Green for most congested lane
        else:
            print("Lane " + str(i) + ": Red")  # Set traffic light to Red for other lanes
        i += 1
