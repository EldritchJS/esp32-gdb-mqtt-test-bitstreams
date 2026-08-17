/* count.S — Print incrementing hex counter to LiteX UART in a loop.
 * Useful for verifying halt/resume: counter advances while running,
 * stops when halted, resumes from where it left off. */

#define UART_RXTX    0xf0002800
#define UART_TXFULL  0xf0002804

.section .text
.globl _start
_start:
    li   s0, 0            /* counter */
loop:
    mv   a0, s0
    call print_hex
    li   a0, '\r'
    call putc
    li   a0, '\n'
    call putc
    call delay
    addi s0, s0, 1
    j    loop

/* putc: send byte in a0 to UART */
putc:
    li   t0, UART_RXTX
    li   t1, UART_TXFULL
1:  lw   t2, 0(t1)
    bnez t2, 1b
    sw   a0, 0(t0)
    ret

/* print_hex: print 32-bit value in a0 as "0x" + 8 hex digits */
print_hex:
    addi sp, sp, -8
    sw   ra, 4(sp)
    sw   s1, 0(sp)
    mv   s1, a0
    li   a0, '0'
    call putc
    li   a0, 'x'
    call putc
    li   t3, 28            /* shift amount, 28 down to 0 */
1:  srl  a0, s1, t3
    andi a0, a0, 0xf
    li   t4, 10
    blt  a0, t4, 2f
    addi a0, a0, ('a' - 10)
    j    3f
2:  addi a0, a0, '0'
3:  call putc
    addi t3, t3, -4
    bgez t3, 1b
    lw   ra, 4(sp)
    lw   s1, 0(sp)
    addi sp, sp, 8
    ret

/* delay: busy-wait roughly 0.5s at 50 MHz */
delay:
    li   t0, 5000000
1:  addi t0, t0, -1
    bnez t0, 1b
    ret
