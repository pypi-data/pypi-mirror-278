import hmac
import hashlib
import datetime
from typing import Dict, Union, Optional
from dataclasses import dataclass
from urllib.parse import urlencode

from send_s3.config import Config

URLParams = Dict[str, str]
HTTPHeaders = Dict[str, str]
HTTPPayload = Union[bytes, str]


@dataclass
class S3Request:
    region: str
    method: str
    host: str
    path: str
    params: URLParams
    headers: HTTPHeaders
    secret_id: str
    secret_key: str
    data: bytes

    def __post_init__(self):
        date = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        self.datetime = date
        self.date = date[:8]
        self.method = self.method.upper()
        self.path = self.path if self.path.startswith('/') else f"/{self.path}"
        self.params = dict(sorted(self.params.items()))
        self.headers.update({
            'Host': self.host,
            'x-amz-date': self.datetime
        })
        self.headers = dict(sorted({k.lower(): v for k, v in self.headers.items()}.items()))
        if self.data is None:
            self.payload_hash = 'UNSIGNED-PAYLOAD'
        else:
            self.payload_hash = self.sha256_hex(self.data)

    @staticmethod
    def from_config(method: str, path: str, config: Config,
                    *headers_list: HTTPHeaders,
                    params: Optional[URLParams] = None,
                    data: Optional[HTTPPayload] = None) -> 'S3Request':
        headers: Dict[str, str] = {}
        for headers in headers_list:
            headers.update(headers)
        return S3Request(
            region=config.region,
            method=method,
            host=config.preferred_upload_domain(),
            path=path,
            params=params or {},
            headers=headers,
            secret_id=config.credentials.secret_id,
            secret_key=config.credentials.secret_key,
            data=data.encode('utf-8') if isinstance(data, str) else data
        )

    @staticmethod
    def sha256(data: HTTPPayload) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    @staticmethod
    def sha256_hex(data: HTTPPayload) -> str:
        return S3Request.sha256(data).hex()

    @staticmethod
    def hmac_sha256(key: HTTPPayload, msg: HTTPPayload) -> bytes:
        if isinstance(key, str):
            key = key.encode("utf-8")
        if isinstance(msg, str):
            msg = msg.encode("utf-8")
        return hmac.new(key, msg, hashlib.sha256).digest()

    @staticmethod
    def hmac_sha256_hex(key: HTTPPayload, msg: HTTPPayload) -> str:
        return S3Request.hmac_sha256(key, msg).hex()

    def url(self) -> str:
        return f"https://{self.host}{self.path}"

    def scope(self) -> str:
        return f"{self.date}/{self.region}/s3/aws4_request"

    def query_string(self) -> str:
        return urlencode(self.params)

    def header_signing_items(self) -> str:
        return '\n'.join([f"{k}:{v}" for k, v in self.headers.items()])

    def header_signing_keys(self) -> str:
        return ';'.join(self.headers.keys())

    def canonical_request(self) -> str:
        return "\n".join([
            self.method,
            self.path,
            self.query_string(),
            self.header_signing_items(),
            '',
            self.header_signing_keys(),
            self.payload_hash
        ])

    def signing_string(self) -> str:
        canonical_request = self.canonical_request()
        return "\n".join([
            'AWS4-HMAC-SHA256',
            self.datetime,
            self.scope(),
            self.sha256_hex(canonical_request)
        ])

    def signature(self) -> str:
        signing_string = self.signing_string()
        k_date = self.hmac_sha256(f"AWS4{self.secret_key}", self.date)
        k_region = self.hmac_sha256(k_date, self.region)
        k_service = self.hmac_sha256(k_region, 's3')
        k_signing = self.hmac_sha256(k_service, 'aws4_request')
        signature = self.hmac_sha256(k_signing, signing_string)
        return f"AWS4-HMAC-SHA256 Credential={self.secret_id}/{self.scope()}, " \
               f"SignedHeaders={self.header_signing_keys()}, Signature={signature.hex()}"

    def signed_headers(self) -> HTTPHeaders:
        result = self.headers.copy()
        result['authorization'] = self.signature()
        result['x-amz-content-sha256'] = self.payload_hash
        return result

    def to_request(self) -> Dict[str, str]:
        return {
            'method': self.method,
            'url': self.url(),
            'headers': self.signed_headers(),
            'params': self.params,
            'data': self.data,
        }


__all__ = ["S3Request", "URLParams", "HTTPHeaders", "HTTPPayload"]
