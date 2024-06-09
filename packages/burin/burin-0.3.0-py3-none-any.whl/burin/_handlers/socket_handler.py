"""
Burin Socket Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import pickle
import socket
import struct
import time

# Burin imports
from .handler import BurinHandler


class BurinSocketHandler(BurinHandler):
    """
    A handler that writes pickled log records to a network socket.

    .. note::

        This has a change from the :class:`logging.handlers.SocketHandler` that
        may be incompatible depending on the receiver's Python version.

        The default pickle protocol version used is **4** instead of **1**;
        this can be configured though by the *pickleProtocol* parameter which
        was added.

    The pickled data that is sent is just of the log records attribute
    dictionary (*__dict__*) so it can process the event in any way it needs and
    doesn't require Burin to be installed.

    The :func:`make_log_record` function can be used on the receiving end to
    recreate the log record from the pickled data if desired.
    """

    def __init__(self, host, port, pickleProtocol=4, level="NOTSET"):
        """
        This will set the *host* and *port* for the socket to connect to.

        :param host: The address of the host to communicate with.
        :type host: str
        :param port: The port to communicate on.
        :type port: int
        :param pickleProtocol: The pickle protocol version to use.  (Default =
                               4)
        :type pickleProtocol: int
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)
        self.host = host
        self.port = port
        self.pickleProtocol = pickleProtocol

        if port is None:
            self.address = host
        else:
            self.address = (host, port)

        self.sock = None
        self.closeOnError = False
        self.retryTime = None

        # Retry parameters for backing off
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    def close(self):
        """
        Closes and handler and the socket.
        """

        with self.lock:
            sock = self.sock

            if sock:
                self.sock = None
                sock.close()

            BurinHandler.close(self)

    def create_socket(self):
        """
        Tries creating the socket.

        If creation of the socket fails this will use a progressively greater
        period of time to retry creation up to
        :attr:`BurinSocketHandler.retryMax` (default 30 seconds).
        """

        now = time.time()

        attempt = True if self.retryTime is None else (now >= self.retryTime)

        if attempt:
            try:
                self.sock = self.make_socket()
                self.retryTime = None
            except OSError:
                # Socket creation failed, determine retry time
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod *= self.retryFactor

                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax

                self.retryTime = now + self.retryPeriod

    def emit(self, record):
        """
        Emits a log record.

        This will pickle the record and then send it through the socket.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            pickledRecord = self.make_pickle(record)
            self.send(pickledRecord)
        except Exception:
            self.handle_error(record)

    def handle_error(self, record):
        """
        Handles errors which may occur during an *emit()* call.

        This wile close the socket if *self.closeOnError*=**True**; it then
        calls :meth:`BurinHandler.handle_error` to continue with the error
        handling.

        :param record: The log record that was being processed when the error
                       occurred.
        :type record: BurinLogRecord
        """

        if self.closeOnError and self.sock:
            self.sock.close()
            self.sock = None
        else:
            BurinHandler.handle_error(self, record)

    def make_pickle(self, record):
        """
        Pickles the record in a binary format.

        This prepares the record for transmission across the socket.

        :param record: The log record to pickle.
        :type record: BurinLogRecord
        :returns: The pickled representation of the record.
        :rtype: bytes
        """

        # If there is exception info then get the traceback text into exc_text
        if record.exc_info:
            self.format(record)

        recordDict = dict(record.__dict__)
        recordDict["msg"] = record.get_message()
        recordDict["args"] = None
        recordDict["kwargs"] = None
        recordDict["exc_info"] = None

        # Python issue #25685: delete message as it's redundant with msg
        recordDict.pop("message", None)

        # Get pickled record and the lenth prefix
        recordBytes = pickle.dumps(recordDict, self.pickleProtocol)
        recordLength = struct.pack(">L", len(recordBytes))

        return recordLength + recordBytes

    def make_socket(self, timeout=1):
        """
        Makes the socket that is used for the connection.

        If :attr:`BurinSocketHandler.port` is not **None** then this will make
        a TCP socket, otherwise it will create a UNIX socket.

        :param timeout: The timeout to configure for the socket.
        :type timeout: int
        :returns: The socket that was created.
        :rtype: socket.socket
        :raises OSError: If making a UNIX socket fails.
        """

        if self.port is not None:
            sock = socket.create_connection(self.address, timeout=timeout)
        else:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            try:
                sock.connect(self.address)
            except OSError:
                sock.close()
                raise

        return sock

    def send(self, pickledRecord):
        """
        Sends the specified pickled record to the socket.

        .. note::

            The parameter for this has been renamed from *s* to *pickledRecord*
            compared to :meth:`logging.handlers.SocketHandler.send`.  This is
            not a keyword arg and therefore this shouldn't have an impact on
            any functionality.

        This will try to create the socket before sending if it hasn't been
        made yet.

        :param pickledRecord: The pickled log record to send over the socket.
        :type pickledRecord: bytes
        """

        if self.sock is None:
            self.create_socket()

        if self.sock is not None:
            try:
                self.sock.sendall(pickledRecord)
            except OSError:
                self.sock.close()
                self.sock = None

    # Aliases for better compatibility to replace standard library logging
    createSocket = create_socket
    handleError = handle_error
    makePickle = make_pickle
    makeSocket = make_socket
