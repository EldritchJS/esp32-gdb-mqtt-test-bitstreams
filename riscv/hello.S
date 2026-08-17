/* hello.S — Print a message to LiteX UART, then spin */

#define UART_RXTX    0xf0002800
#define UART_TXFULL  0xf0002804

.section .text
.globl _start
_start:
    la   a0, msg
    call puts
spin:
    j    spin

puts:
    li   t0, UART_RXTX
    li   t1, UART_TXFULL
1:  lbu  a1, 0(a0)
    beqz a1, 3f
2:  lw   t2, 0(t1)
    bnez t2, 2b
    sw   a1, 0(t0)
    addi a0, a0, 1
    j    1b
3:  ret

.section .rodata
msg:
    .asciz "Hello from VexRiscv!\r\n"
