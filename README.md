# scriptInit

A script that automatically generates a bare-metal STM32F103CBT6 project (startup.s, linker.ld, CMakeLists.txt) with a check for required tools (ARM toolchain, CMake, Ninja, OpenOCD).

## Requirements

- `arm-none-eabi-gcc` (ARM toolchain)
- `cmake`
- `ninja`
- `openocd`
- Python 3

## Installation

```bash
git clone https://github.com/your-user/mon-script-stm32.git
cd mon-script-stm32
chmod +x install.sh
./install.sh
```

The install script:
- Creates `~/.local/bin` if it doesn't exist
- Copies `mcu_project.py` to `~/.local/bin/scriptInit`
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
scriptInit
```

The script first checks that all required tools are installed, then prompts you for:
- The project name
- Where to create it (home directory by default, or a custom path)

It then generates the following structure: