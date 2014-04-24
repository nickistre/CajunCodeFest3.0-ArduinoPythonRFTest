__author__ = 'nick'


class Message:
    DELIM = '|'
    END = "\n"

    def __init__(self, message_str=None):
        """Class constructor to create message from bytes

        @type message_str: str
        """
        self.device_id = None
        self.message_id = None
        self.type = ''
        self.data = ''

        if isinstance(message_str, str) and Message.is_message(message_str):
            # Retrieve message parts from bytes passed in
            parts = Message.__split_message(message_str)
            if (parts != None):
                (self.device_id, self.message_id, self.type, self.data) = parts

    def to_serial_string(self):
        message_str = "%(device_id)d%(delim)s%(message_id)d%(delim)s%(type)s%(delim)s%(data)s%(end)s" % {
            'delim': Message.DELIM,
            'end': Message.END,

            'device_id': self.device_id,
            'message_id': self.message_id,
            'type': self.type,
            'data': self.data
        }
        return message_str

    @staticmethod
    def __split_message(received_str):
        """Checks if the string is a valid message (or has one in it)

        A valid message starts with an number, the delimiter, a message id, a second delimiter, a type string,
        third delimiter, then finally the data itself, ending with a new line.

        @type received_str: str
        """

        # Check for newline
        if not "\n" in received_str:
            return None

        # Remove newline
        received_str = received_str[:received_str.find("\n")]
        parts = received_str.split(Message.DELIM, 3)
        if len(parts) != 4:
            return None

        ( device_id_str, message_id_str, type, data ) = parts

        #logger.debug('Parsed out data - device_id: %s, message_id: %s, type: "%s", data: "%s"' % (device_id, message_id, type, data))

        # Check that device_id is int
        try:
            device_id = int(device_id_str)
        except ValueError:
            return None

        # Check that message_id is int
        try:
            message_id = int(message_id_str)
        except ValueError:
            return None

        return (device_id, message_id, type, data)

    @staticmethod
    def is_message(message_str):
        parts = Message.__split_message(message_str)
        return parts != None