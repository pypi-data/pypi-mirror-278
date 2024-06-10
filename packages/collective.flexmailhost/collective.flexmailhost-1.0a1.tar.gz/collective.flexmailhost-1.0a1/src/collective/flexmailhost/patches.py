from zope.sendmail.mailer import SMTPMailer
from zope.sendmail.mailer import _SMTPState


def default_init(
    self,
    hostname="localhost",
    port=25,
    username=None,
    password=None,
    no_tls=False,
    force_tls=False,
):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    self.force_tls = force_tls
    self.no_tls = no_tls
    self._smtp = _SMTPState()
    print("repatched SMTPMailer")


def apply_patches():
    SMTPMailer.__init__ = default_init
