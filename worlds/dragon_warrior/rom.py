import hashlib
import os
import sys
import logging
import platform
from typing_extensions import override
import zipfile
from worlds.AutoWorld import World
import Utils
import settings
from worlds.Files import APAutoPatchInterface

DRAGON_WARRIOR_HASH = "25cf03eb7ac2dec4ef332425c151f373"

class DWPatch(APAutoPatchInterface):
    hash = DRAGON_WARRIOR_HASH
    game = "Dragon Warrior"
    patch_file_ending = ".apdw"
    result_file_ending = ".nes"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()
    
    @override
    def patch(self, target: str) -> None:
        # Extract the dwr module from the .apworld depending on OS into a temp directory
        current_directory = os.getcwd()
        new_dir = os.path.join(current_directory, "dragon_warrior_randomizer")

        try:
            os.mkdir(new_dir)
            if platform.system() == "Windows":
                file = "dwr.cp312-win_amd64.pyd"
            else:
                file = "dwr.cpython-312-x86_64-linux-gnu.so"
            
            with zipfile.ZipFile(os.path.join(current_directory, "custom_worlds", "dragon_warrior.apworld")) as zf:
                zf.extract("dragon_warrior/" + file, path=new_dir)

            # Clean up format from zip file
            os.replace(os.path.join(new_dir, "dragon_warrior", file), os.path.join(new_dir, file))
            os.rmdir(os.path.join(new_dir, "dragon_warrior"))
            open(os.path.join(new_dir, "__init__.py"), "a")

        except FileExistsError:
            pass

        sys.path.append(new_dir)

        self.read()
        write_rom(8519378015, "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAUAAAAAA", target)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = open(file_name, "rb").read()

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if DRAGON_WARRIOR_HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(PRG1) release.'
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options.dw_options["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

def write_rom(seed: int, flags: str, target: str) -> None:
    import dwr # type: ignore
    dwr.py_dwr_randomize(bytes(get_base_rom_path(), encoding="ascii"), seed, bytes(flags, encoding="ascii"), bytes(target, encoding="ascii"))