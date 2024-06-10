import smtplib, ssl, logging

from credentials import get_creds

CREDS = get_creds()


#################################################################################
# Sent a MIME email object to its recipient using GMail
#################################################################################
def sendMIMEmessage(MIMEmessage):
    if not "@" in MIMEmessage["To"]:
        raise ValueError("Message doesn't have a sane destination address")

    MIMEmessage["From"] = "Asmbly AdminBot"

    logging.debug(
        f"""Sending email subject "{MIMEmessage['Subject']}" to {MIMEmessage['To']}"""
    )

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(CREDS.gmail_user, CREDS.gmail_pass)
            server.sendmail(
                CREDS.gmail_user, MIMEmessage["To"], MIMEmessage.as_string()
            )
    except:
        logging.exception(
            f"""Failed sending email subject "{MIMEmessage['Subject']}" to {MIMEmessage['To']}"""
        )
