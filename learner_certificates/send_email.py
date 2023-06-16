import argparse
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class BreakText:
    def __init__(self, text, max_characters=80):
        self._max = max_characters
        self._nchar = 0
        self._paragraph = ''
        self._line = []

        for word in text.split(' '):
            if len(word) > self._max:
                self._complete_line()
                self._paragraph += word
                self._append_newline()
                continue
            elif len(word) + self._nchar > self._max:
                self._complete_line()

            self._line.append(word)
            self._nchar += len(word)
            if word[-1] == '\n':
                self._complete_line()
        self._complete_line()

    @property
    def paragraph(self):
        return self._paragraph

    def _append_newline(self):
        if self._paragraph[-1] != '\n':
            self._paragraph += '\n'

    def _complete_line(self):
        if len(self._line) > 0:
            self._paragraph += ' '.join(self._line)
            self._append_newline()
            self._line = []
            self._nchar = 0


def create_email_msg(params, certificate, env):
    msg = MIMEMultipart()

    msg['Subject'] = "Certificate of Participation"
    msg['From'] = params["instructor_email"]
    msg['To'] = params["email"]

    template = env.get_template(params['badge'] + ".msg")
    content = BreakText(template.render(**params)).paragraph
    msg.attach(MIMEText(content, "plain"))

    with open(certificate, "rb") as f:
        attach = MIMEApplication(f.read(), subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment',
                      filename=str(certificate.name))
    msg.attach(attach)

    return msg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mail-server', default="localhost",
        help='the SMTP mail server')


if __name__ == '__main__':
    main()
