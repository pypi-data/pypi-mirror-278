from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


class ApiSession:
    """Creates an OCLC Api session and provides methods to request holdings data."""

    def __init__(self, oclc_key, oclc_secret, scope=["wcapi"]):
        client = BackendApplicationClient(client_id=oclc_key, scope=scope)
        self.session = OAuth2Session(client=client)
        self.auth = HTTPBasicAuth(oclc_key, oclc_secret)
        self.token = self.get_token()

    def refresh_token(self):
        self.token = self.get_token()

    def get_token(self):
        return self.session.fetch_token(
            token_url="https://authn.sd00.worldcat.org/oauth2/accessToken",
            auth=self.auth,
        )

    def extract_holdings(self, ocns: list, symbols: list):
        """Get holdings for a list of books and institutes

        :param ocns: list of book identifiers
        :param symbols: list of institute symbols
        :return: holdings: per ocn and institute
        """
        holdings_data = []
        for ocn in ocns:
            url = (
                f"https://americas.discovery.api.oclc.org/worldcat/search/v2/bibs-detailed-holdings?"
                f"oclcNumber={ocn}&"
                f'heldBySymbol={",".join(symbols)}'
            )
            r = self.do_request(url)
            holdings_data.append(r.json())
        return holdings_data

    def extract_record_type(self, ocns):
        """Get record types (e.g. single or multipart) for a list of books

        :param ocns: list of book identifiers
        :return: record types per ocn
        """
        records = {}
        for ocn in ocns:
            url = f"https://circ.sd00.worldcat.org/LHR?" f"q=oclc%3A{ocn}"
            r = self.do_request(url)
            data = r.json()
            records[ocn] = data["entry"]
        return records

    def do_request(self, url):
        success = False
        retry = 0
        r = None
        while not success and retry < 3:
            try:
                r = self.session.get(
                    url,
                    headers={
                        "Accept": "application/json",
                        "Content": "application/json",
                        "Authorization": self.token,
                    },
                )
            except TokenExpiredError:
                pass
            if r and r.status_code == 200:
                success = True
            else:
                print("Request to %s: returned: %s" % (url, str(r.status_code)))
                self.refresh_token()  # try with fresh token
                retry += 1
                print("Retrying %i" % (retry))
        if not success:
            # @TODO return more specific error message.
            raise Exception("API returned %s" % (str(r.status_code)))
        return r
