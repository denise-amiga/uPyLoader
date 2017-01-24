from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QDir
import json

from src.singleton import Singleton


class Settings(metaclass=Singleton):
    def __init__(self):
        self.version = 100
        self.root_dir = QDir().currentPath()
        self.send_sleep = 0.1
        self.read_sleep = 0.1
        self.use_transfer_scripts = True
        self.wifi_presets = []
        self.python_flash_executable = None
        self.last_firmware_directory = None
        self.debug_mode = False
        self._geometries = {}

        if not self.load():
            self.load_old()

    def load(self):
        try:
            with open("config.json") as file:
                for key, val in json.load(file).items():
                    self.__dict__[key] = val
                pass
        except FileNotFoundError:
            return False

        return True

    def load_old(self):
        try:
            with open("config.txt") as file:
                for line in file:
                    if line.startswith("root_dir"):
                        self.root_dir = line.strip().split("=", 1)[1]
                    elif line.startswith("send_sleep"):
                        self.send_sleep = float(line.strip().split("=", 1)[1])
                    elif line.startswith("read_sleep"):
                        self.read_sleep = float(line.strip().split("=", 1)[1])
                    elif line.startswith("use_transfer_scripts"):
                        self.use_transfer_scripts = bool(int(line.strip().split("=", 1)[1]))
                    elif line.startswith("wifi_preset"):
                        value = line.strip().split("=", 1)[1]
                        name, ip, port = value.split(",")
                        self.wifi_presets.append((name, ip, int(port)))
                    elif line.startswith("python_flash_executable"):
                        self.python_flash_executable = line.strip().split("=", 1)[1]
                    elif line.startswith("last_firmware_directory"):
                        self.last_firmware_directory = line.strip().split("=", 1)[1]
        except FileNotFoundError:
            return False

        return True

    def save(self):
        try:
            with open("config.json", "w") as file:
                json.dump(self.__dict__, file)
        except IOError:
            pass

    def update_geometry(self, name, geometry):
        self._geometries[name] = list(geometry.data())

    def retrieve_geometry(self, name):
        if name not in self._geometries:
            return None

        return QByteArray(bytes(self._geometries[name]))