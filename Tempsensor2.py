
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))

# Configure connection
connector = rti.Connector("MyParticipantLibrary::Tempsensor2", filepath + "/DDS.xml")
output_DDS_temp_sensor = connector.getOutput("MyPublisher::MyWriter_Tempsensor2")

while True:
    # Generate a random temperature value between 0 and 50
    current_temperature = random.randint(0, 50)

    # Set the temperature value and write to DDS
    output_DDS_temp_sensor.instance.setNumber("Temp", current_temperature)
    output_DDS_temp_sensor.write()

    # Sleep for 0.1 seconds
    sleep(0.1)

    # Print the published temperature
    print(f'Published Temp2: {current_temperature}')
