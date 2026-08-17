# esp32-gdb-mqtt Test Bitstreams

Pre-built bitstreams and RISC-V test binaries for use with [esp32-gdb-mqtt](https://github.com/EldritchJS/esp32-gdb-mqtt).

## Bitstream

- `tang-primer-25k/sipeed_tang_primer_25k.fs` — LiteX SoC with VexRiscv CPU for the Sipeed Tang Primer 25K. Built with LiteX, targets Gowin GW5A-25.

### Flashing

Requires [openFPGALoader](https://github.com/trabucayre/openFPGALoader) with XTX XT25F64B flash support (JEDEC 0x0b4017). See the main repo's `docs/fpga-toolchain-setup.md` for the patch.

```bash
# SRAM (volatile)
openFPGALoader -b tangprimer25k tang-primer-25k/sipeed_tang_primer_25k.fs

# Persistent flash
openFPGALoader -b tangprimer25k -f tang-primer-25k/sipeed_tang_primer_25k.fs
```

## Test Binaries

RISC-V bare-metal binaries for the VexRiscv soft CPU. Upload to the ESP32 via the file manager, then load with `monitor riscv_load <name>`.

| Binary | Size | Behavior |
|--------|------|----------|
| `riscv/hello.bin` | 87 B | Prints "Hello from VexRiscv!" to UART, then spins |
| `riscv/count.bin` | 184 B | Prints incrementing hex counter to UART every ~0.5s |

Output is visible on `device/<id>/console/out` via the UART relay.

### Building

Requires a RISC-V GCC toolchain (`riscv64-elf-gcc` or similar):

```bash
cd riscv
make
```

## Rebuilding the Bitstream

```bash
source ~/fpga/oss-cad-suite/environment
python3 build_soc_tang.py
```
