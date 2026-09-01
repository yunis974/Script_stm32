
# scriptInit

A script that automatically generates a bare-metal STM32F103CBT6 project (startup.s, linker.ld, CMakeLists.txt) with a check for required tools (ARM toolchain, CMake, Ninja, OpenOCD).

## Requirements

- `arm-none-eabi-gcc` (ARM toolchain)
- `cmake`
- `ninja`
- `openocd`
- `Python 3`

## Installation

```bash
git clone https://github.com/yunis974/Script_stm32.git
cd Script_stm32
chmod +x install.sh
./install.sh
```

The install script:
- Creates `~/.local/bin` if it doesn't exist
- Copies `mcu_project.py` to `~/.local/bin/mcuProjectInit`
- Makes it executable

## Make sure `~/.local/bin` is in your PATH

If the installer prints a warning, add this line to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

## Usage

```bash
mcuProjectInit
```

The script first checks that all required tools are installed, then prompts you for:
- The project name
- Where to create it (home directory by default, or a custom path)

It then generates the following structure:

my_project/
├── CMakeLists.txt
├── linker.ld
├── startup.s
├── build/
└── src/
└── main.c


## Building and flashing the generated project

```bash
cd my_project
cmake -G Ninja -S . -B build
cmake --build build
cmake --build build --target flash
```

## Uninstall

```bash
rm ~/.local/bin/mcuProjectInit
```