#!/usr/bin/env python3

import numpy

import cepton_sdk
from common import *


def on_image_frames(serial_number, image_points):
    print("Received {} points from sensor {}".format(
        len(image_points), serial_number))


if __name__ == "__main__":
    # Initialize
    cepton_sdk.initialize(capture_path=get_sample_capture_path())
    sensors_dict = cepton_sdk.get_sensors()
    sensor = next(iter(sensors_dict.values()))

    callback_id = cepton_sdk.listen_image_frames(on_image_frames)
    cepton_sdk.wait(0.1)
    cepton_sdk.unlisten_image_frames(callback_id)

    # Get next frames for all sensors. Wait until data is available.
    listener = cepton_sdk.ImageFramesListener()
    image_points_dict = listener.get_points()
    del listener

    # Get next frames for single sensor. Wait until data is available.
    listener = cepton_sdk.SensorImageFramesListener(sensor.serial_number)
    image_points_list = listener.get_points()
    del listener

    # Get large chunk of data
    listener = cepton_sdk.ImageFramesListener()
    cepton_sdk.wait(10)
    image_points_dict = listener.get_points()
    del listener
    image_points = cepton_sdk.combine_points(
        image_points_dict[sensor.serial_number])
    print("Received {} seconds of data from sensor {}".format(
        numpy.ptp(image_points.timestamps), sensor.serial_number))