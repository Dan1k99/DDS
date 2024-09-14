import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep

# Set the filepath to the directory of this script
filepath = osPath.dirname(osPath.realpath(__file__))

# Configure connection
connector = rti.Connector("MyParticipantLibrary::Actuator2", filepath + "/DDS.xml")

# Configure all Inputs (Subscribers of Actuator)
input_DDS_button = connector.getInput("Actuator2::Actuator_button")
input_DDS_temp2 = connector.getInput("Actuator2::Actuator_Tempsensor2")

# Configure all Outputs (Publishers of Actuator)
output_DDS_actuator_status = connector.getOutput("actuator_publisher21::status_writer")
output_DDS_temp_extreme = connector.getOutput("actuator_publisher22::temp_extreme_writer")

# Initialize parameters
button_state = 1  # Default to start
actuator_status_list = ["Working", "Degraded", "Stopped"]
status_index = 0  # Will decide the actuator's status
temp2_message = 0
temp2_status = False

def get_temp_status(num_samples):
    """This function returns True if the temp sensor is functioning, False otherwise."""
    return num_samples > 0  # If no samples, it means the temp sensor is not running

while True:
    sleep(1)  # Sleep for 1 second

    # Take the data from the button input
    input_DDS_button.take()
    num_samples_button = input_DDS_button.samples.getLength()
    for i in range(num_samples_button):
        if input_DDS_button.infos.isValid(i):
            button_state = input_DDS_button.samples.getNumber(i, 'Button')

    # Update the actuator status based on the button state
    if button_state == 0:  # Received stop from StartStop
        if status_index in [0, 1]:
            status_index = 2
    elif button_state == 1 and status_index == 2:  # Received start from StartStop
        status_index = 0

    if status_index != 2:  # If actuator is working, connect to all sensors
        input_DDS_temp2.take()
        num_samples_temp2 = input_DDS_temp2.samples.getLength()

        # Receive all temperature information
        for i in range(num_samples_temp2):
            if input_DDS_temp2.infos.isValid(i):
                temp2_message = input_DDS_temp2.samples.getNumber(i, "Temp")

        temp2_status = get_temp_status(num_samples_temp2)  # Check which temps are running

        # Checking for extreme temperatures
        if temp2_status:
            if temp2_message > 45:
                output_DDS_temp_extreme.instance.setNumber("Tempsensor2_extreme", temp2_message)
                output_DDS_temp_extreme.write()  # Send the extreme temps to the dashboard
                status_index = 1
            else:
                status_index = 0

    # Print the current actuator status
    print(f'Actuator status: {actuator_status_list[status_index]}')

    # Publish the current actuator status
    output_DDS_actuator_status.instance.setString("Actuator2Status", actuator_status_list[status_index])
    output_DDS_actuator_status.write()
