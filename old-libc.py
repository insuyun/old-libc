#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

from pathlib import Path

GLIBC_ALL_IN_ONE  = Path(__file__).parent / "glibc-all-in-one"

def _get_glibc_versions():
    glibc_list = Path(GLIBC_ALL_IN_ONE / "list")
    if not glibc_list.exists():
        subprocess.run([
            "python2", "update_list"
        ], cwd=GLIBC_ALL_IN_ONE)

    return glibc_list.read_text().splitlines()

def _download_glibc(version):
    subprocess.run([
        "./download", version
    ], cwd=GLIBC_ALL_IN_ONE)

def _get_glibc_version():
    glibc_version = os.environ.get("GLIBC_VERSION")
    if not glibc_version:
        raise ValueError("GLIBC_VERSION is not set")


    for version in _get_glibc_versions():
        if version.startswith(glibc_version):
            _download_glibc(version)
            return version

    raise ValueError(f"GLIBC_VERSION is not valid: {glibc_version}")

def main():
    glibc_version = _get_glibc_version()
    cmd = (["gcc"] + sys.argv[1:] + [
        "-Xlinker", "-rpath", f"{GLIBC_ALL_IN_ONE}/libs/{glibc_version}",
        "-Xlinker", "-I", f"{GLIBC_ALL_IN_ONE}/libs/{glibc_version}/ld-linux-x86-64.so.2",
        "-Xlinker", f"{GLIBC_ALL_IN_ONE}/libs/{glibc_version}/libc.so.6",
        "-Xlinker", f"{GLIBC_ALL_IN_ONE}/libs/{glibc_version}/libdl.so.2",
    ])

    print(f"[*] Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()