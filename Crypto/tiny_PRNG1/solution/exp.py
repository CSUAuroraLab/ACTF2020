#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, z3
from sys import argv
from typing import List
from pwn import (
    process,
    remote,
    log,
    # context
)
from Crypto.Util.number import long_to_bytes
# context.log_level = "DEBUG"
bit64 = 0xffffffffffffffff

def LShL(x, n): return (x << n) & bit64

def xo128(x, y, LShR = lambda x,i: x>>i):
    y ^= x
    return y ^ LShL(y, 14) ^ (LShL(x,55)|LShR(x,9)), (LShL(y,36)|LShR(y,28))

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
    log.info("get output")
    out = get_output(io, 10)
    x0, y0 = z3.BitVecs('x0 y0', 64)
    x, y = x0, y0
    s = z3.SimpleSolver()
    
    for v in out:
        s.add((x + y) & bit64 == v)
        x, y = xo128(x, y, z3.LShR)
    
    ans = []

    for i in range(1, sys.maxsize):
        if s.check().r != 1: break  # quit if failed
        soln = s.model()
        x, y = (soln[i].as_long() for i in (x0,y0))
        ans += ["ACTF{" 
            + long_to_bytes(x).decode("utf-8")[::-1]
            + long_to_bytes(y).decode("utf-8")[::-1]
            + "}"]
        for j in range(10):
            x, y = xo128(x, y)
        s.add( z3.Or(x0 != soln[x0], y0 != soln[y0]) )
    
    for a in ans:
        log.info("possible flag: " + a)

if __name__ == "__main__":
    main()


