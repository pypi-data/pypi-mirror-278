import os
import sys
import argparse
import platform
import subprocess

from send_s3.config import CONFIG_SOURCE_PATH
from send_s3.common import PROG, MACOS_HELPER_URL, LINESEP, Console, app_directory


def install_config():
    config_file = app_directory("config.toml")
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    if not os.path.exists(config_file):
        with open(CONFIG_SOURCE_PATH, 'r', encoding='utf-8') as f:
            config_content = f.read()
        with open(config_file, 'w+', encoding='utf-8') as f:
            f.write(config_content)
    Console() >> f"Configuration file installed at '{config_file}'" >> LINESEP >> sys.stdout
    Console() >> f"Please edit the configuration file before using {PROG}" >> LINESEP >> sys.stdout


def install_windows_shortcut():
    binary_path = os.path.join(os.path.dirname(sys.argv[0]), f"{PROG}.exe")
    script = f"""
    $shortcut = (New-Object -COM WScript.Shell).CreateShortcut("$($env:APPDATA)\\Microsoft\\Windows\\SendTo\\Send S3.lnk")
    $shortcut.TargetPath = "{binary_path}"
    $shortcut.Arguments = "upload --windows-sendto"
    $shortcut.Save()
    """
    result = subprocess.run(["powershell", script], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    Console() >> "Windows SendTo shortcut installed." >> LINESEP >> sys.stdout


def show_macos_shortcut_prompt():
    Console() >> f"Obtain the helper 'Shortcut' from: {MACOS_HELPER_URL}" >> LINESEP >> sys.stdout


def main(_args: argparse.Namespace) -> int:
    if platform.system() == "Windows":
        install_windows_shortcut()
    if platform.system() == "Darwin":
        show_macos_shortcut_prompt()
    install_config()
    return 0


def register_arguments(_parser: argparse.ArgumentParser):
    pass


__all__ = ['main', 'register_arguments']
