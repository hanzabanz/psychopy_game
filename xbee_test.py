import xbee
import time
import serial

def SendStr(xbee, msg, addr=0xFFFF, options=0x01, frameid=0x00):
    return Send(xbee, msg.encode('utf-8'), addr, options, frameid)

def Send(xbee, msg, addr=0xFFFF, options=0x01, frameid=0x00):
    if not msg:
        return 0

    hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
    len(msg) + 5,           # LSB (length)
    frameid,
    (addr & 0xFF00) >> 8,   # Destination address high byte
    addr & 0xFF,            # Destination address low byte
    options
    )
    frame = bytearray.fromhex(hexs)
    #  Append message content
    frame.extend(msg)

    # Calculate checksum byte
    frame.append(0xFF - (sum(frame[3:]) & 0xFF))
    # Escape any bytes containing reserved characters
    # frame = Escape(frame)

    print("Tx: " + format(frame))
    return xbee.serial.write(frame)


# x = xbee.XBee("COM4")
# print x
# x.serial.write("1")
# sent = SendStr(x, "Hello World")
# time.sleep(0.25)
# # msg = x.Receive()
# # if msg:
# #     content = msg[7:-1].decode('ascii')
# #     print ("msg: " + content)
#
# x.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
# time.sleep(0.25)
# # msg = x.Receive()
# # if msg:
# #     content = msg[7:-1]
# #     print ("msg: " + content)


ser = serial.Serial("COM4", 9600)


packet = bytearray.fromhex("7E 74 65 73 74 20 76 6C 75 65 73")
ser.write(packet)
