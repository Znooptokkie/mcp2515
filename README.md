# MCP2515 CAN-Bus Communicatie met Raspberry Pi 5 en Raspberry Pi Pico

## 📌 Benodigdheden
- **Raspberry Pi 5** + **MCP2515 CAN-module**
- **Raspberry Pi Pico** + **MCP2515 CAN-module**
- **2 x 120 ohm weerstand**
- **Jumper wires**
- **Micro-USB-kabel voor de Raspberry Pi Pico**

---

## 🛠️ Hardware aansluiten

### **CAN-bus bedrading**
🔹 Zorg dat op beide MCP2515 modules een **120 ohm weerstand** aanwezig is!  

| **MCP2515 (Raspberry Pi 5)** | **MCP2515 (Raspberry Pi Pico)** |
|------------------------------|---------------------------------|
| **CAN_H (female jumper)** | **CAN_H (male jumper)** |
| **CAN_L (female jumper)** | **CAN_L (male jumper)** |

---

## 🔌 SPI-aansluitingen MCP2515 → Raspberry Pi 5

| **MCP2515** | **Raspberry Pi 5 (GPIO)** |
|------------|---------------------------|
| **VCC** | **5V** |
| **GND** | **GND** |
| **CS** | **GPIO 8 (Pin 24, CE0)** |
| **SCK** | **GPIO 11 (Pin 23, SCLK)** |
| **SI (MOSI)** | **GPIO 10 (Pin 19, MOSI)** |
| **SO (MISO)** | **GPIO 9 (Pin 21, MISO)** |
| **INT** | **GPIO 25 (Pin 22, Optioneel)** |

---

## 🔌 SPI-aansluitingen MCP2515 → Raspberry Pi Pico

| **MCP2515** | **Raspberry Pi Pico (GPIO)** |
|------------|-------------------------------|
| **VCC** | **5V (Pin 40)** |
| **GND** | **GND** |
| **CS** | **GP17 (Pin 22)** |
| **SCK** | **GP18 (Pin 24)** |
| **SI (MOSI)** | **GP19 (Pin 25)** |
| **SO (MISO)** | **GP16 (Pin 21)** |
| **INT** | **GP20 (Optioneel)** |

---

## 🖥️ Raspberry Pi 5 configureren

### **SPI inschakelen**
```bash
sudo raspi-config
```

### **Herstart de Raspberry Pi 5**
```bash
sudo reboot
```

## MCP2515 configureren

### **Open het configuratiebestand**
```bash
sudo nano /boot/firmware/config.txt
```

###  **Voeg de volgende regelst toe (of wijzig ze als ze al bestaan)**
```bash
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
```

🔹 **Opmerking:** `oscillator=8000000` is nodig omdat de MCP2515 een 8 MHz kristal gebruikt.


### **Sla op en herstart de Raspberry Pi 5 opnieuw**
```bash
sudo reboot
```

## 🖧 CAN-interface activeren

### **Zet de CAN-interface aan met:**
```bash
sudo ip link set can0 up type can bitrate 500000
```

### **Controleer of can0 actief is**
```bash
ip link show can0
```

## 🖥️ Raspberry Pi Pico instellen

### **Flash MicroPython op de Pico**
1. **Download de MicroPython UF2:** [**MicroPython voor Raspberry Pi Pico**](https://micropython.org/download/RPI_PICO/)  
2. **Houd BOOTSEL ingedrukt**, sluit de Pico via USB aan en **sleep het UF2-bestand** naar de `"RPI-RP2"` USB-schijf.  
3. De **Pico start automatisch opnieuw op**. (Zo niet, verwijder en sluit hem opnieuw aan.)  
   - **Als hij niet meer als USB-schijf verschijnt, is dat CORRECT!** 

### **Sluit Thonny aan op de Pico**
1. **Open Thonny.**
2. Ga naar **Interpreter** > **MicroPython (Raspberry Pi Pico)**.
3. Druk op **Verbinden**.

---

## 🔍 Test de communicatie

### **Zorg eerst dat je candump correct hebt gedownload**
```bash
sudo apt install can-utils
```

### **Start `candump` op de Raspberry Pi 5:**
```bash
candump can0
```

### **Stuur een bericht naar de Pico vanaf de Raspberry Pi 5**
```bash
cansend can0 123#11223344
```

## 🛠️ Troubleshooting

**Probleem: De CAN-Bus zit in een error-modus ("bus-off")**  
**Controleer de MCP2515-status met:**
```bash
dmesg | grep -i mcp
```

### **Oplossing: Reset de MCP2515 met de volgende commando's**
```bash
sudo dmesg -C
sudo rmmod mcp251x
sudo modprobe mcp251x
```