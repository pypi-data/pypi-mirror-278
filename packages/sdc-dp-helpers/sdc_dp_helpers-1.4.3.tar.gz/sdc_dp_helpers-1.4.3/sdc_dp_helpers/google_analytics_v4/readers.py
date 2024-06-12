"""
    CUSTOM READER CLASS
"""
# pylint: disable=too-few-public-methods,import-error,unused-import,redefined-outer-name
from typing import Dict, List, Any
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    FilterExpressionList,
    Metric,
    RunReportRequest,
)
from google.api_core import exceptions


from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file


class GAV4Reader:
    """
    GOOGLE ANALYTICS V4 READERS CLASS
    """

    api_calls = 0

    def __init__(self, configs_file_path: str, service_account_file_path: str):
        self.configs = load_file(configs_file_path, fmt="yml")
        self.service_account_file_path = service_account_file_path
        self._client = self._get_client()
        self.dataset = []
        self.errors: dict = {}

    def _get_client(self):
        client = BetaAnalyticsDataClient().from_service_account_json(
            self.service_account_file_path
        )
        return client

    def _normalize(self, data, property_id: str) -> List[Dict[Any, Any]]:
        """Normalizes Data to Dictionary Format"""
        list_dataset = []
        dimension_headers = data.dimension_headers
        metric_headers = data.metric_headers

        for idx, row in enumerate(data.rows):
            row_data = {
                "property_id": property_id,
                "profile_name": self.configs["property_ids"][property_id],
            }

            for idx, dim_value_key in enumerate(row.dimension_values):
                row_data[dimension_headers[idx].name] = dim_value_key.value

            for idx, metric_value_key in enumerate(row.metric_values):
                row_data[metric_headers[idx].name] = metric_value_key.value

            list_dataset.append(row_data)
            # print(row_data)
        return list_dataset

    @staticmethod
    def build_multi_dimension_filter(config: dict):
        """method to build the api query to run"""
        expressions: List[FilterExpression] = []
        for field_name, value in config.items():
            dimension_filter = FilterExpression(
                filter=Filter(
                    field_name=field_name,
                    in_list_filter=Filter.InListFilter(values=value),
                )
            )
            expressions.append(dimension_filter)
        return FilterExpression(and_group=FilterExpressionList(expressions=expressions))


    def filtered_request(
        self, property_id: str,
        start_date: str,
        end_date:str,
        filters: dict
        ) -> RunReportRequest:
        """method for generating api call filters"""
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dim) for dim in self.configs["dimensions"]],
            metrics=[Metric(name=metric) for metric in self.configs["metrics"]],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=self.build_multi_dimension_filter(filters),
            limit=self.configs.get("limit", 100000),
        )
        return request

    def unfiltered_request(
        self,
        property_id: str,
        start_date: str,
        end_date: str
        ) -> RunReportRequest:
        """method for generating api calls that are not filtered"""
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dim) for dim in self.configs["dimensions"]],
            metrics=[Metric(name=metric) for metric in self.configs["metrics"]],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            limit=self.configs.get("limit", 100000),
        )
        return request

    def get_request(
        self,
        property_id: str,
        start_date: str,
        end_date: str,
        filters: dict
        ) -> RunReportRequest:
        """method to return the request"""
        if filters:
            return self.filtered_request(property_id, start_date, end_date, filters)
        return self.unfiltered_request(property_id, start_date, end_date)

    def _query_handler(self, property_id: str, start_date: str, end_date: str):
        """Runs a simple report on a Google Analytics 4 property."""
        # Explicitly use service account credentials by specifying
        # the private key file.
        response = None
        request = self.get_request(
            property_id, start_date, end_date, self.configs.get("filters", {}))
        GAV4Reader.api_calls += 1
        try:
            response = self._client.run_report(request)
        except exceptions.InvalidArgument as error:
            print(f"invalid parameters for property_id: {error.message}")
            response = {"details": "invalid parameters"}
            self.errors[property_id] = error.message
        except Exception as error:
            print(f"Number of api calls made before this error {GAV4Reader.api_calls}")
            raise error
        return response

    def run_query(self):
        """Controls the Flow of Query"""
        try:
            for property_id in self.configs["property_ids"]:
                for start_date, end_date in date_range_iterator(
                    start_date=self.configs["start_date"],
                    end_date=self.configs["end_date"],
                    interval=self.configs["interval"],
                    end_inclusive=True,
                    time_format="%Y-%m-%d",
                ):
                    payload = self._query_handler(
                        property_id=property_id,
                        start_date=start_date,
                        end_date=end_date,
                    )

                    if (
                        isinstance(payload, dict)
                        and payload.get("details") == "invalid parameters"
                    ):
                        break
                    if not payload:
                        continue

                    dataset: List[Dict] = self._normalize(payload, property_id)
                    yield {
                        "date": start_date,
                        "property_id": property_id,
                        "data": dataset,
                    }
                    self.dataset = dataset
                if not self.dataset:
                    print(f"no data for property_id {property_id}")
        except Exception as error:
            print(f"Number of api calls made before this error {GAV4Reader.api_calls}")
            raise error
        finally:
            print(f"Current number of api calls: {GAV4Reader.api_calls}")
