
# mcu

A command-line tool that generates a bare-metal STM32F103CBT6 project (startup.s, linker.ld, CMakeLists.txt) and builds and flashes it. It checks for the required tools (ARM toolchain, CMake, Ninja, OpenOCD) and can install any that are missing.

## Requirements

- `Python 3.10+`
- `arm-none-eabi-gcc`, `arm-none-eabi-objcopy`, `arm-none-eabi-size`, `arm-none-eabi-gdb` (ARM toolchain)
- `cmake`
- `ninja`
- `openocd`
- A ST-Link probe to flash the board

Only Python has to be installed beforehand: if other tools are missing, `mcu` offers to install them with your package manager (`pacman`, `apt`, `dnf`, `zypper` or `apk`), using `sudo`.

## Installation

```bash
git clone https://github.com/yunis974/Script_stm32.git
cd Script_stm32
chmod +x install.sh
./install.sh
```

The install script:
- Creates `~/.local/bin` if it doesn't exist
- Removes the old `mcuProjectInit` command if it is still there
- Copies `mcu_project.py` to `~/.local/bin/mcu` and makes it executable
- Copies the project templates to `~/.local/share/mcu/data`
- Offers to add `~/.local/bin` to your PATH if it is missing

## Make sure `~/.local/bin` is in your PATH

If you accepted the installer's prompt, reload your shell:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

If you declined it, add this line to your `~/.bashrc` or `~/.zshrc` first:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

### Create a project

```bash
mcu
```

The command first checks that all required tools are installed. If some are missing, it offers to install them and stops; run `mcu` again afterwards.

It then prompts you for:
- The project name
- Where to create it (home directory with `y`, or a custom path with `n`)

It generates the following structure:

```
my_project/
├── CMakeLists.txt
├── linker.ld
├── startup.s
├── include/
└── src/
    └── main.c
```

### Build and flash

Run these commands from the root of the generated project:

| Command        | Action                                                 |
| -------------- | ------------------------------------------------------ |
| `mcu -t`       | Check the toolchain                                    |
| `mcu -r`       | Refresh the project: delete `build/` and rerun CMake   |
| `mcu -b`       | Build the project, configuring it first if needed      |
| `mcu -f`       | Flash the project                                      |
| `mcu -b -f`    | Build and flash                                        |
| `mcu -r -b`    | Refresh and build                                      |
| `mcu -r -b -f` | Refresh, build and flash                               |

Long options are also available: `--tools`, `--refresh`, `--build` and `--flash`. Run `mcu -h` to see the help.

## Uninstall

```bash
rm ~/.local/bin/mcu
rm -r ~/.local/share/mcu
```
