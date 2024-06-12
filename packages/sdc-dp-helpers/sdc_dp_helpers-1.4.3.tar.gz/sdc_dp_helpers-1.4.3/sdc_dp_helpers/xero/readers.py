# pylint: disable=no-member,inconsistent-return-statements,wrong-import-order,broad-exception-raised,no-else-return,arguments-differ, line-too-long,missing-module-docstring,too-many-nested-blocks, missing-final-newline, too-many-arguments
from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.xero.xero_sdk import XeroAPICall, GetTrackingCategories
from sdc_dp_helpers.base_readers import BaseReader


class XeroReader(BaseReader):
    """
    Xero reader
    """

    def __init__(self, creds_path: str, config_path: str):
        self.creds_path: str = creds_path
        self.config: dict = load_file(config_path, "yml")
        self.service = self._get_auth()
        self.dataset = []

    def _get_auth(self):
        """Authenticate."""
        self.service = XeroAPICall(config=self.config, creds_path=self.creds_path)
        return self.service

    def _query_handler(
        self,
        tenant_id,
        report: str,
        start_date: str,
        end_date: str,
        tracking_category: str,
        filterby: str,
    ):
        """Runs a simple reports."""
        data = self.service.get_reports(
            tenant_id, report, start_date, end_date, tracking_category, filterby
        )
        return data

    def run_query(self):
        """Controls the Flow of Query"""
        payload = []
        if self.config.get("report"):
            for tenants_name, tenant_id in self.config.get("tenants").items():
                trackingcategories = GetTrackingCategories(
                    config=self.config, creds_filepath=self.creds_path
                ).make_api_call(tenant_id)
                for tracking_category in trackingcategories:
                    for filterby in self.config["filters"]:
                        for start_date, end_date in date_range_iterator(
                            start_date=self.config["start_date"],
                            end_date=self.config["end_date"],
                            interval=self.config["interval"],
                            end_inclusive=True,
                            time_format="%Y-%m-%d",
                            ytd=self.config.get("ytd", False),
                        ):
                            payload = self._query_handler(
                                tenant_id,
                                self.config.get("report"),
                                start_date,
                                end_date,
                                tracking_category,
                                filterby,
                            )
                            yield {
                                "endpoint": self.config.get("report"),
                                "tenant_name": tenants_name,
                                "trackingCategoryId": tracking_category[
                                    "TrackingCategoryID"
                                ],
                                "data": payload,
                                "date": end_date,
                                "filterby": filterby,
                            }
                            self.is_success()
                            if not payload:
                                self.not_success()
                                print(
                                    f"""No data for {self.config.get("report")} Report for start_date {start_date} and end_date {end_date}"""
                                )
        if self.config.get("modules"):
            for tenants_name, tenant_id in self.config.get("tenants").items():
                for module in self.config.get("modules", []):
                    for start_date, end_date in date_range_iterator(
                        start_date=self.config["start_date"],
                        end_date=self.config["end_date"],
                        interval=self.config["interval"],
                        end_inclusive=True,
                        time_format="%Y-%m-%d",
                    ):
                        payload = self.service.get_modules(
                            tenant_id, module, start_date, end_date
                        )
                        yield {
                            "endpoint": module,
                            "tenant_name": tenants_name,
                            "data": payload,
                            "date": end_date,
                            "trackingCategoryId": "",
                        }
                        self.is_success()
                        if not payload:
                            self.not_success()
                            print(
                                f"""No data for {module} Module for start_date {start_date} and end_date {end_date}"""
                            )
