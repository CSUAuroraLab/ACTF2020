#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from typing import List
from tqdm import tqdm
from mt19937 import clone_mt19937
import re 
from pwn import (
    process,
    remote,
    log,
    # context
)
# context.log_level = "DEBUG"


def get_output(io, size):
    output = []
    with tqdm(total=size) as bar:
        while len(output) < size:
            io.sendlineafter("> ", "1")
            line = io.recvline().decode("utf-8")
            output += list(map(int, line.strip().split(" ")))
            bar.update(10)
    bar.close()
    return output

def main():
    if len(argv) == 1:
        io = process("./a.out")
    else:
        io = remote(argv[1], int(argv[2]))
    log.info("get output from mt19937")
    out = get_output(io, 640)
    log.info("clone mt19937 from output")
    new_iter = iter(clone_mt19937(out))
    io.sendline("2")
    log.info("send answer")
    io.sendline(str(next(new_iter)))
    s = str(io.recvuntil("4) "))
    s = str(io.recvuntil("4) "))
    log.success(re.search("ACTF{.*}", s).group(0))

if __name__ == "__main__":
    main()