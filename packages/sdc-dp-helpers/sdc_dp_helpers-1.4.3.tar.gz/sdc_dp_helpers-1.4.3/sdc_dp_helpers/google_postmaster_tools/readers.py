"""
CUSTOM READERS MODULE FOR GOOGLE POSTMASTER READER
"""
from typing import Dict, List, Any, Union, Generator
from googleapiclient import discovery, errors
from google.oauth2 import service_account

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import (
    date_range_iterator,
    check_date_range_validity,
)
from sdc_dp_helpers.base_readers import BaseReader


class GooglePostmasterReader(BaseReader):
    """
    Google Postmaster Reader
    """

    def __init__(self, creds_filepath: str, config_filepath: str) -> None:
        super().__init__()
        self.secrets: Dict[Any, Any] = load_file(creds_filepath)
        self.config: Dict[Any, Any] = load_file(config_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client.
        """
        credentials = service_account.Credentials.from_service_account_info(
            info=self.secrets,
            scopes=["https://www.googleapis.com/auth/postmaster.readonly"],
        )
        service = discovery.build(
            serviceName="gmailpostmastertools",
            version="v1beta1",
            credentials=credentials,
        )
        if service is None:
            raise RuntimeError("Service is null.")
        if not hasattr(service, "domains"):
            raise KeyError("Service does not have domains attribute.")
        return service

    def _query_handler(self, *args, **kwargs) -> dict:
        # pylint: disable=no-member
        """Handles the Query call"""

        if not {"domain", "date"}.issubset(set(kwargs.keys())):
            raise KeyError("Invalid arguments - expecting: domain, date")
        response = (
            self.service.domains()
            .trafficStats()
            .get(name=f"domains/{kwargs['domain']}/trafficStats/{kwargs['date']}")
            .execute()
        )
        if response is None:
            raise RuntimeError("response is 'None'")
        self.is_success()
        return response

    def run_query(
        self,
    ) -> Union[
        Generator[Dict[List[Dict[Any, Any]], Any], None, None],
        Dict[List[Dict[Any, Any]], Any],
    ]:
        """Run the query and return the data"""
        check_date_range_validity(self.config["start_date"], self.config["end_date"])

        domains = self.config["domains"]

        date_range = date_range_iterator(
                start_date=self.config["start_date"],
                end_date=self.config["end_date"],
                interval="1_day",
                end_inclusive=True,
                time_format="%Y%m%d",
            )
        for date, _ in date_range:
            print(f"date : {date}")
            for domain in domains:
                print(f"domain : {domain}")
                try:

                    dataset = self._query_handler(domain=domain, date=date)
                    print(f"{domain} {date} success")
                    yield {
                        "date": date,
                        "brand": domain.replace(".", "_"),
                        "data": [dataset],
                    }
                except RuntimeError as err:
                    self.not_success()
                    print(f"Error occured: {err}")
                except errors.HttpError as err:
                    self.not_success()
                    print(f"{domain} {date} fail: {err}")
                except KeyError as err:
                    self.not_success()
                    print(f"An error occurred: {err}")
