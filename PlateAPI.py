import bs4
import requests


class PlateLengthError(Exception):
    pass


class PlateAPIError(Exception):
    pass


defaults = {
    # cookie_url gets accessed first to retrieve a valid session ID
    "cookie_url": "https://transactions.dmv.virginia.gov/dmvnet/plate_purchase/select_plate.asp",
    "url": "https://transactions.dmv.virginia.gov/dmvnet/common/router.asp",
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "286",
        "Content-Type": "application/x-www-form-urlencoded",
    },
    "payload": "TransType=INQ&TransID=RESINQ&ReturnPage=%2Fdmvnet%2Fplate_purchase%2Fs2end.asp&HelpPage=&Choice=A&PltNo={plate}&HoldISA=N&HoldSavePltNo=&HoldCallHost=&NumCharsInt=6&CurrentTrans=plate_purchase_reserve&PltType=PAVL&PltNoAvail={plate}&PersonalMsg=Y&Let1=a&Let2=a&Let3=a&Let4=a&Let5=a&Let6=a",
    "max_plate_length": 8,
}


class API:
    def __init__(
        self,
        url=defaults["url"],
        headers=defaults["headers"],
        payload=defaults["payload"],
        cookie_url=defaults["cookie_url"],
        session=None,
        max_plate_length=defaults["max_plate_length"],
    ) -> None:
        self.cookie_url = cookie_url
        self.url = url
        self.headers = headers
        self.payload = payload
        self.session = session
        self.max_plate_length = max_plate_length

        # Automatically generate a request session if one isn't provided
        if session is None:
            self.refresh_session()

    # This method is used to generate the necessary session cookies
    # Queries are rejected without having the "WebSessionDataID" cookie
    def refresh_session(self):
        self.session = requests.Session()
        self.session.get(self.cookie_url)

    def check_plate(self, plate):
        # Prepare input
        plate = plate.strip().upper()

        # Check for plate length, VA plates typically don't exceed 7 characters
        if not 0 < len(plate) <= self.max_plate_length:
            raise PlateLengthError("Plate length is invalid")

        response = self.session.post(
            self.url,
            headers=self.headers,
            data=self.payload.format(plate=plate),
            allow_redirects=True,
        )

        soup = bs4.BeautifulSoup(
            response.text, "lxml"
        )  # lxml runs faster than html.parser!

        # The message we're looking for is contained in a <font> tag with a color attribute
        # This is the only <font> tag with a color attribute on the page
        search = soup.find_all(
            lambda tag: tag.name == "font" and tag.attrs.get("color")
        )

        if len(search) == 0:
            # Raise an exception if we can't find the <font> tag
            raise PlateAPIError("Could not find availability tag")
        else:
            message = search[0].text
            is_available = "congratulations" in message.lower()
            is_reserved = "reserved" in message.lower()
            result = {
                "plate_number": plate,
                "available": is_available,
                "reserved": is_reserved,
                "message": message,
            }
            return result
