import serial
import libscrc

def read(ser):
    byte = []
    while True:
        byte.append(ser.read(1))
        if byte[-1] == b'':
            byte.pop()
            break
    return byte

def byte_to_hex(byte):
    text = ''
    for el in byte:
        sb = str(hex(int.from_bytes(el, "big"))).split('x')[1]
        if len(sb) == 1:
            sb = '0' + sb
        #if text != '':
        #    sb = ' ' + sb
        text = text + ' ' + sb
    return text[1:]

if __name__ == '__main__':
    req_addr ='02 01 65 63' # сетевой адрес устройства (4байта) в формате BCD, старшим байтом вперёд;
    req_f =  '01' # код функции запроса (1 байт);
    req_l = '0E' # общая длина пакета (1 байт);
    req_data = '01 00 00 00' # входные данные запроса (длина определяется F);
    req_id = '00 00' # идентификатор запроса (любые 2 байта);
    req_hex = bytes.fromhex(req_addr+' '+req_f+' '+req_l+' '+req_data+' '+req_id)
    crc_str = hex(libscrc.modbus(req_hex)).split('x')[1]
    crc = crc_str[2:4]+' '+crc_str[0:2]
    req = req_addr + ' ' + req_f + ' ' + req_l + ' ' + req_data + ' ' + req_id+' '+crc
    print('Запрос:', req)
    req_hex = bytes.fromhex(req)
    try:
        ser = serial.Serial(port='COM3',baudrate=9600,timeout=1.5)
        print('Порт',ser.port,'свободен.')
        ser.write(req_hex)  # Определение сетевого адреса.
        byte = read(ser)
        #print('Ответ(byte):', byte)
        hex_str = byte_to_hex(byte)
        hex_list = hex_str.split(' ')
        print('Ответ:',hex_str,'('+str(len(hex_list))+' байт)')
        print('Ответ от:',[hex_list[el] for el in range(4)])
        if req_f == '01':
            data_list = [hex_list[el] for el in range(6,14)]
            print('Ответ DATA:',data_list)
            data_str = ""
            for el in data_list:
                data_str = data_str +' '+ el
            import struct

            DATA = data_str[1:].upper().replace(' ','')
            print('Ответ DATA:', DATA)
            #print(struct.unpack("<f", "F03F".decode("hex")))
    except serial.serialutil.SerialException:
        print('Что то пошло не так.')



