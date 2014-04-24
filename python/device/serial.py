__author__ = 'nick'

# This file is to manage an arduino device connected to the serial port

import logging

import serial
from device.message import Message


# Setup module-wide logger
logger = logging.getLogger(__name__)


class DeviceSerial:
    def __init__(self, device_id, serial_port):
        logger = logging.getLogger(self.__class__.__name__)
        logger.info('Connecting to arduino device at %s' % ( serial_port ))

        self.device_id = device_id
        self.message_count = 0
        self.arduino = serial.Serial(serial_port, 9600)
        self.str_buffer = ''
        self.message_buffer = []

        logger.debug('Waiting until device is writeable')
        while (not self.arduino.writable()):
            pass

        logger.info('Device indicated that it is ready')


    def message_waiting(self):
        self.__fill_buffers()
        return len(self.message_buffer)


    def receive_message(self):
        """Gets the latest message from the buffer

         @rtype: device.message.Message
        """
        if self.message_waiting():
            message = self.message_buffer.pop()
            return message
        else:
            logger.warning('No messages in buffer, check message_waiting first')
            return None

    def send_message(self, data, type=""):
        message = Message()

        message.device_id = self.device_id

        message.message_id = self.message_count
        self.message_count += 1

        message.type = type

        message.data = data

        message_str = message.to_serial_string()

        logger.debug('Created message string to send: %s' % (repr(message_str)))

        self.arduino.write(message_str.encode('ascii'))


    def __fill_buffers(self):
        """Adds any data from serial device to the buffer"""
        # Fill up the bytes buffer furst.
        if self.arduino.inWaiting():
            while self.arduino.inWaiting():
                self.str_buffer += self.arduino.read().decode('ascii')

        # Check bytes buffer if there are any messages in it
        while self.str_buffer.count(Message.END) > 0:
            ( message_bytes, self.str_buffer) = self.str_buffer.split(Message.END, 1)
            message_bytes += Message.END
            logger.debug('Checking if message in: %s' % (repr(message_bytes)))
            if (Message.is_message(message_bytes)):
                logger.info('message is valid, generating and adding to message_buffer')
                message = Message(message_bytes)
                logger.debug('message data: %s' % (vars(message)))
                self.message_buffer.append(message)
            else:
                logger.warning('Received malformed message, throwing away and trying next one')



