
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
import datetime

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))

# Configure connection
connector = rti.Connector("MyParticipantLibrary::Button", filepath + "/DDS.xml")
output_DDS_button = connector.getOutput("MyPublisher::MyWriter_Button")

while True:
    # Set the button state to ON (1) and write to DDS
    output_DDS_button.instance.setNumber("Button", 1)
    output_DDS_button.write()
    print("Button is switched ON")

    # Sleep for 20 seconds
    sleep(20)

    # Set the button state to OFF (0) and write to DDS
    output_DDS_button.instance.setNumber("Button", 0)
    output_DDS_button.write()
    print("Button is switched OFF")

    # Sleep for 5 seconds
    sleep(5)
