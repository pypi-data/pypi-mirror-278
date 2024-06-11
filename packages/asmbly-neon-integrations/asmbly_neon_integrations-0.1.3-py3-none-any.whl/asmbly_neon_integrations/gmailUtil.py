import smtplib, ssl, logging

from asmbly_neon_integrations.credentials import GmailCredentials


#################################################################################
# Sent a MIME email object to its recipient using GMail
#################################################################################
def sendMIMEmessage(MIMEmessage, creds: GmailCredentials):
    if not "@" in MIMEmessage["To"]:
        raise ValueError("Message doesn't have a sane destination address")

    MIMEmessage["From"] = "Asmbly AdminBot"

    logging.debug(
        f"""Sending email subject "{MIMEmessage['Subject']}" to {MIMEmessage['To']}"""
    )

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(creds.username, creds.password)
            server.sendmail(creds.username, MIMEmessage["To"], MIMEmessage.as_string())
    except:
        logging.exception(
            f"""Failed sending email subject "{MIMEmessage['Subject']}" to {MIMEmessage['To']}"""
        )
