#!/usr/bin/env python


########################################################################################################################


def get_html_table(header, rows):
    html_table = f"""<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color : Teal; color: White'>
"""
    for h in header:
        html_table += f"""        <th>{h}</th>
"""

    html_table += f"""    </tr>
    </thead>
    <tbody>
{rows}    </tbody>
</table>
"""
    return html_table


def get_html_row(row):
    html_row = f"    <tr>"
    for item in row:
        html_row += f"""
        <td>{item}</td>"""
    html_row += """
    </tr>"""
    if row:
        return html_row


class Report(object):
    def __init__(self, certs, warning, critical,
                 ok_symbol=":white_check_mark:",
                 error_symbol=":no_entry:",
                 warning_symbol=":warning:",
                 critical_symbol=":bangbang:",
                 expired_symbol=":rotating_light:",
                 skip_ok=False, title="SSL certificates report",
                 html=False):
        self.certs = certs
        self.warning = warning
        self.critical = critical
        self.skip_ok = skip_ok
        self.title = title
        self.html = html
        self.ok_symbol = ok_symbol
        self.error_symbol = error_symbol
        self.warning_symbol = warning_symbol
        self.critical_symbol = critical_symbol
        self.expired_symbol = expired_symbol
        self.report = []
        self.html_header = ["Status", "SSL Cert", "Message", "Expiration date"]
        self.html_rows = ""

    def gen_report(self):
        for c in self.certs:
            name = c.get("name")
            expire_date = c.get("notAfter")
            days = c.get("expire_age")
            error_message = c.get("error_message")
            if error_message:
                row = f"{self.error_symbol} *{name}* - {error_message}"
                html_row = ["Error!", name, error_message, "-"]

            elif not error_message and isinstance(days, int) and days < 0:
                msg = f" Will expire in {abs(days)} days"
                row = f"*{name}* - {msg} ({expire_date})."
                html_row = [name, msg, expire_date]

                if abs(days) <= self.critical:
                    row = f"{self.critical_symbol} {row}"
                    html_row = ["CRITICAL"] + html_row
                elif self.warning >= abs(days) > self.critical:
                    row = f"{self.warning_symbol} {row}"
                    html_row = ["Warning"] + html_row
                elif self.skip_ok:
                    continue
                else:
                    html_row = ["OK"] + html_row
                    row = f"{self.ok_symbol} {row}"

            elif not error_message and isinstance(days, int) and days >= 0:
                msg = f"* Has already expired. Expired {abs(days)} days ago."
                row = f"*{name}* - {msg} ({expire_date})."
                html_row = [name, msg, expire_date]
                if abs(days) <= self.critical:
                    row = f"{self.expired_symbol} {row}"
                    html_row = ["EXPIRED!!"] + html_row
            else:
                row = f"Unknown state for cert **{name}**."
                html_row = ["Unknown", name, "-", "-"]

            if self.html and html_row:
                row = get_html_row(html_row)

            if row:
                self.report.append((days, row))

    def get_report(self):
        rows = ""

        for e in sorted(self.report, reverse=True):
            rows += f"{e[-1]}\n"

        if rows and self.html:
            return self.title, get_html_table(self.html_header, rows)

        if rows:
            return f"*{self.title}*\n{rows}"

        if self.html:
            return None, None
