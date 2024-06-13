#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import argparse
import dataclasses
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from joker.cast.iterative import chunkwize

from cascadis.environ import GlobalInterface
from cascadis.solutions import register_cli_upload
from cascadis.utils import find_regular_files

gi = GlobalInterface()


@dataclasses.dataclass
class _CommandContext:
    delete: bool = False
    concurrency: int = 1

    def _put_file_into_cas(self, path: str):
        # TODO: check gi.dirs existence
        if self.delete and os.stat(path).st_dev == os.stat(gi.dirs[0]).st_dev:
            return gi.cas.seize(path)
        with open(path, "rb") as fin:
            content = fin.read()
            cid = gi.cas.save([content])
        if self.delete:
            os.remove(path)
        return cid

    def put_file_into_cas(self, path: str):
        path = os.path.abspath(path)
        cid = self._put_file_into_cas(path)
        print(cid, path)
        register_cli_upload(cid, path)
        return cid

    def put_files_in_dir_into_cas(self, dirpath):
        paths = find_regular_files(dirpath)
        if self.concurrency == 1:
            for path in paths:
                self.put_file_into_cas(path)
        else:
            executor = ThreadPoolExecutor(max_workers=self.concurrency)
            for batch in chunkwize(1000, paths):
                executor.map(self.put_file_into_cas, batch)

    def run(self, paths: list[str]):
        for path in paths:
            if os.path.isdir(path):
                self.put_files_in_dir_into_cas(path)
            else:
                self.put_file_into_cas(path)


def _main(paths: list[str], delete=False):
    cc = _CommandContext(delete=delete)
    for path in paths:
        if os.path.isdir(path):
            cc.put_files_in_dir_into_cas(path)
        else:
            cc.put_file_into_cas(path)


def main(prog: str, args: list[str]):
    desc = "Put files into Cascadis."
    ap = argparse.ArgumentParser(prog=prog, description=desc)
    ap.add_argument(
        "-c",
        "--concurrency",
        type=int,
        help="number of threads",
    )
    ap.add_argument(
        "-D",
        "--delete",
        action="store_true",
        help="delete source files",
    )
    ap.add_argument(
        "files",
        metavar="path",
        nargs="*",
        help="source file",
    )
    ns = ap.parse_args(args)
    cc = _CommandContext(delete=ns.delete, concurrency=ns.concurrency)
    cc.run(ns.files)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
