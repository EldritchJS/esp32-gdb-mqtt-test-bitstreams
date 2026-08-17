ENTRY(_start)

MEMORY {
    SRAM (rwx) : ORIGIN = 0x10000000, LENGTH = 8K
}

SECTIONS {
    .text : { *(.text*) } > SRAM
    .rodata : { *(.rodata*) } > SRAM
    .data : { *(.data*) } > SRAM
    .bss : { *(.bss*) *(COMMON) } > SRAM
}
