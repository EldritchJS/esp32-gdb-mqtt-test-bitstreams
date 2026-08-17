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

## Test Binaries (Phase 3)

RISC-V binaries for the VexRiscv soft CPU, loaded via the esp32-gdb-mqtt file manager:

- `riscv/blink0.bin` — LED 0 slow blink (TBD)
- `riscv/blink1.bin` — LED 1 double blink (TBD)
- `riscv/hello.bin` — UART hello + LED cycle (TBD)

These will be built when Phase 3 (ESP32 + FPGA integration) begins.
