import os
import sys
import hashlib
import argparse
import requests
import traceback
import urllib.parse
from base64 import b64encode
from typing import Mapping, Tuple, Sequence
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor

from send_s3.db import Database
from send_s3.s3 import S3Request, URLParams, HTTPHeaders, HTTPPayload
from send_s3.config import Config
from send_s3.common import PROG, VERSION, LINESEP, Console


MultiPartSlice = Tuple[int, int, int]
MultiPartResult = Tuple[int, str]


class File:
    def __init__(self, args: argparse.Namespace, config: Config, filepath: str):
        if not self.check(filepath):
            raise Exception(f"Can not upload file: '{filepath}'")
        self.args = args
        self.config = config
        self.upload_domain = config.preferred_upload_domain()
        self.download_domain = config.preferred_download_domain()
        self.download_domains = config.preferred_download_domains()
        self.filepath = filepath
        self.key = config.format_filename(filepath)
        self.url_encoded_key = urllib.parse.quote(self.key)
        self.size = os.path.getsize(filepath)
        self.completed = 0
        self.checksum_chunk_size = 1024 * 1024 * 2    # 2 MB
        self.multipart_chunk_size = 1024 * 1024 * 5   # 5 MB
        self.multipart_threads = 8
        self.headers: HTTPHeaders = {
            'User-Agent': f'{PROG}/{VERSION}',
        }

    def __call__(self, *args, **kwargs):
        self.upload()

    @staticmethod
    def check(filepath: str) -> bool:
        if not (os.path.exists(filepath)):
            Console() >> f"ERROR: File Not Found: {filepath}" >> LINESEP >> sys.stderr
            return False
        if os.path.isdir(filepath):
            Console() >> f"ERROR: Is a directory: {filepath}" >> LINESEP >> sys.stderr
            return False
        return True

    def hide_progress(self) -> bool:
        return self.args.typora

    def single_download_link(self) -> bool:
        return self.args.typora

    def hash(self) -> HTTPHeaders:
        available_checksums = list(filter(lambda x: hasattr(hashlib, x), self.config.checksum))
        available_checksums.append('sha256')
        hash_list = {}
        for checksum in set(available_checksums):
            hash_list[checksum] = getattr(hashlib, checksum)()
        with open(self.filepath, 'rb') as f:
            while chunk := f.read(self.checksum_chunk_size):
                for hash_func in hash_list.values():
                    hash_func.update(chunk)
        return {k: v.hexdigest() for k, v in hash_list.items()}

    def split_parts(self) -> Sequence[MultiPartSlice]:
        for i, start in enumerate(range(0, self.size, self.multipart_chunk_size)):
            yield i + 1, start, min(start + self.multipart_chunk_size - 1, self.size)

    def progress(self) -> None:
        if self.hide_progress():
            return
        percent = min((self.completed / self.size) * 100, 100.0)
        Console() >> f"{percent:.2f}% ({min(self.completed, self.size)}/{self.size}) [{self.key}]\r" >> sys.stderr

    def initialize_multi_part(self, hashes: Mapping[str, str]) -> str:
        signed_request = S3Request.from_config('POST', self.url_encoded_key, self.config,
                                               self.headers, dict(self.config.format_metadata(hashes)),
                                               params={'uploads': ''})
        response = requests.request(**signed_request.to_request())
        response.raise_for_status()
        result = ElementTree.fromstring(response.text)
        return result.find('{*}UploadId').text

    def upload_parts(self, upload_id: str) -> Sequence[MultiPartResult]:
        def upload_part(part_number: int, start: int, end: int):
            self.progress()
            with open(self.filepath, 'rb') as f:
                f.seek(start)
                data = f.read(end - start + 1)
                headers = {
                    'Content-MD5': b64encode(hashlib.md5(data).digest()).decode(),
                    'X-Amz-Content-Sha256': hashlib.sha256(data).hexdigest(),
                }
                signed_request = S3Request.from_config('PUT', self.url_encoded_key, self.config,
                                                       self.headers, headers,
                                                       params={'partNumber': part_number, 'uploadId': upload_id},
                                                       data=data)
                response = requests.request(**signed_request.to_request())
                response.raise_for_status()
                self.completed += len(data)
                self.progress()
                return part_number, response.headers['ETag']
        with ThreadPoolExecutor(max_workers=self.multipart_threads) as executor:
            results = []
            for i, s, e in self.split_parts():
                thread = executor.submit(upload_part, i, s, e)
                results.append(thread)
        results = [r.result() for r in results]
        if not self.hide_progress():
            Console() >> LINESEP >> sys.stderr
        return results

    def complete_multi_part(self, upload_id: str, parts: Sequence[MultiPartResult]) -> HTTPHeaders:
        parts = ''.join([f'<Part><PartNumber>{p}</PartNumber><ETag>{e}</ETag></Part>' for p, e in parts])
        data = f'<CompleteMultipartUpload>{parts}</CompleteMultipartUpload>'.encode('utf-8')
        signed_request = S3Request.from_config('POST', self.url_encoded_key, self.config,
                                               self.headers,
                                               params={'uploadId': upload_id},
                                               data=data)
        response = requests.request(**signed_request.to_request())
        response.raise_for_status()
        return dict(response.headers)

    def download_links(self) -> Tuple[str, Mapping[str, str]]:
        return f"https://{self.download_domain}/{self.url_encoded_key}", {
            k: f"https://{v}/{self.url_encoded_key}" for k, v in self.download_domains.items()
        }

    def write_log(self, hashes: HTTPHeaders, upload_id: str, parts: Sequence[MultiPartResult], headers: HTTPHeaders):
        single, multiple = self.download_links()
        db = Database()
        db.insert(self.filepath, self.key, self.size, f"sha256:{hashes['sha256']}", single, {
            'upload_id': upload_id,
            'parts': parts,
            'headers': headers,
            'download_links': multiple
        })

    def print_download_links(self) -> None:
        single, multiple = self.download_links()
        if self.single_download_link():
            Console() >> single >> LINESEP >> sys.stdout
            return
        length = max(max(map(len, multiple.keys())), len('file')) + 2
        Console() >> f"{'local':<{length}}: {self.filepath}" >> LINESEP >> sys.stdout
        for domain_type, url in multiple.items():
            Console() >> f"{domain_type:<{length}}: {url}" >> LINESEP >> sys.stdout

    def upload(self):
        hashes = self.hash()
        upload_id = self.initialize_multi_part(hashes)
        parts = self.upload_parts(upload_id)
        headers = self.complete_multi_part(upload_id, parts)
        self.write_log(hashes, upload_id, parts, headers)
        self.print_download_links()


def main(args: argparse.Namespace) -> int:
    pause_after_execution = args.windows_sendto
    quiet_output = args.typora
    config = Config.load()
    for file in args.files:
        # noinspection PyBroadException
        try:
            File(args, config, file)()
        except Exception as e:
            Console() >> f"ERROR: {e}" >> LINESEP >> sys.stderr
            Console() >> traceback.format_exc() >> LINESEP >> sys.stderr
            continue
        finally:
            if not quiet_output:
                Console() >> ("-" * 60) >> LINESEP >> sys.stdout
    if pause_after_execution:
        input('Done! Press Enter to close this window...')
    return 0


def register_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("files", metavar="FILE", type=str, nargs="+", help="Files to upload")
    parser.add_argument("--typora", dest="typora", action="store_true")
    parser.add_argument("--windows-sendto", dest="windows_sendto", action="store_true")


__all__ = ['main', 'register_arguments']
