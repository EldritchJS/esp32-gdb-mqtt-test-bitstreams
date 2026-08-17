#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.expanduser("~/fpga/litex-boards"))

from migen import *
from litex.build.generic_platform import Subsignal, Pins, IOStandard
import litex_boards.platforms.sipeed_tang_primer_25k as tang_platform
from litex_boards.targets.sipeed_tang_primer_25k import BaseSoC
from litex.soc.integration.builder import Builder
from litex.soc.cores.led import LedChaser
from litex.soc.cores.cpu.vexriscv_smp.core import VexRiscvSMP

for i, io in enumerate(tang_platform._dock_io):
    if io[0] == "serial":
        tang_platform._dock_io[i] = ("serial", 0,
            Subsignal("rx", Pins("j4:5")),
            Subsignal("tx", Pins("j4:4")),
            IOStandard("LVCMOS33"),
        )
        break

VexRiscvSMP.privileged_debug = True
VexRiscvSMP.hardware_breakpoints = 0
VexRiscvSMP.jtag_tap = True
VexRiscvSMP.dcache_size = 2048
VexRiscvSMP.icache_size = 2048

class TestSoC(BaseSoC):
    def __init__(self, **kwargs):
        kwargs["with_led_chaser"] = False
        super().__init__(**kwargs)

        platform = self.platform

        chaser_pads = platform.request_all("led")
        self.led_chaser = LedChaser(pads=chaser_pads, sys_clk_freq=self.sys_clk_freq)

        _jtag_io = [
            ("jtag", 0,
                Subsignal("tck", Pins("j4:0")),
                Subsignal("tdi", Pins("j4:1")),
                Subsignal("tdo", Pins("j4:2")),
                Subsignal("tms", Pins("j4:3")),
                IOStandard("LVCMOS33"),
            )
        ]
        platform.add_extension(_jtag_io)
        jtag_pads = platform.request("jtag")
        self.cpu.add_jtag(jtag_pads)
        platform.add_false_path_constraints(self.crg.cd_sys.clk, jtag_pads.tck)

soc = TestSoC(
    sys_clk_freq        = 50e6,
    cpu_type            = "vexriscv_smp",
    cpu_variant         = "standard",
    integrated_rom_size = 0x20000,
    toolchain           = "apicula",
)

soc.platform.toolchain._synth_opts += " -family gw5a -nolutram"
# nextpnr only supports sspi_as_gpio and i2c_as_gpio as --vopt; gowin_pack checks
# that these match between nextpnr's routed JSON and its own flags.
soc.platform.toolchain._pnr_opts += " --vopt sspi_as_gpio --vopt i2c_as_gpio "
# GW5A-25A also requires sspi_as_gpio in gowin_pack (platform only sets mspi)
soc.platform.toolchain.options["use_sspi_as_gpio"] = 1

build_dir = os.path.expanduser("~/fpga/build/tang-primer-25k-soc")
builder = Builder(soc, output_dir=build_dir)
builder.build(run=False)

gw_dir = os.path.join(build_dir, "gateware")
for fname in os.listdir(gw_dir):
    if fname.startswith("VexRiscvLitexSmpCluster") and fname.endswith(".v"):
        path = os.path.join(gw_dir, fname)
        with open(path, "r") as f:
            text = f.read()
        text = text.replace('(* ram_style = "distributed" *) ', '')
        with open(path, "w") as f:
            f.write(text)
        print(f"Stripped ram_style from {fname}")

import subprocess
subprocess.check_call(["bash", "build_sipeed_tang_primer_25k.sh"], cwd=gw_dir)
print("Build complete")
