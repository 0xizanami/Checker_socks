import socket
import struct
from multiprocessing.dummy import Pool
 
TIMEOUT = 3
SOURCE = 'proxy.txt'
 
def SaveFile(version, proxy):
    print(f'SOCKS{version}: {proxy}')
    file = open(f'SOCKS{version}.txt', 'a+', encoding='utf-8')
    file.write(proxy + '\n')
    file.flush()
    
def connect(proxyport, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect(proxyport)
        s.sendall(data)
        return s.recv(2)
    except Exception as e:
#        print(e)
        return 'None'
 
def main(host_port):
    proxy = host_port.split(':')
    
    port = int(proxy[1])
    pconnect = (proxy[0], port)
    
    data_socks5 = struct.pack('BBB', 0x05, 0x01, 0x00)
    response = connect(pconnect, data_socks5)
    if response == b'\x05\x00' :
        SaveFile(5, host_port)
        return
        
    if response == 'None':
        print('BAD: ' + host_port)
        return
        
    data_socks4 = struct.pack('BBH', 0x04, 0x01, port)
    response = connect(pconnect, data_socks4)
    if response == b'':
        SaveFile(4, host_port)
        return
    
source = open(SOURCE, 'r', encoding='utf-8').read().splitlines()
 
pp = Pool(32)
pp.map(main, source)
