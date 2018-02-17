import sav
import ace4f

t = sav.SAVFile("test.sav")
t2 = sav.SAVFile("test2.sav")

print t[1][0x1523]

print ace4f.gen_checksum(t[1][0x0598:(0x0598+(0x1523-0x0598+1))])

print t2[1][0x1523]

print ace4f.gen_checksum(t2[1][0x0598:(0x0598+(0x1523-0x0598+1))])
