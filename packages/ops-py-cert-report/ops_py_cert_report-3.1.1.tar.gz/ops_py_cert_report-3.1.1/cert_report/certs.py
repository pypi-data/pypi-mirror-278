#!/usr/bin/env python

import ssl
import socket
import logging
from datetime import datetime


########################################################################################################################


def set_timestamp(fmt, s):
    """Returns a date object of a string in the provided format (fmt).

    The string has to be in the correct format, if not None is returned."""

    try:
        ts = datetime.strptime(str(s.strip()), fmt)
    except ValueError:
        logging.error(f"Unable to convert provided argument '{str(s)}' to timestamp object")
        return

    return ts


class Certs(object):
    def __init__(self, hostnames):
        self.hostnames = hostnames
        self.date_format = "%b %d %H:%M:%S %Y"
        self.now = datetime.now()
        self.slack_report = []
        self.certs = []

    def parse_certs(self):
        for c in self.hostnames:
            self.ssl_cert_expire(c)

    def ssl_cert_expire(self, crt):
        c = {"name": crt}
        context = ssl.create_default_context()

        with socket.create_connection((crt, 443)) as sock:
            try:
                with context.wrap_socket(sock, server_hostname=crt) as s:
                    s.do_handshake()
                    cert = s.getpeercert()
                    not_after = cert.get("notAfter")
                    ts = set_timestamp(self.date_format, not_after.rstrip("GMT"))
                    age = (self.now - ts).days
                    c["notAfter"] = not_after
                    c["expire_ts"] = ts
                    c["expire_age"] = age
            except ssl.SSLCertVerificationError as e:
                c["error_message"] = e.verify_message
                c["expire_age"] = 999999
            finally:
                self.certs.append(c)

            return

    def get_certs(self):
        return self.certs
