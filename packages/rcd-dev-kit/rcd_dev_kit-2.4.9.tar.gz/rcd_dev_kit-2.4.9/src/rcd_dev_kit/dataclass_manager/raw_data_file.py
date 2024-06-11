import os
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional
from ..database_manager import OipApiOperator, download_from_gcloud, upload_to_gcloud
from ..file_manager import detect_path


class RawDataFile(ABC):
    source_name: str = NotImplemented
    source_url: str = NotImplemented
    source_uuid: str = NotImplemented
    file_name: str = NotImplemented
    file_folder: str = NotImplemented
    debug: bool = False

    def __init__(self, base_path: str) -> None:
        """Call in each child to check and fill info"""
        self.check_source_uuid()
        self.fill_cls_info()
        self.file_path = os.path.join(base_path, "raw_data", self.source_uuid, self.file_folder)
        self.lst_df_raw = list()
        detect_path(path=self.file_path)

    """
    Class method: Strictly check if source UUID is a source UUID, fill information at __init__ time
    """

    # @classmethod
    # def check_source_uuid(cls) -> None:
    #     """Check if source uuid is registered in database"""
    #     mo = MysqlOperator()
    #     df_source = pd.read_sql_query("SELECT * FROM oip.sources", mo.engine)
    #     assert cls.source_uuid in df_source[
    #         "id"].unique(), f"❌️Source UUID is not registered in OIP block: {cls.source_uuid}"

    @classmethod
    def check_source_uuid(cls) -> None:
        """Check if source uuid is registered in database"""
        if cls.debug is False:
            # If debug is false, Check uuid and raise error if not find
            cls.get_source_uuid()
        else:
            print('Checking source UUID in debug mode...')
            # If debug is True, Check uuid and goes on if not exist.
            try:
                cls.get_source_uuid()
                print("Source UUID successfully checked in debug mode.")
            except Exception as e:
                print(f"Error occurred while checking source UUID: {e}")
    
    @classmethod
    def get_source_uuid(cls) -> None:
        oip_api = OipApiOperator()
        raw_response_all_sources = oip_api.authenticate_auth0().set_sources().get_all_sources()
        lst_data_sources = raw_response_all_sources["data"]
        lst_sources_uuid = [source["id"] for source in lst_data_sources if source["type"] == "sources"]
        if cls.source_uuid not in lst_sources_uuid:
            print(f"❌️Source UUID is not registered in OIP block: {cls.source_uuid}")

    @classmethod
    def fill_cls_info(cls) -> None:
        """Fill oip provider/source block url, and gcloud raw data bucket url"""
        cls.oip_url = f"https://openinnovationprogram.com/source/{cls.source_uuid}/description"
        cls.gcloud_url = f"https://console.cloud.google.com/storage/browser/oip-opendata-raw_784c50873a74/{cls.source_uuid}"

    """
    Abstract method: Strictly required in each child to get download file, and sync to gcloud
    """

    @abstractmethod
    def download(self) -> None:
        """"To download this raw data file"""

    def sync_gcloud(self) -> None:
        """To sync with gcloud raw data folder"""
        bucket=os.environ.get("OPEN_DATA_SOURCE_BUCKET")
        upload_to_gcloud(local_folder_path=self.file_path, uuid=self.source_uuid, bucket=bucket)
        download_from_gcloud(local_folder_path=self.file_path, uuid=self.source_uuid, bucket=bucket)

    @abstractmethod
    def read(self) -> Optional:
        """To read list of df_raw"""
