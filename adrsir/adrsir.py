#!/usr/bin/env python3

"""
ADRSIR Controller
=================

Usage
-----
```
adrsir = AdrsirCtrl()

# Read the code from flash
# n = <memory id>
print(adrsir.read(n))

# Write the code to the flash
# n = <memory id>
# code = <code string>
# e.g.
# 5B0018002E001800180018002E
# 001800170018002E0019001700
# 1800170018002E001800180018
# 00170018001700180017004F03
adrsir.write(n, code)

# Transmit the code
# code = <code string>
adrsir.transmit(code)
```

"""

import argparse

import smbus


class AdrsirCtrl:
    # I2C Bus
    BUS = smbus.SMBus(1)
    SLAVE_ADDRESS = 0x52

    """
    Commands
    Read Commands
    * READ_SET_MEM_ID = 0x15
    * READ_GET_DATA_NUM = 0x25
    * READ_DATA = 0x35
    Write Commands
    * WRITE_SET_MEM_ID = 0x19
    * WRITE_SET_DATA_NUM = 0x29
    * WRITE_DATA = 0x39
    * WRITE_FLASH = 0x49
    Transmit Commands
    * TRANSMIT_START = 0x59
    """

    def read(self, mem_id=0):
        # Read the data written in the flash
        mem_id = [mem_id]
        # Set MEM_ID
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x15, mem_id)
        # Get DATA_NUM
        data_numHL = self.BUS.read_i2c_block_data(self.SLAVE_ADDRESS, 0x25, 3)
        data_num = data_numHL[1] * 256 + data_numHL[2]
        # Read DATA
        data = []
        self.BUS.read_i2c_block_data(self.SLAVE_ADDRESS, 0x35, 1)
        for i in range(data_num):
            data.append(self.BUS.read_i2c_block_data(self.SLAVE_ADDRESS, 0x35, 4))
        data = sum(data, [])
        data_str = "".join([f"{x:02X}" for x in data])
        return data_str

    def write(self, mem_id, data_str):
        # Write the data to the flash
        mem_id = [mem_id]
        data = []
        for i in range(len(data_str) // 2):
            data.append(int(data_str[2 * i : 2 * i + 2], 16))
        data_num = len(data) // 4
        # Set MEM_ID
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x19, mem_id)
        # Set DATA_NUM
        data_numHL = [data_num // 256, data_num % 256]
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x29, data_numHL)
        # Write DATA
        for i in range(data_num):
            self.BUS.write_i2c_block_data(
                self.SLAVE_ADDRESS, 0x39, data[4 * i : 4 * i + 4]
            )
        # Flash write
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x49, mem_id)

    def transmit(self, data_str):
        # Transmit the data
        data = []
        for i in range(len(data_str) // 2):
            data.append(int(data_str[2 * i : 2 * i + 2], 16))
        data_num = len(data) // 4
        # Set DATA_NUM
        data_numHL = [data_num // 256, data_num % 256]
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x29, data_numHL)
        # Write DATA
        for i in range(data_num):
            self.BUS.write_i2c_block_data(
                self.SLAVE_ADDRESS, 0x39, data[4 * i : 4 * i + 4]
            )
        self.BUS.write_i2c_block_data(self.SLAVE_ADDRESS, 0x59, [0x00])


if __name__ == "__main__":
    adrsir = AdrsirCtrl()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--read", type=int, help="read the code written in the flash"
    )
    parser.add_argument(
        "-w", "--write", nargs=2, type=str, help="write the code to the flash"
    )
    parser.add_argument("-t", "--transmit", type=str, help="transmit the code")
    args = parser.parse_args()
    if args.read:
        if args.read >= 0 and args.read <= 9:
            print(adrsir.read(args.read))
        else:
            print("mem_id must be 0...9")
    if args.write:
        mem_id = int(args.write[0])
        data_str = args.write[1]
        if mem_id >= 0 and mem_id <= 9:
            adrsir.write(mem_id, data_str)
        else:
            print("mem_id must be 0...9")
    if args.transmit:
        adrsir.transmit(args.transmit)
