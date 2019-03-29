import os
res = os.popen('arp -a').readlines()
for I in res:
 if "00:00:5e:00:xx:xx" in I:
   print(I[:20])
