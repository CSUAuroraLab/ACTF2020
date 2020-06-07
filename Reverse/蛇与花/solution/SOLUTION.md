#### SOLUTION



1. python 反编译工具用不了，工具网站用不了，加了混淆，根据工具脚本报错可以得出，Load 了超出常量表大小 index 的常量
   
2. 3 个函数及最外面的代码依次加了花指令混淆，去掉，找出和去除这个过程虽然麻烦但不难

   ```pyc
   `0x71 0x06 0x00 0x64 0xff 0xff`
                 0 JUMP_ABSOLUTE            6
                 3 LOAD_CONST           65535
   
   0 JUMP_ABSOLUTE 4		71 04 00
   3 LOAD_CONST 2417		64 71 09 
   6 STOP_CODE				00 
   7 LOAD_CONST x			64 00 x
   
   `0x71 0x03 0x00`
                 0 JUMP_ABSOLUTE            3
   
   `0x71 0x06 0x00 0x64 0xff 0xff`
                 0 JUMP_ABSOLUTE            6
                 3 LOAD_CONST           65535
   ```

3. 可用反编译工具，也可用工具脚本查看 python 字节码

   ```pyc
   magic 03f30d0a
   moddate b052c65e (Thu May 21 18:06:40 2020)
   code
      argcount 0
      nlocals 0
      stacksize 31
      flags 0040
      code
         640000640100640200640300640400640500640600640700640800640900
         640a00640b00640c00640d00640e00640f00641000641100641200640600
         641300641400641500641600641700641800641900640400641a00641b00
         641c00671f005a0000641d00641e006702005a0100641f008400005a0200
         6420008400005a03006421008400005a04006505008300005a0600650400
         6506008301000164220053
     1           0 LOAD_CONST               0 (0)
                 3 LOAD_CONST               1 (15)
                 6 LOAD_CONST               2 (78)
                 9 LOAD_CONST               3 (6)
                12 LOAD_CONST               4 (54)
                15 LOAD_CONST               5 (27)
                18 LOAD_CONST               6 (26)
                21 LOAD_CONST               7 (14)
                24 LOAD_CONST               8 (34)
                27 LOAD_CONST               9 (92)
                30 LOAD_CONST              10 (58)
                33 LOAD_CONST              11 (68)
                36 LOAD_CONST              12 (23)
                39 LOAD_CONST              13 (133)
                42 LOAD_CONST              14 (90)
                45 LOAD_CONST              15 (79)
                48 LOAD_CONST              16 (94)
                51 LOAD_CONST              17 (93)
                54 LOAD_CONST              18 (137)
                57 LOAD_CONST               6 (26)
                60 LOAD_CONST              19 (106)
                63 LOAD_CONST              20 (97)
                66 LOAD_CONST              21 (55)
                69 LOAD_CONST              22 (91)
                72 LOAD_CONST              23 (49)
                75 LOAD_CONST              24 (103)
                78 LOAD_CONST              25 (105)
                81 LOAD_CONST               4 (54)
                84 LOAD_CONST              26 (40)
                87 LOAD_CONST              27 (37)
                90 LOAD_CONST              28 (115)
                93 BUILD_LIST              31
                96 STORE_NAME               0 (arr1)
   
     2          99 LOAD_CONST              29 (-62)
               102 LOAD_CONST              30 (80)
               105 BUILD_LIST               2
               108 STORE_NAME               1 (arr2)
   
     5         111 LOAD_CONST              31 (<code object encode at 00000000031D6E30, file "./py&flower.py", line 5>)
               114 MAKE_FUNCTION            0
               117 STORE_NAME               2 (encode)
   
    15         120 LOAD_CONST              32 (<code object check at 00000000031D69B0, file "./py&flower.py", line 15>)
               123 MAKE_FUNCTION            0
               126 STORE_NAME               3 (check)
   
    31         129 LOAD_CONST              33 (<code object main at 00000000031D6B30, file "./py&flower.py", line 31>)
               132 MAKE_FUNCTION            0
               135 STORE_NAME               4 (main)
   
    42         138 LOAD_NAME                5 (raw_input)
               141 CALL_FUNCTION            0
               144 STORE_NAME               6 (s)
   
    43         147 LOAD_NAME                4 (main)
               150 LOAD_NAME                6 (s)
               153 CALL_FUNCTION            1
               156 POP_TOP
               157 LOAD_CONST              34 (None)
               160 RETURN_VALUE
      consts
         0
         15
         78
         6
         54
         27
         26
         14
         34
         92
         58
         68
         23
         133
         90
         79
         94
         93
         137
         106
         97
         55
         91
         49
         103
         105
         40
         37
         115
         -62
         80
         code
            argcount 2
            nlocals 5
            stacksize 8
            flags 0043
            code
               7400007401007c00008302007d02006401007d0300786a00740200740300
               7c0100830100830100445d56007d04007c04007403007c02008301006b05
               00724400506e00007c03007404007c02007c0400190f7401007c01007c04
               0019830100407c02007c0400197401007c01007c0400198301000f404283
               0100377d0300712800577c030053
     6           0 LOAD_GLOBAL              0 (map)
                 3 LOAD_GLOBAL              1 (ord)
                 6 LOAD_FAST                0 (s)
                 9 CALL_FUNCTION            2
                12 STORE_FAST               2 (a)
   
     7          15 LOAD_CONST               1 ('')
                18 STORE_FAST               3 (enc)
   
     8          21 SETUP_LOOP             106 (to 130)
                24 LOAD_GLOBAL              2 (range)
                27 LOAD_GLOBAL              3 (len)
                30 LOAD_FAST                1 (key)
                33 CALL_FUNCTION            1
                36 CALL_FUNCTION            1
                39 GET_ITER
           >>   40 FOR_ITER                86 (to 129)
                43 STORE_FAST               4 (i)
   
     9          46 LOAD_FAST                4 (i)
                49 LOAD_GLOBAL              3 (len)
                52 LOAD_FAST                2 (a)
                55 CALL_FUNCTION            1
                58 COMPARE_OP               5 (>=)
                61 POP_JUMP_IF_FALSE       68
   
    10          64 BREAK_LOOP
                65 JUMP_FORWARD             0 (to 68)
   
    11     >>   68 LOAD_FAST                3 (enc)
                71 LOAD_GLOBAL              4 (chr)
                74 LOAD_FAST                2 (a)
                77 LOAD_FAST                4 (i)
                80 BINARY_SUBSCR
                81 UNARY_INVERT
                82 LOAD_GLOBAL              1 (ord)
                85 LOAD_FAST                1 (key)
                88 LOAD_FAST                4 (i)
                91 BINARY_SUBSCR
                92 CALL_FUNCTION            1
                95 BINARY_AND
                96 LOAD_FAST                2 (a)
                99 LOAD_FAST                4 (i)
               102 BINARY_SUBSCR
               103 LOAD_GLOBAL              1 (ord)
               106 LOAD_FAST                1 (key)
               109 LOAD_FAST                4 (i)
               112 BINARY_SUBSCR
               113 CALL_FUNCTION            1
               116 UNARY_INVERT
               117 BINARY_AND
               118 BINARY_OR
               119 CALL_FUNCTION            1
               122 INPLACE_ADD
               123 STORE_FAST               3 (enc)
               126 JUMP_ABSOLUTE           40
           >>  129 POP_BLOCK
   
    12     >>  130 LOAD_FAST                3 (enc)
               133 RETURN_VALUE
            consts
               None
               ''
            names ('map', 'ord', 'range', 'len', 'chr')
            varnames ('s', 'key', 'a', 'enc', 'i')
            freevars ()
            cellvars ()
            filename './py&flower.py'
            name 'encode'
            firstlineno 5
            lnotab 00010f0106011901120104013e01
         code
            argcount 1
            nlocals 4
            stacksize 8
            flags 0043
            code
               7400007401007c00008302007d01007c0100640100640200640300850300
               197d0200784e007402007403007c0100830100830100445d3a007d03007c
               01007c0300630200197c02007c03007403007c020083010016194e033c7c
               01007c0300197c030017640400407c01007c03003c713500577848007402
               00740300740400830100830100445d34007d03007c03007403007c010083
               01006b050072a200740500537c01007c0300197404007c0300196b030072
               860074050053718600577c0200640100197c020064050019187406006401
               00196b030072fa007c0200640100197c0200640500191774060064050019
               6b030072fa007405005374070053
    16           0 LOAD_GLOBAL              0 (map)
                 3 LOAD_GLOBAL              1 (ord)
                 6 LOAD_FAST                0 (s)
                 9 CALL_FUNCTION            2
                12 STORE_FAST               1 (a)
   
    17          15 LOAD_FAST                1 (a)
                18 LOAD_CONST               1 (0)
                21 LOAD_CONST               2 (31)
                24 LOAD_CONST               3 (16)
                27 BUILD_SLICE              3
                30 BINARY_SUBSCR
                31 STORE_FAST               2 (b)
   
    18          34 SETUP_LOOP              78 (to 115)
                37 LOAD_GLOBAL              2 (range)
                40 LOAD_GLOBAL              3 (len)
                43 LOAD_FAST                1 (a)
                46 CALL_FUNCTION            1
                49 CALL_FUNCTION            1
                52 GET_ITER
           >>   53 FOR_ITER                58 (to 114)
                56 STORE_FAST               3 (i)
   
    19          59 LOAD_FAST                1 (a)
                62 LOAD_FAST                3 (i)
                65 DUP_TOPX                 2
                68 BINARY_SUBSCR
                69 LOAD_FAST                2 (b)
                72 LOAD_FAST                3 (i)
                75 LOAD_GLOBAL              3 (len)
                78 LOAD_FAST                2 (b)
                81 CALL_FUNCTION            1
                84 BINARY_MODULO
                85 BINARY_SUBSCR
                86 INPLACE_XOR
                87 ROT_THREE
                88 STORE_SUBSCR
   
    20          89 LOAD_FAST                1 (a)
                92 LOAD_FAST                3 (i)
                95 BINARY_SUBSCR
                96 LOAD_FAST                3 (i)
                99 BINARY_ADD
               100 LOAD_CONST               4 (255)
               103 BINARY_AND
               104 LOAD_FAST                1 (a)
               107 LOAD_FAST                3 (i)
               110 STORE_SUBSCR
               111 JUMP_ABSOLUTE           53
           >>  114 POP_BLOCK
   
    21     >>  115 SETUP_LOOP              72 (to 190)
               118 LOAD_GLOBAL              2 (range)
               121 LOAD_GLOBAL              3 (len)
               124 LOAD_GLOBAL              4 (arr1)
               127 CALL_FUNCTION            1
               130 CALL_FUNCTION            1
               133 GET_ITER
           >>  134 FOR_ITER                52 (to 189)
               137 STORE_FAST               3 (i)
   
    22         140 LOAD_FAST                3 (i)
               143 LOAD_GLOBAL              3 (len)
               146 LOAD_FAST                1 (a)
               149 CALL_FUNCTION            1
               152 COMPARE_OP               5 (>=)
               155 POP_JUMP_IF_FALSE      162
   
    23         158 LOAD_GLOBAL              5 (False)
               161 RETURN_VALUE
   
    24     >>  162 LOAD_FAST                1 (a)
               165 LOAD_FAST                3 (i)
               168 BINARY_SUBSCR
               169 LOAD_GLOBAL              4 (arr1)
               172 LOAD_FAST                3 (i)
               175 BINARY_SUBSCR
               176 COMPARE_OP               3 (!=)
               179 POP_JUMP_IF_FALSE      134
   
    25         182 LOAD_GLOBAL              5 (False)
               185 RETURN_VALUE
               186 JUMP_ABSOLUTE          134
           >>  189 POP_BLOCK
   
    26     >>  190 LOAD_FAST                2 (b)
               193 LOAD_CONST               1 (0)
               196 BINARY_SUBSCR
               197 LOAD_FAST                2 (b)
               200 LOAD_CONST               5 (1)
               203 BINARY_SUBSCR
               204 BINARY_SUBTRACT
               205 LOAD_GLOBAL              6 (arr2)
               208 LOAD_CONST               1 (0)
               211 BINARY_SUBSCR
               212 COMPARE_OP               3 (!=)
               215 POP_JUMP_IF_FALSE      250
               218 LOAD_FAST                2 (b)
               221 LOAD_CONST               1 (0)
               224 BINARY_SUBSCR
               225 LOAD_FAST                2 (b)
               228 LOAD_CONST               5 (1)
               231 BINARY_SUBSCR
               232 BINARY_ADD
               233 LOAD_GLOBAL              6 (arr2)
               236 LOAD_CONST               5 (1)
               239 BINARY_SUBSCR
               240 COMPARE_OP               3 (!=)
               243 POP_JUMP_IF_FALSE      250
   
    27         246 LOAD_GLOBAL              5 (False)
               249 RETURN_VALUE
   
    28     >>  250 LOAD_GLOBAL              7 (True)
               253 RETURN_VALUE
            consts
               None
               0
               31
               16
               255
               1
            names ('map', 'ord', 'range', 'len', 'arr1', 'False', 'arr2', 'True')
            varnames ('s', 'a', 'b', 'i')
            freevars ()
            cellvars ()
            filename './py&flower.py'
            name 'check'
            firstlineno 15
            lnotab 00010f01130119011e011a011901120104011401080138010401
         code
            argcount 1
            nlocals 5
            stacksize 4
            flags 0043
            code
               6401007d01006402007d02007c0200640300197c01001764030014640400
               177c02007c0100640500191764060014177d03007400007c00007c030083
               02007d04007401007c04008301007401007c00008301006b0300725d0064
               0000537402007c04008301007403006b0200727300640000536407004748
               64000053
    32           0 LOAD_CONST               1 ('%$#@!')
                 3 STORE_FAST               1 (key1)
   
    33           6 LOAD_CONST               2 ('f1owe')
                 9 STORE_FAST               2 (key2)
   
    34          12 LOAD_FAST                2 (key2)
                15 LOAD_CONST               3 (2)
                18 BINARY_SUBSCR
                19 LOAD_FAST                1 (key1)
                22 BINARY_ADD
                23 LOAD_CONST               3 (2)
                26 BINARY_MULTIPLY
                27 LOAD_CONST               4 ('r')
                30 BINARY_ADD
                31 LOAD_FAST                2 (key2)
                34 LOAD_FAST                1 (key1)
                37 LOAD_CONST               5 (4)
                40 BINARY_SUBSCR
                41 BINARY_ADD
                42 LOAD_CONST               6 (3)
                45 BINARY_MULTIPLY
                46 BINARY_ADD
                47 STORE_FAST               3 (key)
   
    35          50 LOAD_GLOBAL              0 (encode)
                53 LOAD_FAST                0 (s)
                56 LOAD_FAST                3 (key)
                59 CALL_FUNCTION            2
                62 STORE_FAST               4 (temp)
   
    36          65 LOAD_GLOBAL              1 (len)
                68 LOAD_FAST                4 (temp)
                71 CALL_FUNCTION            1
                74 LOAD_GLOBAL              1 (len)
                77 LOAD_FAST                0 (s)
                80 CALL_FUNCTION            1
                83 COMPARE_OP               3 (!=)
                86 POP_JUMP_IF_FALSE       93
   
    37          89 LOAD_CONST               0 (None)
                92 RETURN_VALUE
   
    38     >>   93 LOAD_GLOBAL              2 (check)
                96 LOAD_FAST                4 (temp)
                99 CALL_FUNCTION            1
               102 LOAD_GLOBAL              3 (False)
               105 COMPARE_OP               2 (==)
               108 POP_JUMP_IF_FALSE      115
   
    39         111 LOAD_CONST               0 (None)
               114 RETURN_VALUE
   
    40     >>  115 LOAD_CONST               7 ('Give you fffflower~*')
               118 PRINT_ITEM
               119 PRINT_NEWLINE
               120 LOAD_CONST               0 (None)
               123 RETURN_VALUE
            consts
               None
               '%$#@!'
               'f1owe'
               2
               'r'
               4
               3
               'Give you fffflower~*'
            names ('encode', 'len', 'check', 'False')
            varnames ('s', 'key1', 'key2', 'key', 'temp')
            freevars ()
            cellvars ()
            filename './py&flower.py'
            name 'main'
            firstlineno 31
            lnotab 00010601060126010f011801040112010401
         None
      names ('arr1', 'arr2', 'encode', 'check', 'main', 'raw_input', 's')
      varnames ()
      freevars ()
      cellvars ()
      filename './py&flower.py'
      name '<module>'
      firstlineno 1
      lnotab 63010c03090a0910090b0901
   ```

4. 逆向脚本 solve.py
