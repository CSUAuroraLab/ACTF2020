#-*- coding=UTF-8 -*-
cipher='''itctus ehnre_agoi lrtrtspnuoia trigt tp,cna eeeu:a rmolaoin  roh oinsqs r rcepnln eeaoe_ynlsdkutteado u.y gn,nfat}e t iisw tymtt  eic d lh.tarclr ott.phecddvea a e wnarlea ha uerteue srtw_roatysdtmec t  fsc i etowerlip   a k efs iapnwaarovkyotwbdif/ rlecgta ecclre snahyenld  aconirsltkdlrsi,ni f ae sguneotelis.dsns acp sgf e rtdnic n a_ei,plhrct e c(ie acuagfco-f ry ioycn uctstlirs otfefsoshonlos rtyto pi tuf_niygiar.eme if s eancon{cgnsrsv  sp  t)c sxngo dwrigta ect ea y oaeet nt eyn,ema thotn ,imrrrsadhilpe mmrbfefid  spevc  uenctep iee r t  c e eiemc  oorran ececij aatu sxatstmgiodgano aoe p isaepcioherntm,l napno '''

possiblelen=[5,25,125]
for k in possiblelen:
    plaintext=""
    line=625//k
    for i in range(k):
        for j in range(line):
            plaintext+=cipher[j*k+i]
    print(plaintext)
