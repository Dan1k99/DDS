
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))

# Configure connection
connector = rti.Connector("MyParticipantLibrary::Tempsensor1", filepath + "/DDS.xml")
output_DDS_temp_sensor1 = connector.getOutput("MyPublisher::MyWriter_Tempsensor1")

while True:
    # Generate a random temperature value between 10 and 60
    current_temperature = random.randint(10, 60)

    # Set the temperature value and write to DDS
    output_DDS_temp_sensor1.instance.setNumber("Temp", current_temperature)
    output_DDS_temp_sensor1.write()

    # Sleep for 1 second
    sleep(1)

    # Print the published temperature
    print(f'Sensor1 Temp Value: {current_temperature}')
