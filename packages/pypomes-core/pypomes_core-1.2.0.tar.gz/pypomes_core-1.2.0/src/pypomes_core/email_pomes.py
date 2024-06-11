import sys
from email.message import EmailMessage
from logging import Logger
from smtplib import SMTP
from typing import Final
from .env_pomes import APP_PREFIX, env_get_str, env_get_int

EMAIL_ACCOUNT: Final[str] = env_get_str(key=f"{APP_PREFIX}_EMAIL_ACCOUNT")
EMAIL_PWD: Final[str] = env_get_str(key=f"{APP_PREFIX}_EMAIL_PWD")
EMAIL_PORT: Final[int] = env_get_int(key=f"{APP_PREFIX}_EMAIL_PORT")
EMAIL_SERVER: Final[str] = env_get_str(key=f"{APP_PREFIX}_EMAIL_SERVER")


def email_send(errors: list[str] | None,
               user_email: str,
               subject: str,
               content: str,
               logger: Logger = None) -> None:
    """
    Send email to *user_email", with *subject* as the email subject, and *content* as the email message.

    :param errors: incidental error messages
    :param user_email: the address to send the email to
    :param subject: the email subject
    :param content: the email message
    :param logger: optional logger
    """
    # import needed function
    from .exception_pomes import exc_format

    # build the email object
    email_msg = EmailMessage()
    email_msg.set_content(content)
    email_msg["Subject"] = subject
    email_msg["From"] = EMAIL_ACCOUNT
    email_msg["To"] = user_email

    # instanciate the email server
    server = SMTP(host=EMAIL_SERVER,
                  port=EMAIL_PORT)
    server.starttls()
    server.login(user=EMAIL_ACCOUNT,
                 password=EMAIL_PWD)

    # send the message
    try:
        server.send_message(msg=email_msg)
        server.quit()
        if logger:
            logger.debug(msg=f"Sent email {subject} to {user_email}")
    except Exception as e:
        # the operatin raised an exception
        exc_err: str = exc_format(exc=e,
                                  exc_info=sys.exc_info())
        err_msg: str = f"Error sending the email: {exc_err}"
        if logger:
            logger.error(msg=err_msg)
        if isinstance(errors, list):
            errors.append(err_msg)
