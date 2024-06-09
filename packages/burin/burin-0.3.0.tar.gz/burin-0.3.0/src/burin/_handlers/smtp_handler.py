"""
Burin SMTP Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from datetime import datetime
from email.message import EmailMessage
import smtplib
from ssl import SSLContext

# Burin imports
from .handler import BurinHandler


class BurinSMTPHandler(BurinHandler):
    """
    A handler that can send emails over SMTP for logging events.

    This requires an email server that you have permission to send emails
    through; it cannot be used standalone to send directly to a receiving
    server.
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None,
                 secure=None, timeout=5.0, level="NOTSET"):
        """
        This will initialize the handler for sending emails.

        The standard SMTP port from :const:`smtplib.SMTP_PORT` is used by
        default; if you need to use a non-standard port then *mailhost* must be
        a tuple in the form of *(host, port)*.

        You can send to multiple recipients by passing a list of addresses to
        *toaddrs*.

        If your SMTP server requires authentication then *credentials* should
        be a list or tuple in the form of *(username, password)*.  If you are
        sending credentials then *secure* should not be **None** to prevent
        them being sent unencrypted.

        .. note::

            Unlike the standard :class:`logging.handlers.SMTPHandler` you can
            use *secure* even without credentials.  This will at least send
            the message over a connection using STARTTLS.

            Also burin allows *secure* to be a :class:`ssl.SSLContext` instead
            of just a tuple with optional *keyfile* and *certfile* as these are
            deprecated in the :meth:`smtplib.SMTP.starttls` call.

        :param mailhost: The SMTP server to connect to and send mail through.
                         By default the standard SMTP port is used; if you need
                         to use a custom port this should be a tuple in the
                         form of *(host, port)*.
        :type mailhost: str | tuple(str, int)
        :param fromaddr: The address that the email is sent from.
        :type fromaddr: str
        :param toaddrs: The recipient email addresses.  This can be a single
                        address or a list of multiple addresses.
        :type toaddrs: list[str] | str
        :param subject: The subject line of the email.
        :type subject: str
        :param credentials: If the SMTP server requires authentication you can
                            pass a tuple here in the form
                            *(username, password)*.
        :type credentials: tuple(str, str)
        :param secure: If this is set to a tuple or a :class:`ssl.SSLContext`
                       it will enable STARTTLS encryption for the connection to
                       the SMTP server.  It is recommended to use a
                       :class:`ssl.SSLContext` as the *keyfile* and *certfile*
                       params for :meth:`smtplib.SMTP.starttls` are deprecated.
                       However, If using a tuple it can follow one of three
                       forms, an empty tuple *()*, a single value tuple with
                       the name of a keyfile *(keyfile,)*, or a 2-value tuple
                       with the names of a keyfile and certificate file
                       *(keyfile, certfile)*.  This is then passed to
                       :meth:`smtplib.SMTP.starttls`.
        :type secure: tuple
        :param timeout: A timeout (in seconds) for communications with the SMTP
                        server.
        :type timeout: float | int
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)

        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost = mailhost
            self.mailport = None

        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None

        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.fromaddr = fromaddr
        self.secure = secure
        self.subject = subject
        self.timeout = timeout

    def emit(self, record):
        """
        Emits a log record.

        This will format the log record, prepare the email message, and then
        send the message.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        # Create the message
        msg = EmailMessage()
        msg["From"] = self.fromaddr
        msg["To"] = ",".join(self.toaddrs)
        msg["Subject"] = self.getSubject(record)
        msg["Date"] = datetime.now().astimezone()
        msg.set_content(self.format(record))

        port = self.mailport if self.mailport is not None else smtplib.SMTP_PORT

        try:
            # Connect to the host
            smtp = smtplib.SMTP(self.mailhost, port, timeout=self.timeout)

            # Use TLS set to be used
            if self.secure is not None:
                smtp.ehlo()
                if isinstance(self.secure, SSLContext):
                    smtp.starttls(context=self.secure)
                else:
                    smtp.starttls(*self.secure)
                smtp.ehlo()


            # Login if credentials were provided
            if self.username is not None:
                smtp.login(self.username, self.password)

            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handle_error(record)

    def get_subject(self, record): # noqa: ARG002
        """
        Gets the subject for the mail.

        This just returns the *subject* value; however this class can be
        overridden to determine subject based on the record.

        :param record: The log record being handled.  This is not used in this
                       basic method implementation.
        :type record: BurinLogRecord
        :returns: The subject for the mail.
        :rtype: str
        """

        return self.subject

    # Aliases for better compatibility to replace standard library logging
    getSubject = get_subject
