# 4x5-Makropad-with-433Mhz-transmitter

<img width="1788" height="730" alt="WhatsApp Image 2026-08-31 at 16 35 43" src="https://github.com/user-attachments/assets/ed40fcc4-7af6-4d64-9f83-f5bf9086264a" />

This project is about a Makropad that has 20 keys in a 4x5 matrix with a 433Mhz transmitter that is used to power my PC. Every key has an indiviually LED that will be changeable with an app on the PC.

---

## Motivation

In a previous project i made a [wireless power switch for my PC](https://github.com/larshasstdas/Remote-PC-Power-Switch) but as it is only a singular button it feels quite chunky. And i also always had the interest in controlling my LED strips in my room and my PC lighting i got the idea of making a makropad that combines all those features. It should also have usual makropad funktion like adjusting the sound volume and shortcuts. 

---

## How it works

The RP2040 registers which key is pressed. It send that information to a daemon on my pc which has the information of what that key actually does. The programm can also send information to the makropad to what each LED should be. If the button is pressed that is used for turning the PC on the daemon can't answer because the PC is turned of. If the RP2040 does not get a signal back it sends the signal to the stx882 module resulting in turning the PC on. It can use a different function afterwards because the daemon can answer if that button is pressed.

---

## PCB

I am using the RP2040 as a microcontroller it has everything i need and can be soldered onto the pcb with castelladed pads. The same goes for the 433MHz transmitter module the STX882. I also have the option to add a display but I am leaving that open as of now. Furthermore there are Hotswap pockets so i can easily spwap broken switches. And for the LED I am using the SK6812MINI-E, a reverse mount LED. The switches are using a matrix so they need less pins and the LEDs are in an addressable LED chain.

All the PCB files are in the KiCad Folder.

<img width="1261" height="739" alt="image" src="https://github.com/user-attachments/assets/53fd4799-6ba3-4de2-a738-b3363492ecb7" />


---

## Bill of Materials

Bought the parts so they would be as cheap as possible. Did not buy the display pins as i do not plan on using it for now. It is just an option for the future.

| Part                      | Description                                       | Qty | Unit Price | Link |
| ------------------------- | ------------------------------------------------- | --- | ---------- | ---- |
| Waveshare RP2040-Zero     | MCU module, USB-C, castellated                    | 1   | 4.00€      | [Eckstein](https://eckstein-shop.de/WaveShare-RP2040-Zero-MCU-Board-Mini-Version) |
| STX882                    | 433 MHz ASK/OOK transmitter (+ spring antenna)    | 1   | 6.99€      | [Amazon](https://www.amazon.de/dp/B0D3TGHD7H/) |
| SK6812MINI-E              | Addressable RGB LED, reverse mount                | 20  | 6.59€      | [Amazon](https://www.amazon.de/gp/product/B0DQ8HXSQS/) |
| 74AHCT1G125               | Level shifter 3.3V→5V for LED data line (SOT-353) | 1   | 0.20€      | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/tristate-buffer_enable_2_5_5_v_sot-353-5-219156) |
| Gateron Pro Milky Yellow  | Linear 5-pin hotswap switch                       | 20  | 6.80€      | [inputgear](https://inputgear.de/products/gateron-pro-milky-yellow-switch?variant=56226523775320) |
| Kailh MX Hotswap Socket   | MX hotswap socket (THT)                           | 20  | 7.83€      | [Amazon](https://www.amazon.de/gp/product/B07K8CCMQZ/) |
| Keycaps 1u                | Opaque keycaps (light shows around base)          | 20  | 10.71€     | [Amazon](https://www.amazon.de/gp/product/B0F1YQGJ35/) |
| 1N4148W                   | Matrix diode, 100V 150mA (SOD-123)                | 20  | 0.40€      | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/kleinsignal-schalt-diode_100_v_150_ma_sod-123-219382) |
| 100nF capacitor           | Decoupling, X7R 50V (0603)                        | 21  | 0.63€      | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/mlcc_0603_100nf_50v_x7r_-5_-429035) |
| 330 Ω resistor            | LED data-line series resistor (0603)              | 1   | 0.02€      | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/smd-widerstand_0603_330_ohm_100_mw_1_-89424) |
| I2C display header        | 4-pin Dupont, optional display (2.54mm)           | 1   | -          | – |
| PCB                       | pcb ordered on jlcpcb                             | 1   | 33.67€     | – |
| 3D-printed case           | Top + bottom, filament                            | 1   | ~1.00€     | – |
| **Total**                 |                                                   |     | **78.84€** | |

---

## Case

The CAD files for the case are in the CAD folder. There are the source files from creo parametric (my cad tool), the step-files and the stl-files each in one folder. They contain a file for the top and the bottom part and the Creo folder also has the assembly file for the makropad which you can see below. The only files needed for 3D.printing are the case_bottom and cas_top files. The rest are only used for the assembly.

<img width="1403" height="899" alt="image" src="https://github.com/user-attachments/assets/9a2d44e4-6dc4-4761-ba0e-d2ba610bed14" />


---

## How it is build

The pcb is soldered on a hot plate and some parts by soldering iron. The switches get placed into the hotswaps and once that is done it is placed in the bottom half of the case. Afterwards the top part gets fitted onto the bottom part and the keycaps get pressed onto the switches.

<img width="1080" height="1920" alt="image" src="https://github.com/user-attachments/assets/4782ff0d-56fa-4c09-8d19-ebfb6055ca68" />
<img width="1530" height="2040" alt="image" src="https://github.com/user-attachments/assets/37045730-6da7-450d-939b-11d2fbc0432d" />



---

## How to flash

I used VS Code with platform.io to flash the RP2040. Just connect with an USB-C cable and press the flash button bottom left.

---

## How to set up the daemon

1. Create and activating the venv. For that first use "cd C:\path\...\Makropad\Daemon", then "python -m venv venv" and last "venv\Scripts\Activate.ps1".
2. Install all the libarys. The versions are in the requirements.txt
3. Select the right COM port in the config.json
4. Press "Win + R" and type "shell:startup" so the startup folder opens.
5. Rightclick and add a new shortcut. Enter the location "C:\path\...\Makropad\Daemon\venv\Scripts\pythonw.exe main.py" for the shortcut. When you press enter you can choose a name.
6. Rightclick the new shortcut and go to properties. In "Start in" enter the daemon folder "C:\path\...\Makropad\Daemon" it must not include "\venv\Scripts".
7. Apply the changes.

---

## Files

```
CAD/               Creo source files (top, bottom, pcb and assembly), stl files (top & bottom), step files
Deamon/            Python files for the daemon, requirements.txt with all the libary versions  
KiCad/             KiCad files, Gerber files (also as .zip), libarys, Pick&Place
RP2040_Code/       Platform.io project with all files needed for flashing the RP2040
BOM.csv
```
