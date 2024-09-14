import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import datetime

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))

# Configure connection
connector = rti.Connector("MyParticipantLibrary::Camera", filepath + "/DDS.xml")
output_DDS_camera = connector.getOutput("MyPublisher::MyWriter_Camera")

while True:
    # Get the current time in HH:MM:SS format
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Set the camera timestamp and write to DDS
    output_DDS_camera.instance.setString("Camera", current_time)
    output_DDS_camera.write()

    # Sleep for 0.1 seconds
    sleep(0.1)

    # Print the published camera timestamp
    print(f'Camera published: {current_time}')
