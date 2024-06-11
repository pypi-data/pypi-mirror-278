from uuid import UUID
from typing import Optional

from lqs.common.config import CommonConfig


class RESTClientConfig(CommonConfig):
    api_key_id: Optional[UUID] = None
    api_key_secret: Optional[str] = None
    api_url: Optional[str] = "https://api.logqs.com"
    api_endpoint_prefix: str = "/apps"
    dsm_api_key_id: Optional[UUID] = None
    dsm_api_key_secret: Optional[str] = None
    datastore_id: Optional[UUID] = None

    pretty: bool = False
    verbose: bool = False
    log_level: str = "INFO"
    log_as_json: bool = False
    dry_run: bool = False
    retry_count: int = 2
    retry_delay: int = 5
    retry_aggressive: bool = False
    api_request_timeout: int = 60
    additional_headers: dict[str, str] = {}
