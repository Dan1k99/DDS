import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::Example_sub",  filepath + "/DDS.xml")
input_DDS = connector.getInput("MySubscriber::MyReader")

while True:
    input_DDS.take()
    numOfSamples = input_DDS.samples.getLength()
    print(f'numOfSamples: {numOfSamples}')
    for j in range(0, numOfSamples):
        if input_DDS.infos.isValid(j):
            some_number = input_DDS.samples.getNumber(j, "NumberMember")
            some_string = input_DDS.samples.getString(j, "StingMember")
            print(f'Received Example: {some_number}, Status: {some_string}')
    sleep(1)



