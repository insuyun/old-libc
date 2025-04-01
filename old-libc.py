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
        print("[-] GLIBC_VERSION environment variable is not set")
        sys.exit(1)


    for version in _get_glibc_versions():
        if version.startswith(glibc_version):
            _download_glibc(version)
            return version

    print(f"[-] GLIBC_VERSION is not valid: {glibc_version}")
    print(f"\tValid versions:")
    for version in _get_glibc_versions():
        print(f"\t\t{version}")
    sys.exit(1)

def _get_target_file(args):
    for arg in args:
        if arg.endswith(".c"):
            copy = args.copy()
            copy.remove(arg)
            return arg, copy

    print("[-] Target file is not provided")
    sys.exit(1)

def _sanity_check(args):
    if "-no-pie" not in args:
        print("[-] PIE is not supported (-no-pie is required)")
        sys.exit(1)

def main():
    glibc_version = _get_glibc_version()
    lib_dir = GLIBC_ALL_IN_ONE / "libs" / glibc_version
    dev_dir = GLIBC_ALL_IN_ONE / "libs" / glibc_version / ".dev"

    args = sys.argv[1:]
    target_file, args = _get_target_file(args)
    _sanity_check(args)

    cmd = (["gcc",
        "-fcf-protection=none",
        "-nostartfiles",
        "-Wl,--start-group",
        f"{dev_dir}/crt1.o",
        f"{dev_dir}/crti.o",
        f"{dev_dir}/libc_nonshared.a",
        target_file,
        f"{dev_dir}/crtn.o",
        "-Wl,--end-group",
        "-Xlinker", "-rpath", f"{lib_dir}",
        "-Xlinker", "-I", f"{lib_dir}/ld-linux-x86-64.so.2",
        "-Xlinker", f"{lib_dir}/libc.so.6",
        "-Xlinker", f"{lib_dir}/libdl.so.2"]
        + args
    )

    print(f"[*] Running command: {' '.join(cmd)}")
    print()
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()