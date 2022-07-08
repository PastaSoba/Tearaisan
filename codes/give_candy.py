import smbus
import time

i2c = smbus.SMBus(1)
adr = 0x64

t = 5.3 # 回転時間

i2c.write_byte_data(adr, 0, 0x79) # 上位6bitsが電圧，下位2bitsが操作に対応
time.sleep(t)
i2c.write_byte_data(adr, 0, 0x78)

