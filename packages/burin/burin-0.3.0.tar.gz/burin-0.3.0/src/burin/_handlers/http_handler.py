"""
Burin HTTP Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import base64
import urllib.parse

# Burin imports
from .handler import BurinHandler


allowedMethods = ["GET", "POST"]


class BurinHTTPHandler(BurinHandler):
    """
    A handler that can send log records over HTTP to a Web server.

    .. note::

        This has the :meth:`BurinHTTPHandler.get_connection` method (also
        aliased as :meth:`BurinHTTPHandler.getConnection`); this was added to
        the standard library in Python 3.9 but is available here for all Python
        versions supported by Burin.
    """

    def __init__(self, host, url, method="GET", secure=False, credentials=None,
                 context=None, level="NOTSET"):
        """
        This will setup the handler and do some basic checks of parameters.

        Only 'GET' or 'POST' are allowed as *method*.  Also *context* must be
        **None** if *secure* is **False**.

        :param host: The host to connect to; this can be in the form of
                     'host:port' if non-standard HTTP/HTTPS ports are to be
                     used.
        :type host: str
        :param url: The URL path on the host to use.
        :type url: str
        :param method: The HTTP method to use for the request.  This must be
                       either 'GET' or 'POST'.  (Default = 'GET')
        :type method: str
        :param secure: Whether to use HTTPS or not.  (Default = **False**)
        :type secure: bool
        :param credentials: If authentication is needed for the host then this
                            should be a 2-tuple of (username, password).  This
                            will be placed into an HTTP 'Authorization' header
                            for Basic Authentication support.  If this is used
                            you should also use *secure*=**True** so that the
                            username and password are not sent in cleartext to
                            the host.
        :type credentials: tuple(str, str)
        :param context: A :class:`ssl.SSLContext` instance to configured
                        settings for an HTTPS connection.  This must be
                        **None** if *secure*=**False**.
        :type context: ssl.SSLContext
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        :raises ValueError: If *method* is not 'GET' or 'POST', or *context* is
                            not **None** and *secure*=**False**.
        """

        BurinHandler.__init__(self, level=level)

        method = method.upper()
        if method not in allowedMethods:
            raise ValueError(f"method must be one of {', '.join(allowedMethods)}")

        if not secure and context is not None:
            raise ValueError("context parameter cannot be used if secure=False")

        self.context = context
        self.credentials = credentials
        self.host = host
        self.method = method
        self.secure = secure
        self.url = url

    def emit(self, record):
        """
        Emits a log record.

        This will send the record to a web server using a percent-encoded
        dictionary.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            host = self.host
            connection = self.get_connection(host, self.secure)
            url = self.url
            data = urllib.parse.urlencode(self.map_log_record(record))

            if self.method == "GET":
                separator = "&" if url.find("?") >= 0 else "?"
                url = f"{url}{separator}{data}"

            connection.putrequest(self.method, url)

            if self.method == "POST":
                connection.putheader("Content-type", "application/x-www-form-urlencoded")
                connection.putheader("Content-length", str(len(data)))

            if self.credentials:
                authCreds = f"{self.credentials[0]}:{self.credentials[1]}".encode("utf-8")
                authEncoded = base64.b64encode(authCreds).strip().decode("ascii")
                connection.putheader("Authorization", f"Basic {authEncoded}")

            connection.endheaders()
            if self.method == "POST":
                connection.send(data.encode("utf-8"))
            connection.getresponse()
        except Exception:
            self.handle_error(record)

    def get_connection(self, host, secure):
        """
        Gets the HTTP or HTTPS connection.

        This can be overridden to change how the connection is created; for
        example if a proxy is required.

        .. note::

            In Python 3.9 :class:`logging.handlers.HTTPHandler` added this
            undocumented method.  It is available here for all versions of
            Python compatible with Burin (including versions below 3.9).

        :param host: The host to connect to.
        :type host: str
        :param secure: Whether to use HTTPS or not.
        :type secure: bool
        :returns: The connection object.
        :rtype: http.client.HTTPConnection | http.client.HTTPSConnection
        """

        import http.client
        if secure:
            connection = http.client.HTTPSConnection(host, context=self.context)
        else:
            connection = http.client.HTTPConnection(host)

        return connection

    def map_log_record(self, record):
        """
        Default mapping of log record to dictionary for CGI data.

        This can be overridden in subclasses to customise the record map
        format.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        :returns: A map of the record properties and values.
        :rtype: dict{str: Any}
        """

        return record.__dict__

    # Aliases for better compatibility to replace standard library logging
    getConnection = get_connection
    mapLogRecord = map_log_record
