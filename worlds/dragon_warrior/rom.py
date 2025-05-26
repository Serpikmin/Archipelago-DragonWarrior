import hashlib
import os
import Utils
from worlds.Files import APDeltaPatch

DRAGON_WARRIOR_HASH = "25cf03eb7ac2dec4ef332425c151f373"


class LocalRom:

    def __init__(self, file, name=None, hash=None):
        self.name = name
        self.hash = hash

        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        pass
        self.buffer[startaddress:startaddress + len(values)] = values
        pass

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    def find_free_space(self, start, size):
        for i in range(start, 0xffff - size + 1):
            found = True
            if self.read_bytes(i, size) != bytearray([0xff] * size):
                found = False
                break

            if found:
                return i
        return -1


class DWDeltaPatch(APDeltaPatch):
    hash = [DRAGON_WARRIOR_HASH]
    game = "Dragon Warrior"
    patch_file_ending = ".apdw"
    result_file_ending = ".nes"
    name: bytearray

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if DRAGON_WARRIOR_HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(PRG1) release.'
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["dw_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name