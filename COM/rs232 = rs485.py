import serial
from time import sleep
ser = serial.Serial()
ser.port='COM3'
ser.baudrate=9600
ser.open()
ser.timeout = 1.5
print('is_open:',ser.is_open)
ser.write(b'\xF0\x0F\x0F\xF0\x00\x00\x00\x00\x00\xA5\x44') # Определение сетевого адреса.
byte = []
while True:
    byte.append(ser.read(1))
    if byte[-1] == b'':
        byte.pop()
        break
text = ''
if byte[0:4] == [b'\xf0', b'\x0f', b'\x0f', b'\xf0']:
    for el in byte[4:8]:
        sb = str(hex(int.from_bytes(el, "big"))).split('x')[1]
        if len(sb) == 1:
            sb = '0'+sb
        text = text +' '+ sb
print('adres:',text)
#print('line:',len(read),type(read),read)

#readall    line: 10 <class 'bytes'> b'\xf0\x0f\x0f\xf0\x02\x01ec\xcb\xa4'
#readline   line: 10 <class 'bytes'> b'\xf0\x0f\x0f\xf0\x02\x01ec\xcb\xa4'

