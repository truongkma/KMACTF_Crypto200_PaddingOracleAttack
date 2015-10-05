import socket
import re
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("128.199.183.44", 6996))
s.recv(1024)
iv = '25ec080ab01e28c41129491b5fd12abb'
c = ['a5936cfd61e8d5dc6b6b6d121d2a7124', '2185a46e5fa57e13978116bb3a41fad2',
     '0391b4c23db04cebbcf1bad5acc65901', '4dbe68df1de8b218688a304da14d4e5a',
     'c3513a88426e69cb5b6175f1a149eaf4', '53e32ddb37ac74e319b873eaed1bb314']
full_iv = []
def xored(a, b):
    hexxor = '10' * 16
    return hex(int(a, 16) ^ int(hexxor, 16) ^ int(b, 16))[2:-1].decode('hex')


def send_request(data):
    s.send(data + "\n")
    kq = s.recv(1024)
    err = re.findall(r'\d+', kq)
    s.send("\n")
    return eval(err[0])

print send_request(iv + c[0])
for i in range(6):
    new_iv = ['00'] * 16
    for j in range(16):
        print "Compute element " + str(16 - j) + " of block " + str(i + 1)
        iv1 = ''.join(new_iv)
        data = iv1 + c[i]
        er = send_request(data)
        if er == 403:
            for k in range(256):
                new_iv[15 - j] = format(k, '02x')
                iv1 = ''.join(new_iv)
                data = iv1 + c[i]
                er = send_request(data)
                if er == 403:
                    continue
                else:
                    print data
                    for x in range(j + 1):
                        new_iv[
                            15 - x] = format(int(new_iv[15 - x], 16) ^ (j + 1) ^ (j + 2), '02x')
                    break
        else:
            j += 1
    full_iv.append(data)
print full_iv

a = []
b = []
for i in range(6):
    if i == 0:
        a.append(iv)
    else:
        a.append(full_iv[i - 1][32:64])
    b.append(full_iv[i][0:32])

data = ''
for i in range(6):
    data += xored(a[i], b[i])
print data
