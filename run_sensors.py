import smbus
import time

MEASURE = [0x33, 0x00]

class I2C:
    def __init__(self, bus):
        self.bus = smbus.SMBus(bus)
        self.addr_1 = 0x38
        self.addr_2 = 0x4B
        self.LCD_ADDR = 0x27
        self.BLEN = 1

    def getData(self):
        try:
            self.bus.write_i2c_block_data(self.addr_1, 0xAC, MEASURE)
            time.sleep(0.5)
            temp_humid_data = self.bus.read_i2c_block_data(self.addr_1, 0x00)
            temp = ((temp_humid_data[3] & 0x0F) << 16) | (temp_humid_data[4] << 8) | temp_humid_data[5]
            ctemp = ((temp * 200) / 1048576) - 50
            hum = ((temp_humid_data[1] << 16) | (temp_humid_data[2] << 8) | temp_humid_data[3]) >> 4
            chum = int(hum * 100 / 1048576)
            return ctemp, chum
        except Exception as e:
            print("Error reading temperature and humidity:", e)
            return None, None

    def read_channel(self, channel):
        try:
            config_byte = 0x84 | ((channel & 0x07) << 4)
            self.bus.write_byte(self.addr_2, config_byte)
            time.sleep(0.5)
            data = self.bus.read_word_data(self.addr_2, 0)
            voltage = ((data & 0xFF) << 8 | (data >> 8)) * 5.0 / 0xFFF
            return voltage
        except Exception as e:
            print("Error reading channel:", e)
            return None

    def write_word(self, addr, data):
        temp = data
        if self.BLEN == 1:
            temp |= 0x08
        else:
            temp &= 0xF7
        self.bus.write_byte(addr, temp)

    def send_command(self, comm):
        buf = comm & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(self.LCD_ADDR, buf)
        buf = (comm & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(self.LCD_ADDR, buf)

    def send_data(self, data):
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(self.LCD_ADDR, buf)
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.write_word(self.LCD_ADDR, buf)

    def clear(self):
        self.send_command(0x01)

    def lcd_write(self, x, y, string):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)
        for char in string:
            self.send_data(ord(char))

# Initialize AHT10 sensor with bus number 1
i2c = I2C(bus=1)

count = 0
try:
    while True:
        temperature, humidity = i2c.getData()
        temperature = round(temperature,2)
        voltage = i2c.read_channel(0)
        brightness = voltage * 255 / 5
        brightness = round(brightness,2)
        i2c.clear()
        i2c.lcd_write(0, 0, 'T: ' + str(temperature) + 'C H: ' + str(humidity) + '%')  #"Temp: {:.2f} C  Hum: {:.2f} %".format(temperature, humidity)
        i2c.lcd_write(0, 1, 'Light: ' + str(brightness)) #"Brightness: {:.2f}".format(brightness)
        print("Temperature: {} Celsius".format(temperature))
        print("Humidity: {}%".format(humidity))
        print("Brightness value: {:.2f}".format(brightness))
        time.sleep(1)
        count += 1
except KeyboardInterrupt:
    print("Program stopped by the user.")
finally:
    # Cleanup
    i2c.clear()