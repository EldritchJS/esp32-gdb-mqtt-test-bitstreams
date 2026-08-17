CROSS = riscv64-elf-
CC = $(CROSS)gcc
OBJCOPY = $(CROSS)objcopy

CFLAGS = -march=rv32im -mabi=ilp32 -nostdlib -nostartfiles -T link.ld
TARGETS = hello.bin count.bin

all: $(TARGETS)

%.elf: %.S link.ld
	$(CC) $(CFLAGS) -o $@ $<

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@

clean:
	rm -f *.elf *.bin

.PHONY: all clean
