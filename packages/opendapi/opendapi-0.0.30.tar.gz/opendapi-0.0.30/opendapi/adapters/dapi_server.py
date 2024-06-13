# pylint: disable=too-many-instance-attributes, too-many-locals, broad-exception-caught
""""Adapter to interact with the DAPI Server."""

import itertools
import time
from dataclasses import dataclass
from enum import Enum
from importlib.metadata import version
from typing import Callable, Dict, List, Optional, Type
from urllib.parse import urljoin

import requests
from deepmerge import always_merger
from requests.adapters import HTTPAdapter
from snakemd import Document as MDDocument
from urllib3.util.retry import Retry

from opendapi.adapters.file import OpenDAPIFileContents
from opendapi.config import OpenDAPIConfig
from opendapi.logging import LogCounterKey, LogDistKey, Timer, increment_counter

TOTAL_RETRIES = 5
RETRY_BACKOFF_FACTOR = 10


def _chunks(data, size=1):
    iterator = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in itertools.islice(iterator, size)}


@dataclass
class DAPIServerConfig:
    """Configuration for the DAPI Server."""

    server_host: str
    api_key: str
    mainline_branch_name: str
    register_on_merge_to_mainline: bool = True
    suggest_changes: bool = True
    enrich_batch_size: int = 1
    ignore_suggestions_cache: bool = False
    register_batch_size: int = 30
    analyze_impact_batch_size: int = 15


@dataclass
class DAPIServerMeta:
    """Metadata about the DAPI server"""

    name: str
    url: str
    github_user_name: str
    github_user_email: str
    logo_url: Optional[str] = None
    suggestions_cta_url: Optional[str] = None


class DAPIServerRequestType(Enum):
    """Enum for DAPI Server Request Types."""

    VALIDATE = "/v1/registry/validate"
    REGISTER = "/v1/registry/register"
    UNREGISTER = "/v1/registry/unregister"
    ANALYZE_IMPACT = "/v1/registry/impact"


@dataclass
class DAPIServerResponse:
    """DAPI server Response formatted"""

    request_type: DAPIServerRequestType
    status_code: int
    server_meta: DAPIServerMeta
    suggestions: Optional[Dict] = None
    info: Optional[Dict] = None
    errors: Optional[Dict] = None
    text: Optional[str] = None
    markdown: Optional[str] = None

    @property
    def error(self) -> bool:
        """Check if there is an error in the response."""
        return self.errors is not None and len(self.errors) > 0

    @property
    def compiled_markdown(self) -> str:
        """Get the compiled markdown."""
        if (
            self.request_type is DAPIServerRequestType.ANALYZE_IMPACT
            and self.info
            and len(self.info)
        ):
            impact_md = MDDocument()
            impact_md.add_heading(":exclamation: Impact analysis", 2)
            impact_md.add_paragraph(
                "The schema change in this PR might impact an analytics use case. "
                "Please reach out to affected users.\n"
            )
            impact_md.add_table(
                header=[
                    "Dataset",
                    "Datastore",
                    "Impacted Users",
                    "Impacted Tables",
                ],
                data=[
                    [
                        dapi_urn,
                        datastore_urn,
                        (
                            f":warning: <b>{len(compiled_impact['impacted_users'])} users</b>"
                            f"<br>{', '.join(compiled_impact['impacted_users'])}"
                            if compiled_impact["impacted_users"]
                            else ":white_check_mark: No users"
                        ),
                        (
                            f":warning: <b>{len(compiled_impact['impacted_tables'])} tables</b>"
                            f"<br>{', '.join(compiled_impact['impacted_tables'])}"
                            if compiled_impact["impacted_tables"]
                            else ":white_check_mark: No tables"
                        ),
                    ]
                    for dapi_urn, datastore_impact in self.info.items()
                    for datastore_urn, compiled_impact in datastore_impact.items()
                ],
            )
            return str(impact_md)
        return self.markdown

    @property
    def compiled_text(self) -> str:
        """Get the compiled text."""
        return self.text

    def merge(self, other: "DAPIServerResponse") -> "DAPIServerResponse":
        """Merge two responses."""

        def merge_text_fn(this_text, other_text):
            if not this_text or not other_text:
                return other_text or this_text

            return (
                "\n\n".join([this_text, other_text])
                if this_text != other_text
                else other_text
            )

        def merge_dict(this_dict, other_dict):
            if not this_dict or not other_dict:
                return other_dict or this_dict

            return always_merger.merge(this_dict, other_dict)

        if self.request_type != other.request_type:
            raise ValueError(
                f"Cannot merge responses of different types: {self.request_type} and {other.request_type}"
            )

        return DAPIServerResponse(
            request_type=other.request_type or self.request_type,
            status_code=other.status_code or self.status_code,
            server_meta=other.server_meta or self.server_meta,
            errors=merge_dict(self.errors, other.errors),
            suggestions=merge_dict(self.suggestions, other.suggestions),
            info=merge_dict(self.info, other.info),
            text=merge_text_fn(self.text, other.text),
            markdown=merge_text_fn(self.markdown, other.markdown),
        )


class DAPIRequests:
    """Class to handle requests to the DAPI Server."""

    def __init__(
        self,
        dapi_server_config: DAPIServerConfig,
        opendapi_config: OpenDAPIConfig,
        all_files: OpenDAPIFileContents,
        changed_files: OpenDAPIFileContents,
        changed_files_from_base: OpenDAPIFileContents,
        error_msg_handler: Optional[Callable[[str], None]] = None,
        error_exception_cls: Optional[Type[Exception]] = None,
        txt_msg_handler: Optional[Callable[[str], None]] = None,
        markdown_msg_handler: Optional[Callable[[str], None]] = None,
    ):  # pylint: disable=too-many-arguments
        self.dapi_server_config = dapi_server_config
        self.opendapi_config = opendapi_config
        self.all_files = all_files
        self.changed_files = changed_files
        self.changed_files_from_base = changed_files_from_base
        self.error_msg_handler = error_msg_handler
        self.error_exception_cls = error_exception_cls or Exception
        self.txt_msg_handler = txt_msg_handler
        self.markdown_msg_handler = markdown_msg_handler

        self.session = requests.Session()
        # Add retry once after 60s for 500, 502, 503, 504
        # This is to handle the case where the server is starting up
        # or when any AI per-minute token limits are hit
        kwargs = {
            "total": TOTAL_RETRIES,
            "backoff_factor": RETRY_BACKOFF_FACTOR,
            "status_forcelist": [500, 502, 503, 504],
            "allowed_methods": ["POST"],
        }

        # Add some more options for urllib3 2.0.0 and above
        urllib3_version = version("urllib3").split(".")
        if int(urllib3_version[0]) >= 2:  # pragma: no cover
            kwargs.update(
                {
                    "backoff_jitter": 15,
                    "backoff_max": 360,  # Default is 120
                }
            )

        retries = Retry(**kwargs)
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def handle_server_message(self, message: str, should_print: bool = True) -> None:
        """Handle a message from the server."""
        # Show the messages
        if message.get("errors"):
            if self.error_msg_handler:
                self.error_msg_handler("There were errors")

        if should_print:
            if message.get("md") and self.markdown_msg_handler:
                self.markdown_msg_handler(
                    f'<br>{message.get("md", message.get("text"))}'
                )

            if message.get("text") and self.txt_msg_handler:
                self.txt_msg_handler(f'\n{message.get("text")}')

    def ask_dapi_server(
        self,
        request_type: DAPIServerRequestType,
        payload: dict,
        print_txt_markdown: bool = True,
    ) -> DAPIServerResponse:
        """Ask the DAPI Server for something."""
        headers = {
            "Content-Type": "application/json",
            "X-DAPI-Server-API-Key": self.dapi_server_config.api_key,
        }
        request_path = request_type.value
        # mesure the time it takes to get a response from the server in milliseconds
        metrics_tags = {
            "request_path": request_path,
            "org_name": self.opendapi_config.org_name_snakecase,
        }
        with Timer(LogDistKey.ASK_DAPI_SERVER) as _timer:
            response = self.session.post(
                urljoin(self.dapi_server_config.server_host, request_path),
                headers=headers,
                json=payload,
                timeout=60,
            )
            metrics_tags["status_code"] = response.status_code
            _timer.set_tags(metrics_tags)

        for payload_type in ["teams", "datastores", "purposes", "dapis"]:
            if payload_type in payload:
                increment_counter(
                    key=LogCounterKey.ASK_DAPI_SERVER_PAYLOAD_ITEMS,
                    value=len(payload[payload_type]),
                    tags=always_merger.merge(
                        metrics_tags, {"payload_type": payload_type}
                    ),
                )
        # Server responds with a detailed error on 400, so only error when status > 400
        if response.status_code > 400:
            msg = (
                f"Something went wrong! API failure with {response.status_code} "
                f"for {request_path}"
            )
            if self.error_msg_handler:
                self.error_msg_handler(msg)
            raise self.error_exception_cls(msg)

        message = response.json()

        server_meta = message.get("server_meta", {})

        self.handle_server_message(
            message, (print_txt_markdown or response.status_code >= 400)
        )

        return DAPIServerResponse(
            request_type=request_type,
            status_code=response.status_code,
            server_meta=DAPIServerMeta(
                name=server_meta.get("name", "DAPI Server"),
                url=server_meta.get("url", "https://opendapi.org"),
                github_user_name=server_meta.get("github_user_name", "github-actions"),
                github_user_email=server_meta.get(
                    "github_user_email", "github-actions@github.com"
                ),
                logo_url=server_meta.get("logo_url"),
                suggestions_cta_url=server_meta.get("suggestions_cta_url"),
            ),
            errors=message.get("errors"),
            suggestions=message.get("suggestions"),
            info=message.get("info"),
            markdown=message.get("md"),
            text=message.get("text"),
        )

    def validate(
        self,
        commit_hash: str,
        suggest_changes_override: Optional[bool] = None,
        ignore_suggestions_cache: bool = False,
        notify_function: Optional[Callable[[int], None]] = None,
    ) -> DAPIServerResponse:
        """Validate OpenDAPI files with the DAPI Server."""
        all_files = self.all_files.for_server()
        changed_files = self.changed_files.for_server()
        chunk_size = self.dapi_server_config.enrich_batch_size
        suggest_changes = (
            self.dapi_server_config.suggest_changes
            if suggest_changes_override is None
            else suggest_changes_override
        )

        def _build_validate_payload(updates: dict) -> dict:
            base_validate_payload = {
                "dapis": {},
                "teams": {},
                "datastores": {},
                "purposes": {},
                "suggest_changes": suggest_changes,
                "commit_hash": commit_hash,
                "ignore_suggestions_cache": ignore_suggestions_cache,
            }
            result = base_validate_payload.copy()
            result.update(updates)
            return result

        # First, we validate the non-dapi files
        payload = _build_validate_payload(
            {
                "teams": all_files["teams"],
                "datastores": all_files["datastores"],
                "purposes": all_files["purposes"],
            }
        )
        resp = self.ask_dapi_server(
            DAPIServerRequestType.VALIDATE, payload, print_txt_markdown=False
        )
        # Then we validate the dapi files in batches
        for dapi_chunk in _chunks(changed_files["dapis"], chunk_size):
            for dapi_loc in dapi_chunk:
                all_files["dapis"].pop(dapi_loc, None)
            try:
                payload = _build_validate_payload({"dapis": dapi_chunk})
                this_resp = self.ask_dapi_server(
                    DAPIServerRequestType.VALIDATE, payload, print_txt_markdown=False
                )
                resp = resp.merge(this_resp)
            except self.error_exception_cls:
                # In case of errors (likely from AI timeouts), validate one by one
                # but first sleep for RETRY_BACKOFF_FACTOR to give the server time to recover
                time.sleep(RETRY_BACKOFF_FACTOR)
                for loc, item in dapi_chunk.items():
                    payload = _build_validate_payload({"dapis": {loc: item}})
                    this_resp = self.ask_dapi_server(
                        DAPIServerRequestType.VALIDATE,
                        payload,
                        print_txt_markdown=False,
                    )
                    resp = resp.merge(this_resp)

            if notify_function is not None:
                notify_function(chunk_size)

        # Finally, we validate the remaining files without suggestions
        if all_files["dapis"]:
            payload = _build_validate_payload(
                {"dapis": all_files["dapis"], "suggest_changes": False}
            )
            resp = resp.merge(
                self.ask_dapi_server(
                    DAPIServerRequestType.VALIDATE, payload, print_txt_markdown=False
                )
            )
            if notify_function is not None:
                notify_function(chunk_size)

        return resp

    def analyze_impact(
        self,
        notify_function: Optional[Callable[[int], None]] = None,
        from_base: bool = True,
    ) -> DAPIServerResponse:
        """Analyze the impact of changes on the DAPI Server."""
        files = self.changed_files_from_base if from_base else self.changed_files
        server_files = files.for_server()
        chunk_size = self.dapi_server_config.analyze_impact_batch_size
        resp: DAPIServerResponse = self.ask_dapi_server(
            DAPIServerRequestType.ANALYZE_IMPACT,
            {
                "dapis": {},
                "teams": server_files["teams"],
                "datastores": server_files["datastores"],
                "purposes": server_files["purposes"],
            },
        )

        for dapi_chunk in _chunks(server_files["dapis"], chunk_size):
            this_resp = self.ask_dapi_server(
                DAPIServerRequestType.ANALYZE_IMPACT,
                {
                    "dapis": dapi_chunk,
                    "teams": {},
                    "datastores": {},
                    "purposes": {},
                },
            )
            resp = resp.merge(this_resp) if resp else this_resp
            if notify_function is not None:
                notify_function(chunk_size)
        return resp

    def register(
        self,
        commit_hash: str,
        source: str,
        notify_function: Optional[Callable[[int], None]] = None,
    ) -> Optional[DAPIServerResponse]:
        """Register OpenDAPI files with the DAPI Server."""
        all_files = self.all_files.for_server()
        chunk_size = self.dapi_server_config.register_batch_size
        resp: DAPIServerResponse = self.ask_dapi_server(
            DAPIServerRequestType.REGISTER,
            {
                "dapis": {},
                "teams": all_files["teams"],
                "datastores": all_files["datastores"],
                "purposes": all_files["purposes"],
                "commit_hash": commit_hash,
                "source": source,
            },
        )

        for dapi_chunk in _chunks(all_files["dapis"], chunk_size):
            this_resp = self.ask_dapi_server(
                DAPIServerRequestType.REGISTER,
                {
                    "dapis": dapi_chunk,
                    "teams": {},
                    "datastores": {},
                    "purposes": {},
                    "commit_hash": commit_hash,
                    "source": source,
                },
            )
            resp = resp.merge(this_resp) if resp else this_resp
            if notify_function is not None:
                notify_function(chunk_size)
        return resp

    def unregister(self, source: str, except_dapi_urns: List[str]):
        """Unregister missing DAPIs from the DAPI Server."""
        return self.ask_dapi_server(
            DAPIServerRequestType.UNREGISTER,
            {
                "source": source,
                "except_dapi_urns": except_dapi_urns,
            },
        )
