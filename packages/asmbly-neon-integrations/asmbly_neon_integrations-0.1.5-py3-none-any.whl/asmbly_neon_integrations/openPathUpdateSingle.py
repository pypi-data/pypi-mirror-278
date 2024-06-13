###############################################################################
# Fetch all member records from Neon and update OpenPath as necessary for all
# * Run me at least once a day to catch subscription expirations

import logging

from asmbly_neon_integrations import neonUtil, openPathUtil

from asmbly_neon_integrations.credentials import (
    AltaCredentials,
    GmailCredentials,
    NeonCredentials,
)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def openPathUpdateSingle(
    alta_creds: AltaCredentials,
    gmail_creds: GmailCredentials,
    neon_creds: NeonCredentials,
    neonID,
):
    account = neonUtil.getMemberById(neonID, credentials=neon_creds)
    if account.get("OpenPathID"):
        openPathUtil.updateGroups(
            creds=alta_creds, gmail_creds=gmail_creds, neonAccount=account
        )
        # note that this isn't necessarily 100% accurate, because we have Neon users with provisioned OpenPath IDs and no access groups
        # assuming that typical users who gained and lost openPath access have a signed waiver
    elif neonUtil.accountHasFacilityAccess(account):
        account = openPathUtil.createUser(
            alta_creds=alta_creds, neon_creds=neon_creds, neonAccount=account
        )
        openPathUtil.updateGroups(
            creds=alta_creds,
            gmail_creds=gmail_creds,
            neonAccount=account,
            openPathGroups=[],
        )  # pass empty groups list to skip the http get
        openPathUtil.createMobileCredential(creds=alta_creds, neonAccount=account)
    elif account.get("validMembership"):
        if not account.get("WaiverDate"):
            logging.info(
                "%s (%s) is missing the Waiver",
                account.get("fullName"),
                account.get("Email 1"),
            )
        if not account.get("FacilityTourDate"):
            logging.info(
                "%s (%s) is missing the Facility Tour",
                account.get("fullName"),
                account.get("Email 1"),
            )
