import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Dashboard", filepath + "/DDS.xml")

# Input Domains
input_DDS_Camera = connector.getInput("Dashboard::dashboard_Camera")
input_DDS_temp_extreme = connector.getInput("Dashboard::dashboard_temp_extreme")
input_DDS_temp2_extreme = connector.getInput("Dashboard::dashboard_temp2_extreme")
input_DDS_actuator_status = connector.getInput("Dashboard::dashboard_actuator_status")
input_DDS_actuator2_status = connector.getInput("Dashboard::dashboard_actuator2_status")

# Initialize parameters
camera_message = ""
temp1_series = []
temp2_series = []
actuator_status_series = []
actuator2_status_series = []

def update_series(series, message, limit=10):
    """Update the series with the new message, ensuring the series length doesn't exceed the limit."""
    if len(series) >= limit:
        series.pop(0)
    series.append(message)

while True:
    sleep(5)  # Sleep for 5 seconds

    # Take the data from the DDS inputs
    input_DDS_temp_extreme.take()
    input_DDS_temp2_extreme.take()
    input_DDS_actuator_status.take()
    input_DDS_actuator2_status.take()

    # Camera Connectivity
    for sample in input_DDS_Camera.samples.valid_data_iter:
        camera_message = input_DDS_Camera.samples.getString(sample, "Camera")

    # Temp1 Connectivity
    for i in range(input_DDS_temp_extreme.samples.getLength()):
        if input_DDS_temp_extreme.infos.isValid(i):
            temp1_message = input_DDS_temp_extreme.samples.getNumber(i, "Tempsensor1_extreme")
            update_series(temp1_series, temp1_message)

    # Temp2 Connectivity
    for i in range(input_DDS_temp2_extreme.samples.getLength()):
        if input_DDS_temp2_extreme.infos.isValid(i):
            temp2_message = input_DDS_temp2_extreme.samples.getNumber(i, "Tempsensor2_extreme")
            update_series(temp2_series, temp2_message)

    # Actuator Status Connectivity
    for i in range(input_DDS_actuator_status.samples.getLength()):
        if input_DDS_actuator_status.infos.isValid(i):
            actuator_status_message = input_DDS_actuator_status.samples.getString(i, "ActuatorStatus")
            update_series(actuator_status_series, actuator_status_message)

    # Actuator2 Status Connectivity
    for i in range(input_DDS_actuator2_status.samples.getLength()):
        if input_DDS_actuator2_status.infos.isValid(i):
            actuator2_status_message = input_DDS_actuator2_status.samples.getString(i, "Actuator2Status")
            update_series(actuator2_status_series, actuator2_status_message)

    # Print Log
    print("-------------------------------------------")
    print(f'Camera: {camera_message}')
    print(f'Actuator 1 Status: {actuator_status_series}')
    print(f'Actuator 2 Status: {actuator2_status_series}')
    print(f'Thermometer 1: {temp1_series}')
    print(f'Thermometer 2: {temp2_series}')
