"""CUSTOM MODULE TO WRITE ZOHO RECRUIT DATA"""
# pylint: disable=too-few-public-methods, too-many-arguments, line-too-long
import json
from typing import Union, List, Any, Dict, Tuple, Optional
import boto3
from sdc_dp_helpers.base_writers import BaseWriter


class GAV4Writer(BaseWriter):
    """WRITER FOR GA V4 DATA"""

    def __init__(
        self,
        bucket: str,
        folder_path: str,
        destination: str,
        configs: Optional[Dict[str, Any]] = None,
        clear_destination: bool = False,
    ):
        self.success: List[bool] = []
        self.current_destination: Union[str, None] = None
        super().__init__(
            bucket=bucket,
            folder_path=folder_path,
            destination=destination,
            configs=configs,
            clear_destination=clear_destination,
        )

    def verify_data(
        self, payload: Dict[str, Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[str, Any]): expecting a dictionary having data, date and dimension

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
        """
        # confirm the payload keys are matching accurately with what is expected
        if list(payload.keys()).sort() != ["data", "date", "property_id"].sort():
            raise KeyError("Invalid payload")
        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")
        if not isinstance(payload["property_id"], str):
            raise TypeError("invalid property_id passed: expected string")
        _property_id = payload.get("property_id")
        _date = payload.get("date")
        if _date:
            _date = _date.replace("-", "")
        else:
            raise KeyError("Date cannot be None")
        _data = payload.get("data")
        write_path: str = f"{self.folder_path}/{_property_id}/{_date}"

        return write_path, _data

    def write_stats_to_s3(
        self,
        stats: str,
        date: str,
        property_id: str,
        use_case: str,
        target_table_name: str = "gav4_api_statistics",
    ) -> None:
        """
        Write statistics about the number of api calls on a particular date, network and endpoint.
        """
        boto3_session = boto3.Session()
        s3_resource = boto3_session.resource("s3")
        write_path: str = f"{target_table_name}/date={date}/use_case={use_case}/property_id={property_id}/stats.json"
        if stats:
            print(
                f"Writing data to s3://{self.bucket}/{write_path} partitioned by networks and date."
            )
            s3_resource.Object(self.bucket, write_path).put(Body=json.dumps(stats))
