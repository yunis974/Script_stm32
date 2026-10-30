#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys
import os
import subprocess
import argparse
from argparse import Namespace


REQUIRED_TOOLS = [
    "arm-none-eabi-gcc",
    "arm-none-eabi-objcopy",
    "arm-none-eabi-size",
    "arm-none-eabi-gdb",
    "cmake",
    "ninja",
    "openocd",
]

PM = {
    "pacman": "pacman -S --needed --noconfirm arm-none-eabi-gcc arm-none-eabi-newlib arm-none-eabi-gdb cmake ninja openocd",
    "apt":    "apt-get install -y gcc-arm-none-eabi libnewlib-arm-none-eabi gdb-multiarch cmake ninja-build openocd",
    "dnf":    "dnf install -y arm-none-eabi-gcc-cs arm-none-eabi-newlib gdb cmake ninja-build openocd",
    "zypper": "zypper install -y cross-arm-none-gcc14 cross-arm-none-newlib-devel gdb cmake ninja openocd",
    "apk":    "apk add gcc-arm-none-eabi newlib-arm-none-eabi gdb-multiarch cmake samurai openocd",
}







def check_tool(name: str) -> str | None:
    return shutil.which(name)

def get_pm() -> str:
    for pm in PM:
        p = shutil.which(pm)
        if p:
            return pm




def creating_project():

    path = Path.home()

    project_name = input("enter project name: ")

    use_home_path = input(
        f"save project in '{Path.home()}' [y/n]: "
    )

    if use_home_path == "n" or use_home_path == "N":

        path = Path(input("enter project path: "))
        path = path / project_name

    elif use_home_path == "y" or use_home_path == "Y":

        path = Path.home()
        path = path / project_name

    try:

        path.mkdir()
        shutil.copytree("data", path, dirs_exist_ok=True)

        print(f"project '{path}' created successfully")

    except FileExistsError:

        print(f"Directory '{path}' already exists.")

    except PermissionError:

        print(f"Permission denied: Unable to create '{path}'.")

    except Exception as e:

        print(f"An error occurred: {e}")



def create_cmd(arr) -> str:
    cmd = ""
    for item in arr:
        cmd = cmd + " " + item
    return cmd
        

def check_toolchains() -> int:
    missing = []
    print("Checking Tools... :\n")

    for tool in REQUIRED_TOOLS:
        path = check_tool(tool)
        if path:
            print(f"  [OK]      {tool:<25} -> {path}")
        else:
            print(f"  [MISSING] {tool}")
            missing.append(tool)

    if missing:
        print(f"\n{len(missing)} Missing tool(s) : {', '.join(missing)}")
        ans = input("Install tools ? [Y/N]")
        if ans == "Y" or ans == "y":
            subprocess.run("sudo " + str(PM[get_pm()]), shell=True)
            #subprocess.run(get_pm() + tool, check=True)
        else:
            pass
        return False
    else:
        print("\n Tools Ready !")
        return True




def refresh_project():
    shutil.rmtree("build", ignore_errors=True)
    subprocess.run(["cmake", "-B", "build", "-G", "Ninja"], check=True)

def build():
    if not os.path.isdir("build"):
        refresh_project()
    subprocess.run(["cmake", "--build", "build"], check=True)

def flash():
    subprocess.run(["cmake", "--build", "build", "--target", "flash"], check=True)

def main():
    parser = argparse.ArgumentParser(
        prog="mcu",
        description="Create an empty program ready to flash !",
        epilog="""
        Exemple:
            mcu    | create a new project
            mcu -b -f | build and flash
        """
    )

    parser.add_argument("-t", "--tools", action="store_true", help="Check toolchain")
    parser.add_argument("-b", "--build", action="store_true", help ="Build project")
    parser.add_argument("-f", "--flash", action="store_true", help ="Flash project" )
    parser.add_argument("-r", "--refresh", action="store_true", help ="Refresh project" )

    args = parser.parse_args()

    match args:
        
        case Namespace(refresh=True, build=True, flash=True):
            refresh_project()
            build()
            flash()
        case Namespace(refresh=True, build=True):
            refresh_project()
            build()
        case Namespace(build=True, flash=True):
            build()
            flash()

        case Namespace(tools=True):
            check_toolchains()
        case Namespace(refresh=True):
            refresh_project()
        case Namespace(build=True):
            build()
        case Namespace(flash=True):
            flash()

        case _:
            if check_toolchains():
                creating_project()

main()

   












