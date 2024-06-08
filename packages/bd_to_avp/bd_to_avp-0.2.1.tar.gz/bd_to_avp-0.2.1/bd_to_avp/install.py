import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests

from bd_to_avp.modules.config import config
from bd_to_avp.modules.util import run_command


def prompt_for_password() -> Path:
    script = f"""
    with timeout of 3600 seconds
        tell app "System Events"
            activate
            set pw to text returned of (display dialog "Enter your password: (This will take a while)" default answer "" with hidden answer)
        end tell
        return pw
    end timeout
    """
    with tempfile.NamedTemporaryFile(suffix=".sh", delete=False) as pw_file:
        pw_file.write('#!/bin/bash\necho "$HOMEBREW_PASSOWRD"\n'.encode())
        pw_file_path = Path(pw_file.name)
    pw_file_path.chmod(0o700)
    password_correct = False
    while not password_correct:
        password = subprocess.check_output(
            ["osascript", "-e", script], text=True
        ).strip()

        os.environ["HOMEBREW_PASSOWRD"] = password

        os.environ["SUDO_ASKPASS"] = pw_file_path.as_posix()
        check_sudo_password = subprocess.run(
            ["/usr/bin/sudo", "-A", "ls"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=password,
        )
        password_correct = check_sudo_password.returncode == 0
    return pw_file_path


def install_deps(is_gui: bool) -> None:
    if not is_arm64():
        raise ValueError("This script is only supported on Apple Silicon Macs.")
    print("Installing dependencies...")
    pw_file_path = None

    if is_gui:
        pw_file_path = prompt_for_password()

    if not Path("/opt/homebrew/bin/brew").exists():
        install_brew(is_gui)
    else:
        update_brew(is_gui)

    Path("/Applications/Makemkv.app").unlink(missing_ok=True)
    Path("/Applications/Wine Stable.app").unlink(missing_ok=True)

    for package in config.BREW_CASKS_TO_INSTALL:
        manage_brew_package(package, is_gui, True, "uninstall")
        manage_brew_package(package, is_gui, True)

    for package in config.BREW_PACKAGES_TO_INSTALL:
        manage_brew_package(package, is_gui)

    check_mp4box(is_gui)

    wine_boot()

    if pw_file_path:
        pw_file_path.unlink()


def check_mp4box(is_gui: bool) -> None:
    if not config.MP4BOX_PATH.exists() or not check_mp4box_version(
        config.MP4BOX_VERSION
    ):
        if config.MP4BOX_PATH.exists():
            print("Removing old MP4Box...")
            shutil.rmtree("/Applications/GPAC.app", ignore_errors=True)
        print("Installing MP4Box...")
        install_mp4box(is_gui)


def check_install_version() -> bool:
    installed_version = config.load_version()
    print(
        f"Installed bd-to-avp version: {installed_version}\nbd-to-avp version: {config.code_version}"
    )
    if installed_version == config.code_version:
        return True

    return False


def show_message(title: str, message: str) -> None:
    script = f"""
    tell app "System Events"
        display dialog "{message}" buttons {{"OK"}} default button "OK" with title "{title}" with icon caution
    end tell
    """
    subprocess.call(["osascript", "-e", script])


def on_error_process(
    package: str, process: subprocess.CompletedProcess, is_gui: bool
) -> None:
    command = (
        " ".join(process.args) if isinstance(process.args, list) else str(process.args)
    )
    if is_gui:
        show_message(
            f"Failed {package} processing",
            f"Command:{command}\nOutput:{process.stderr}\nError:{process.stdout}",
        )
    raise subprocess.CalledProcessError(
        process.returncode,
        command,
        output=process.stdout,
        stderr=process.stderr,
    )


def on_error_string(package: str, error: str, is_gui: bool) -> None:
    if is_gui:
        show_message(f"Failed to install {package}.", error)
    raise ValueError(error)


def is_arm64() -> bool:
    return platform.machine() == "arm64"


def manage_brew_package(
    package: str, is_gui: bool, cask: bool = False, operation: str = "install"
) -> None:
    print(f"{operation.title()}ing {package}...")
    brew_command = ["/opt/homebrew/bin/brew", operation]
    if operation == "install":
        brew_command.append("--no-quarantine")
        app_dir_path = next(
            Path("/Applications").glob(f"{package.replace('-', ' ')}.app"), None
        )
        if app_dir_path and app_dir_path.is_dir():
            shutil.rmtree(app_dir_path, ignore_errors=True)
            print(f"Removed existing application: {app_dir_path}")

    if cask:
        brew_command.append("--cask")
    brew_command.append(package)

    process = subprocess.run(
        brew_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if operation == "uninstall" and process.returncode == 1:
        print(f"{package} not installed.")
        return

    if process.returncode != 0:
        on_error_process(package, process, is_gui)

    print(f"{package} {operation}ed.")


def update_brew(is_gui: bool) -> None:
    print("Updating Homebrew...")
    brew_command = ["/opt/homebrew/bin/brew", "update"]
    process = subprocess.run(
        brew_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        on_error_process("Homebrew", process, is_gui)
    print("Homebrew updated.")


def check_mp4box_version(version: str) -> bool:
    processs = subprocess.run(
        [config.MP4BOX_PATH, "-version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return version in processs.stdout


def install_mp4box(is_gui: bool) -> None:
    print("Installing MP4Box...")
    sudo_env = os.environ.copy()

    command = [
        "sudo",
        "installer",
        "-pkg",
        (config.SCRIPT_PATH / "installers" / "gpac-2.2.1.pkg").as_posix(),
        "-target",
        "/",
    ]
    process = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=sudo_env,
    )

    if process.returncode != 0:
        on_error_process("MP4Box", process, is_gui)
    print("MP4Box installed.")


def wine_boot() -> None:
    print("Booting Wine...")
    process = subprocess.run(
        [(config.HOMEBREW_PREFIX_BIN / "wineboot").as_posix()],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        on_error_process("Wine", process, False)
    print("Wine booted.")


def install_brew(is_gui: bool) -> None:
    print("Installing Homebrew for arm64...")

    response = requests.get(
        "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    )
    if response.status_code != 200:
        on_error_string(
            "Homebrew", "Failed to download Homebrew install script.", is_gui
        )
    brew_install_script = response.text

    with tempfile.NamedTemporaryFile(suffix=".sh", delete=False) as brew_install_file:
        brew_install_file.write(brew_install_script.encode())
        brew_install_file_path = Path(brew_install_file.name)

    brew_install_command = ["/bin/bash", brew_install_file_path.as_posix()]
    process = subprocess.run(
        brew_install_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        on_error_process("Homebrew", process, is_gui)
    print("Homebrew installed.")
    brew_install_file_path.unlink()


def setup_frim() -> None:
    wine_prefix = Path(os.environ.get("WINEPREFIX", "~/.wine")).expanduser()
    frim_destination_path = wine_prefix / "drive_c/UTL/FRIM"

    if frim_destination_path.exists():
        print(f"{frim_destination_path} already exists. Skipping install.")
        return

    shutil.copytree(config.FRIM_PATH, frim_destination_path)
    print(f"Copied FRIM directory to {frim_destination_path}")

    reg_file_path = config.FRIM_PATH / "plugins64.reg"
    if not reg_file_path.exists():
        print(f"Registry file {reg_file_path} not found. Skipping registry update.")
        return

    regedit_command = [config.WINE_PATH, "regedit", reg_file_path]
    regedit_env = {"WINEPREFIX": str(wine_prefix)}
    run_command(
        regedit_command, "Update the Windows registry for FRIM plugins.", regedit_env
    )
    print("Updated the Windows registry for FRIM plugins.")
