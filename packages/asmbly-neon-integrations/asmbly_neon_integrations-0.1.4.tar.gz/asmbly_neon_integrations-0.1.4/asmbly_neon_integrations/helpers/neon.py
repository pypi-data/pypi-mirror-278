import datetime

from asmbly_neon_integrations.credentials import NeonCredentials
from asmbly_neon_integrations.helpers.api import apiCall


N_BASE_URL = "https://api.neoncrm.com/v2"


###########################
#####   NEON EVENTS   #####
###########################


# Get list of custom fields for events
def getEventCustomFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/customFields"
    queryParams = "?category=Event"
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseEventFields = apiCall(httpVerb, url, data, credentials.headers).json()
    # print("### CUSTOM FIELDS ###\n")
    # pprint(responseFields)

    return responseEventFields


# Get list of event categories
def getEventCategories(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/properties/eventCategories"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseCategories = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseCategories


# Filter event categories to active only
def getEventActiveCategories(responseCategories):
    categories = list(filter(lambda cat: cat["status"] == "ACTIVE", responseCategories))

    return categories


# Get a list of active event category names
def getEventActiveCatNames(responseCategories):
    categories = []
    for cat in responseCategories:
        if cat["status"] == "ACTIVE":
            categories.append(cat["name"])

    return categories


# Get possible search fields for POST to /events/search
def getEventSearchFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/events/search/searchFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseSearchFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseSearchFields


# Get possible output fields for POST to /events/search
def getEventOutputFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/events/search/outputFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseOutputFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseOutputFields


# Post search query to get back events (only gets 200 events, pagination not currently supported)
def postEventSearch(searchFields, outputFields, credentials: NeonCredentials, page=0):
    httpVerb = "POST"
    resourcePath = "/events/search"
    queryParams = ""
    data = {
        "searchFields": searchFields,
        "outputFields": outputFields,
        "pagination": {"currentPage": page, "pageSize": 200},
    }

    url = N_BASE_URL + resourcePath + queryParams
    responseEvents = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvents


# Get registrations for a single event by event ID
def getEventRegistrants(eventId, credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = f"/events/{eventId}/eventRegistrations"
    queryParams = "?pageSize=30"
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    individualEvent = apiCall(httpVerb, url, data, credentials.headers).json()

    return individualEvent


# Get event registration count (SUCCEEDED status only) from "eventRegistrations" field in individual event
def getEventRegistrantCount(registrantList):
    count = 0
    if type(registrantList) is not type(None):
        for registrant in registrantList:
            status = registrant["tickets"][0]["attendees"][0]["registrationStatus"]
            if status == "SUCCEEDED":
                tickets = registrant["tickets"][0]["attendees"]
                count += len(tickets)

    return count


# Get individual accounts by account ID
def getAccountIndividual(acctId, credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = f"/accounts/{acctId}"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseAccount = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseAccount


# Get possible search fields for POST to /orders/search
def getOrderSearchFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/orders/search/searchFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseSearchFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseSearchFields


# Get possible output fields for POST to /events/search
def getOrderOutputFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/orders/search/outputFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseOutputFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseOutputFields


# Post search query to get back orders (only gets 200 events, pagination not currently supported)
def postOrderSearch(searchFields, outputFields, credentials: NeonCredentials):
    httpVerb = "POST"
    resourcePath = "/orders/search"
    queryParams = ""
    data = {
        "searchFields": searchFields,
        "outputFields": outputFields,
        "pagination": {"currentPage": 0, "pageSize": 200},
    }

    url = N_BASE_URL + resourcePath + queryParams
    responseEvents = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvents


# Get possible search fields for POST to /accounts/search
def getAccountSearchFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/accounts/search/searchFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseSearchFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseSearchFields


# Get possible output fields for POST to /events/search
def getAccountOutputFields(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = "/accounts/search/outputFields"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseOutputFields = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseOutputFields


# Post search query to get back orders (only gets 200 events, pagination not currently supported)
def postAccountSearch(searchFields, outputFields, credentials: NeonCredentials):
    httpVerb = "POST"
    resourcePath = "/accounts/search"
    queryParams = ""
    data = {
        "searchFields": searchFields,
        "outputFields": outputFields,
        "pagination": {"currentPage": 0, "pageSize": 200},
    }

    url = N_BASE_URL + resourcePath + queryParams
    responseEvents = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvents


def postEventRegistration(
    accountID, eventID, accountFirstName, accountLastName, credentials: NeonCredentials
):
    httpVerb = "POST"
    resourcePath = "/eventRegistrations"
    queryParams = ""
    data = {
        "id": "string",
        "payments": [
            {
                "id": "string",
                "amount": 0,
                "paymentStatus": "Succeeded",
                "tenderType": 0,
                "receivedDate": datetime.datetime.today().isoformat(),
            }
        ],
        "donorCoveredFeeFlag": False,
        "eventId": eventID,
        "donorCoveredFee": 0,
        "taxDeductibleAmount": 0,
        "sendSystemEmail": True,
        "registrationAmount": 0,
        "ignoreCapacity": False,
        "registrantAccountId": accountID,
        "tickets": [
            {
                "attendees": [
                    {
                        "attendeeId": 0,
                        "accountId": accountID,
                        "firstName": accountFirstName,
                        "lastName": accountLastName,
                        "markedAttended": True,
                        "registrantAccountId": accountID,
                        "registrationStatus": "SUCCEEDED",
                        "registrationDate": datetime.datetime.today().isoformat(),
                    }
                ]
            }
        ],
    }

    url = N_BASE_URL + resourcePath + queryParams
    responseEvents = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvents


def getAccountEventRegistrations(neonId, credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = f"/accounts/{neonId}/eventRegistrations"
    queryParams = "?sortColumn=registrationDateTime&sortDirection=DESC"
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseEvents = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvents


def getEvent(eventId, credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = f"/events/{eventId}"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseEvent = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseEvent


def cancelClass(registrationId, credentials: NeonCredentials):
    httpVerb = "PATCH"
    resourcePath = f"/eventRegistrations/{registrationId}"
    queryParams = ""
    data = {
        "tickets": [
            {
                "attendees": [
                    {
                        "registrationStatus": "CANCELED",
                    }
                ]
            }
        ]
    }

    url = N_BASE_URL + resourcePath + queryParams
    responseStatus = apiCall(httpVerb, url, data, credentials.headers)

    return responseStatus


def getEventTopics(credentials: NeonCredentials):
    httpVerb = "GET"
    resourcePath = f"/properties/eventTopics"
    queryParams = ""
    data = ""

    url = N_BASE_URL + resourcePath + queryParams
    responseTopics = apiCall(httpVerb, url, data, credentials.headers).json()

    return responseTopics


def eventTierCodePatch(classId, tier, credentials: NeonCredentials):
    httpVerb = "PATCH"
    resourcePath = f"/events/{classId}"
    queryParams = ""
    data = {"code": f"Tier {tier}"}

    url = N_BASE_URL + resourcePath + queryParams
    response = apiCall(httpVerb, url, data, credentials.headers)

    return response


def eventTimePatch(
    classId: str,
    credentials: NeonCredentials,
    eventStartTime: str = "hh:mm AM/PM",
    eventEndTime: str = "hh:mm AM/PM",
):
    httpVerb = "PATCH"
    resourcePath = f"/events/{classId}"
    queryParams = ""
    data = {"eventDates": {"startTime": eventStartTime, "endTime": eventEndTime}}

    url = N_BASE_URL + resourcePath + queryParams
    response = apiCall(httpVerb, url, data, credentials.headers)

    return response


def eventAttendeeCountPatch(
    classId: str, maxAttendees: int, credentials: NeonCredentials
):
    httpVerb = "PATCH"
    resourcePath = f"/events/{classId}"
    queryParams = ""
    data = {"maximumAttendees": maxAttendees}

    url = N_BASE_URL + resourcePath + queryParams
    response = apiCall(httpVerb, url, data, credentials.headers)

    return response


def eventNamePatch(classId: str, newName: str, credentials: NeonCredentials):
    httpVerb = "PATCH"
    resourcePath = f"/events/{classId}"
    queryParams = ""
    data = {"name": newName}

    url = N_BASE_URL + resourcePath + queryParams
    response = apiCall(httpVerb, url, data, credentials.headers)

    return response
