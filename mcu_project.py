#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys


REQUIRED_TOOLS = [
    "arm-none-eabi-gcc",
    "arm-none-eabi-objcopy",
    "arm-none-eabi-size",
    "arm-none-eabi-gdb",
    "cmake",
    "ninja",
    "openocd",
]


def check_tool(name: str) -> str | None:
    return shutil.which(name)






def writing_file(path):

    cmake_file =  r"""
cmake_minimum_required(VERSION 3.20)

# --- Config toolchain (doit être AVANT project()) ---
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER   arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER arm-none-eabi-gcc)
set(CMAKE_OBJCOPY      arm-none-eabi-objcopy)
set(CMAKE_SIZE         arm-none-eabi-size)

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# --- Projet (STM32F103CBT6 — Cortex-M3) ---
project(firmware C ASM)

set(CPU_FLAGS "-mcpu=cortex-m3 -mthumb")

set(CMAKE_C_FLAGS "${CPU_FLAGS} -Wall -Wextra -ffunction-sections -fdata-sections -O0 -g")
set(CMAKE_ASM_FLAGS "${CPU_FLAGS}")

set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/linker.ld)

# Pas de -T ici — il est ajouté une seule fois via target_link_options plus bas
set(CMAKE_EXE_LINKER_FLAGS
    "${CPU_FLAGS} -nostdlib -Wl,--gc-sections -Wl,-Map=firmware.map"
)

# --- Sources ---
file(GLOB SOURCES CONFIGURE_DEPENDS "src/*.c")

if(NOT SOURCES)
    message(FATAL_ERROR "Aucun fichier .c trouvé dans src/ — vérifie le chemin.")
endif()

message(STATUS "Fichiers sources trouvés : ${SOURCES}")

add_executable(firmware
    startup.s
    ${SOURCES}
)

target_link_options(firmware PRIVATE -T${LINKER_SCRIPT})

# --- Post-build : génère le .bin et affiche la taille flash/RAM ---
add_custom_command(TARGET firmware POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary firmware firmware.bin
    COMMAND ${CMAKE_SIZE} firmware
)

# --- Target de flash via OpenOCD (ST-Link, STM32F1) ---
find_program(OPENOCD openocd REQUIRED)

add_custom_target(flash
    COMMAND ${OPENOCD} -f interface/stlink.cfg -f target/stm32f1x.cfg
            -c "program firmware.bin 0x08000000 verify reset exit"
    DEPENDS firmware
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)


"""

    startup_file = r"""
    .syntax unified
    .cpu cortex-m3
    .thumb

    /* Symboles fournis par le linker script */
    .word _sidata
    .word _sdata
    .word _edata
    .word _sbss
    .word _ebss

        .section .text.Reset_Handler
        .weak Reset_Handler
        .type Reset_Handler, %function
    Reset_Handler:
        /* Copie .data de la flash vers la RAM */
        ldr r0, =_sdata
        ldr r1, =_edata
        ldr r2, =_sidata
        movs r3, #0
        b LoopCopyDataInit

    CopyDataInit:
        ldr r4, [r2, r3]
        str r4, [r0, r3]
        adds r3, r3, #4

    LoopCopyDataInit:
        adds r4, r0, r3
        cmp r4, r1
        bcc CopyDataInit

        /* Met .bss à zéro */
        ldr r2, =_sbss
        ldr r4, =_ebss
        movs r3, #0
        b LoopFillZerobss

    FillZerobss:
        str r3, [r2]
        adds r2, r2, #4

    LoopFillZerobss:
        cmp r2, r4
        bcc FillZerobss

        /* Appel du programme principal */
        bl main
        b Infinite_Loop

    Infinite_Loop:
        b Infinite_Loop
        .size Reset_Handler, .-Reset_Handler

    /* Handler par défaut pour tout ce qui n'est pas défini ailleurs */
        .section .text.Default_Handler,"ax",%progbits
    Default_Handler:
    Infinite_Loop_Default:
        b Infinite_Loop_Default
        .size Default_Handler, .-Default_Handler

    /* Table des vecteurs */
        .section .isr_vector,"a",%progbits
        .type g_pfnVectors, %object
        .size g_pfnVectors, .-g_pfnVectors

    g_pfnVectors:
        .word _estack
        .word Reset_Handler
        .word NMI_Handler
        .word HardFault_Handler
        .word MemManage_Handler
        .word BusFault_Handler
        .word UsageFault_Handler
        .word 0
        .word 0
        .word 0
        .word 0
        .word SVC_Handler
        .word DebugMon_Handler
        .word 0
        .word PendSV_Handler
        .word SysTick_Handler
        /* IRQ périphériques à rajouter au besoin (EXTI, USART, TIM, etc.) */

    /* Alias vers Default_Handler pour tous les handlers non redéfinis */
        .weak NMI_Handler
        .thumb_set NMI_Handler,Default_Handler

        .weak HardFault_Handler
        .thumb_set HardFault_Handler,Default_Handler

        .weak MemManage_Handler
        .thumb_set MemManage_Handler,Default_Handler

        .weak BusFault_Handler
        .thumb_set BusFault_Handler,Default_Handler

        .weak UsageFault_Handler
        .thumb_set UsageFault_Handler,Default_Handler

        .weak SVC_Handler
        .thumb_set SVC_Handler,Default_Handler

        .weak DebugMon_Handler
        .thumb_set DebugMon_Handler,Default_Handler

        .weak PendSV_Handler
        .thumb_set PendSV_Handler,Default_Handler

        .weak SysTick_Handler
        .thumb_set SysTick_Handler,Default_Handler
    """

    linker_file = r"""
    ENTRY(Reset_Handler)

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 128K
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 20K
}

_estack = ORIGIN(RAM) + LENGTH(RAM);

SECTIONS
{
    .isr_vector :
    {
        . = ALIGN(4);
        KEEP(*(.isr_vector))
        . = ALIGN(4);
    } >FLASH

    .text :
    {
        . = ALIGN(4);
        *(.text)
        *(.text*)
        *(.rodata)
        *(.rodata*)
        . = ALIGN(4);
    } >FLASH

    _sidata = LOADADDR(.data);

    .data :
    {
        . = ALIGN(4);
        _sdata = .;
        *(.data)
        *(.data*)
        . = ALIGN(4);
        _edata = .;
    } >RAM AT> FLASH

    .bss :
    {
        . = ALIGN(4);
        _sbss = .;
        *(.bss)
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
    } >RAM

    ._user_heap_stack :
    {
        . = ALIGN(8);
        end = .;
        . = . + 0x400; /* espace mini réservé pour heap+stack, ajustable */
        . = ALIGN(8);
    } >RAM
}
"""

    main_file = r"""
    int main(void){
        return 0;
    }

"""

    for file in path.rglob("*.txt"):
        Path(file).write_text(cmake_file, encoding="utf-8")

    for file in path.rglob("*.s"):
        Path(file).write_text(startup_file, encoding="utf-8")

    for file in path.rglob("*.ld"):
        Path(file).write_text(linker_file, encoding="utf-8")

    for file in path.rglob("*.c"):
        Path(file).write_text(main_file, encoding="utf-8")

    print("File ready !")



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
        (path / "CMakeLists.txt").touch()
        (path / "linker.ld").touch()
        (path / "startup.s").touch()
        (path / "src").mkdir()
        (path / "build").mkdir()
        (path / "src" / "main.c").touch()

        print(f"project '{path}' created successfully")
        writing_file(path)

    except FileExistsError:

        print(f"Directory '{path}' already exists.")

    except PermissionError:

        print(f"Permission denied: Unable to create '{path}'.")

    except Exception as e:

        print(f"An error occurred: {e}")




def main():
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
        sys.exit(1)
        return
    else:
        print("\n Tools Ready !")
        creating_project()

main()











