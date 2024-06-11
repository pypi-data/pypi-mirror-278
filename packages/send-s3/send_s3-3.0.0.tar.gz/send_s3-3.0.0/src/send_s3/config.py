import os
import toml
import uuid
import time
import datetime
from typing import Mapping, Sequence, Dict
from pydantic import BaseModel

from send_s3.common import app_directory

CONFIG_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "config.toml")


class BaseConfig(BaseModel):
    class Config:
        @staticmethod
        def alias_generator(field_name: str) -> str:
            return field_name.replace("_", "-")


class CredentialsConfig(BaseConfig):
    secret_id: str
    secret_key: str


class TransportConfig(BaseConfig):
    metadata_prefix: str
    upload_domain: str
    download_domain: Sequence[str]


class Config(BaseConfig):
    region: str
    bucket: str
    prefix: str
    checksum: Sequence[str]
    filename: str
    utc_time: bool
    credentials: CredentialsConfig
    transport: TransportConfig
    domains: Mapping[str, str]

    def preferred_upload_domain(self) -> str:
        if result := self.domains.get(self.transport.upload_domain):
            return result.format(**self.model_dump())
        if len(self.domains) > 0:
            return next(iter(self.domains.values())).format(**self.model_dump())
        raise IndexError(f"Domain '{self.transport.upload_domain}' not found in configuration")

    def preferred_download_domains(self) -> Dict[str, str]:
        domains = {}
        for domain_type in self.transport.download_domain:
            if result := self.domains.get(domain_type):
                domains[domain_type] = result.format(**self.model_dump())
        if len(domains) > 0:
            return domains
        return {'default': self.perferred_upload_domain()}

    def preferred_download_domain(self) -> str:
        for k, v in self.preferred_download_domains().items():
            return v

    @staticmethod
    def load() -> 'Config':
        config_file = app_directory("config.toml")
        config_toml = toml.load(config_file)
        return Config.model_validate(config_toml)

    def format_metadata(self, metadata: Mapping[str, str]) -> Mapping[str, str]:
        prefix = self.transport.metadata_prefix
        if not prefix.endswith('-'):
            prefix += '-'
        return {f"{prefix}{k}": v for k, v in metadata.items()}

    def format_filename(self, filepath: str) -> str:
        current_time = datetime.datetime.now(datetime.UTC) if self.utc_time else datetime.datetime.now()
        filename, extension = os.path.splitext(os.path.basename(filepath))
        params = {
            "uuid": str(uuid.uuid4()),
            "name": filename,
            "ext": extension,
            "y": current_time.strftime("%Y"),
            "m": current_time.strftime("%m"),
            "d": current_time.strftime("%d"),
            "h": current_time.strftime("%H"),
            "i": current_time.strftime("%M"),
            "s": current_time.strftime("%S"),
            "ts": int(time.time()),
        }
        return self.prefix + self.filename.format(**params)


__all__ = ['Config', 'CredentialsConfig', 'TransportConfig', 'CONFIG_SOURCE_PATH']
