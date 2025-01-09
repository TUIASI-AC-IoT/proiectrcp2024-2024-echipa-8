import psutil
import time
from tkinter import messagebox
from pyasn1.type import univ


class MIB:
    Name = "Agent"
    Temperature = "Celsius"
    getData = True


    def get_temperatura(temperature_unit):
        try:
            if not hasattr(psutil, "sensors_temperatures"):
                return None  # Platforma nu suportă

            temperature_info = psutil.sensors_temperatures()

            if not temperature_info:
                return None

            cpu_sensors = ["coretemp", "k10temp", "cpu_thermal"]
            for sensor in cpu_sensors:
                if sensor in temperature_info:
                    for entry in temperature_info[sensor]:
                        # Temperatura inițială în Celsius
                        temp_celsius = entry.current

                        # Convertim OctetString la string
                        if isinstance(temperature_unit, univ.OctetString):
                            temperature_unit = str(temperature_unit)

                        unit = temperature_unit.strip().lower()
                        if unit == 'kelvin':
                            temp = temp_celsius + 273.15
                        elif unit == 'fahrenheit':
                            temp = (temp_celsius * 9 / 5) + 32
                        else:
                            temp = temp_celsius

                        return round(temp, 2)

            return None

        except Exception as e:
            print(f"Eroare în funcția get_temperatura: {e}")
            return None

    def changeTemperature(self, new_temperature):
        self.Temperature = new_temperature

    def changeName(self, new_name):
        self.Name = new_name

    def getRamPercent(self):
        try:
            ram_percent = psutil.virtual_memory().percent
            return str(ram_percent)
        except Exception as e:
            return f"Eroare la obținerea procentului RAM: {str(e)}"

    def getRamGB(self):
        try:
            ram_gb = psutil.virtual_memory().used / 1e9
            return f"{ram_gb:.2f}"
        except Exception as e:
            return f"Eroare la obținerea memoriei RAM: {str(e)}"

    def getCPUPercent(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=4)
            return str(cpu_percent)
        except Exception as e:
            return f"Eroare la obținerea utilizării CPU: {str(e)}"