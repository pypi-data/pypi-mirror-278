"""
Burin Syslog Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import array
import socket

# Burin imports
from .handler import BurinHandler


# Default Syslog values
SYSLOG_UDP_PORT = 514


class BurinSyslogHandler(BurinHandler):
    """
    A handler that supports sending log records to a local or remote syslog.

    .. note::

        Unlike the standard library handler the 'l' in 'Syslog' of the class
        name is not capitalized so this class better matches the actual
        'Syslog' name.

        The *mapPriority* method and *priority_map* property from
        :class:`logging.handlers.SysLogHandler` is also not included as they
        have not been needed for mapping to lowercase levels for a while.
    """

    # These values are based on the standard library SysLogHandler which bases
    # them from syslog.h
    #
    # Syslog priorities and facilities are encoded together into a single
    # 32-bit value.  The lowest 3 bits are the priorities (0-7) and the highest
    # 28 bits are the facilities (0-268M+).

    # Priorities
    LOG_EMERG = 0  # System is unusable
    LOG_ALERT = 1  # Immediate action must be taken
    LOG_CRIT = 2  # Critical events
    LOG_ERR = 3  # Error events
    LOG_WARNING = 4  # Warning events
    LOG_NOTICE = 5  # Normal but significant events
    LOG_INFO = 6  # Informational
    LOG_DEBUG = 7  # Debug messages

    # Facilities (0-15 reserved for system use)
    LOG_KERN = 0  # Kernel
    LOG_USER = 1  # User-level
    LOG_MAIL = 2  # Email
    LOG_DAEMON = 3  # System daemons
    LOG_AUTH = 4  # Authorization/security
    LOG_SYSLOG = 5  # Syslog internal
    LOG_LPR = 6  # Line printer
    LOG_NEWS = 7  # Network news
    LOG_UUCP = 8  # UUCP
    LOG_CRON = 9  # Cron/clock
    LOG_AUTHPRIV = 10  # Private authorization/security
    LOG_FTP = 11  # FTP
    LOG_NTP = 12  # NTP
    LOG_SECURITY = 13  # Security audit
    LOG_CONSOLE = 14  # Console output
    LOG_SOLCRON = 15  # Solaris scheduler

    # Additional facilities
    LOG_LOCAL0 = 16
    LOG_LOCAL1 = 17
    LOG_LOCAL2 = 18
    LOG_LOCAL3 = 19
    LOG_LOCAL4 = 20
    LOG_LOCAL5 = 21
    LOG_LOCAL6 = 22
    LOG_LOCAL7 = 23

    priority_names = {
        "alert": LOG_ALERT,
        "crit": LOG_CRIT,
        "critical": LOG_CRIT,
        "debug": LOG_DEBUG,
        "emerg": LOG_EMERG,
        "err": LOG_ERR,
        "error": LOG_ERR,  # Deprecated
        "info": LOG_INFO,
        "notice": LOG_NOTICE,
        "panic": LOG_EMERG,  # Deprecated
        "warn": LOG_WARNING,  # Deprecated
        "warning": LOG_WARNING
    }

    facility_names = {
        "auth": LOG_AUTH,
        "authpriv": LOG_AUTHPRIV,
        "console": LOG_CONSOLE,
        "cron": LOG_CRON,
        "daemon": LOG_DAEMON,
        "ftp": LOG_FTP,
        "kern": LOG_KERN,
        "local0": LOG_LOCAL0,
        "local1": LOG_LOCAL1,
        "local2": LOG_LOCAL2,
        "local3": LOG_LOCAL3,
        "local4": LOG_LOCAL4,
        "local5": LOG_LOCAL5,
        "local6": LOG_LOCAL6,
        "local7": LOG_LOCAL7,
        "lpr": LOG_LPR,
        "mail": LOG_MAIL,
        "news": LOG_NEWS,
        "ntp": LOG_NTP,
        "security": LOG_SECURITY,
        "solaris-cron": LOG_SOLCRON,
        "syslog": LOG_SYSLOG,
        "user": LOG_USER,
        "uucp": LOG_UUCP
    }

    # Additional handling values
    append_nul = True
    ident = ""

    # Unix socket types to try if none are specified
    _unix_socktypes = (socket.SOCK_DGRAM, socket.SOCK_STREAM)


    def __init__(self, address=("localhost", SYSLOG_UDP_PORT),
                 facility=LOG_USER, socktype=None, level="NOTSET"):
        """
        This initializes the handler and sets it for sending to syslog.

        By default the handler will try to use a local syslog through UDP port
        514. To change this *address* must be set as a tuple in the form
        *(host, port)*; or to use a UNIX socket as a string that is a file
        system location.  A bytes-like object can also be used as this may
        represent addresses in Linux's abstract namespace.

        By default a UDP connection is created; if TCP is needed ensure
        *socktype* is set to :const:`socket.SOCK_STREAM`.

        :param address: The address to connect to syslog at.  This should be a
                        tuple in the form of *(host, port)* for an INET socket;
                        or for a UNIX socket a string to a filesystem path or a
                        bytes-like object (such as for Linux's abstract
                        namespace addresses).  (Default = ('localhost', 514))
        :type address: tuple(str, int) | str | bytes | bytearray | array.array
        :param facility: The syslog facility to use.  These are available as
                         class attributes on the handler to simplify usage.
                         (Default = 1 (LOG_USER))
        :type facility: int
        :param socktype: The socket type to use for the connection to syslog.
                         By default a :const:`socket.SOCK_DGRAM` socket is
                         used if this is **None**; for TCP connections specify
                         :const:`socket.SOCK_STREAM`.
        :type socktype: int
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)

        self.address = address
        self.facility = facility
        self.socktype = socktype
        self.socket = None

        self.create_socket()

    def close(self):
        """
        Closes the handler and the syslog socket.
        """

        with self.lock:
            if self.socket:
                socket = self.socket
                self.socket = None
                socket.close()
            BurinHandler.close(self)

    def create_socket(self):
        """
        Try to create a socket and, if not datagram, connect to the other end.

        This will be called automatically during initialization of the handler.
        If it fails to connect at this point it is not considered an error.
        The method will be called again when emitting an event if there is
        still no socket connected.

        .. note::

            In Python 3.11 :meth:`logging.handlers.SysLogHandler.createSocket`
            was added to the standard library; it is supported here for all
            versions of Python compatible with Burin (including versions below
            3.11).
        """

        address = self.address
        socktype = self.socktype

        if isinstance(address, (str, bytes, bytearray, array.array)):
            self.unixsocket = True

            # The syslog server may be unavailable during handler
            # initialization which can be ignored
            try:
                self._connect_unixsocket(address)
            except OSError:
                pass
        else:
            self.unixsocket = False

            if socktype is None:
                socktype = socket.SOCK_DGRAM

            host, port = address
            addrInfo = socket.getaddrinfo(host, port, 0, socktype)

            if not addrInfo:
                raise OSError("getaddrinfo returned an empty list")

            for addr in addrInfo:
                addrFam, socktype, addrProto, addrCanon, addrSock = addr
                err = sock = None

                try:
                    sock = socket.socket(addrFam, socktype, addrProto)

                    if socktype == socket.SOCK_STREAM:
                        sock.connect(addrSock)
                    break
                except OSError as exc:
                    err = exc

                    if sock is not None:
                        sock.close()

            if err is not None:
                raise err

            self.socket = sock
            self.socktype = socktype

    def emit(self, record):
        """
        Emits a log record to the Syslog socket.

        The log record will be formatted and sent to the Syslog server.  If
        exception information is present in the log record it will *NOT* be
        sent along to the server.

        .. note::

            If a socket connection was not established earlier this will
            attempt to create it again before emitting the record.  This
            functionality was added in the Python 3.11 standard library and is
            supported here for all versions of Python compatible with Burin
            (including versions below 3.11)

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            msg = self.format(record)
            if self.ident:
                msg = self.ident + msg
            if self.append_nul:
                msg += "\000"

            # Convert the level to lowercase for Syslog
            priority = f"{self.encodePriority(self.facility, record.levelname.lower())}"

            # Convert the message to bytes are required by RFX 5424
            priority = priority.encode("utf-8")
            msg = msg.encode("utf-8")
            msg = priority + msg

            if not self.socket:
                self.create_socket()

            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except Exception:
            self.handle_error(record)

    def encode_priority(self, facility, priority):
        """
        Encodes the facility and priority.

        Either strings or integers can be used for the facility and priority
        values, these will be mapped into the single 32-bit value used by
        Syslog.

        :param facility: The facility for Syslog to log the record as.
        :type facility: int | str
        :param priority: The priority for Syslog to log the record with.
        :type priority: int | str
        :returns: The single 32-bit value for Syslog encoded with the facility
                  and priority.
        :rtype: int
        """

        if isinstance(facility, str):
            facility = self.facility_names[facility]

        if isinstance(priority, str):
            priority = self.priority_names[priority]

        return (facility << 3) | priority

    # Aliases for better compatibility to replace standard library logging
    createSocket = create_socket
    encodePriority = encode_priority

    def _connect_unixsocket(self, address):
        """
        Tries to connect through a unix socket.

        :param address: The socket address to connect to.
        :type address: str | bytes
        :raises OSError: If there connecting to the socket failed.
        """

        # Use multiple socket types for fallback tries if none is specified
        trySocktypes = self._unix_socktypes if self.socktype is None else (self.socktype,)
        lastSocktype = trySocktypes[-1]

        for socktype in trySocktypes:
            self.socket = socket.socket(socket.AF_UNIX, socktype)

            try:
                self.socket.connect(address)

                # Connection was successful so save the socktype used
                self.socktype = socktype
            except OSError:
                self.socket.close()

                if socktype is lastSocktype:
                    raise
