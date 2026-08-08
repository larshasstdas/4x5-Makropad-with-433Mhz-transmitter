# 4x5-Makropad-with-433Mhz-transmitter

This project is about a Makropad that has 20 keys in a 4x5 matrix with a 433Mhz transmitter that is used to power my PC. Every key has an indiviually LED that will be changeable with an app on the PC.

---

## Motivation

In a previous project i made a wireless power switch for my PC but as it is only a singular button it feels quite chunky. And i also always had the interest in controlling my LED strips in my room and my PC lighting i got the idea of making a makropad that combines all those features. It should also have usual makropad funktion like adjusting the sound volume and shortcuts. 

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
| PCB                       | Fabricated 4×5 board                              | 1   | 33.67€     | – |
| 3D-printed case           | Top + bottom, filament                            | 1   | ~1.00€     | – |
| **Total**                 |                                                   |     | **78.84€** | |

---

## Case

The CAD files for the Case are in the CAD folder. There are the source files from creo parametric (my cad tool), the step-files and the stl-files each in one folder. They contain a file for the top and the bottom part and the Creo folder also has the assembly file for the makropad which you can see below. The only files needed for 3D.printing are the case_bottom and cas_top files. The rest are only used for the assembly.

<img width="1403" height="899" alt="image" src="https://github.com/user-attachments/assets/9a2d44e4-6dc4-4761-ba0e-d2ba610bed14" />


---

## Files

```
CAD/
├──Creo/
   ├──Case_top.prt
   ├──Case_bottom.prt
   ├──Case.asm
   ├──pcb.asm
   └──stx882.prt
├──stl/
   ├──Case_top.stl
   └──Case_bottom.stl
└──stp/
   ├──Case_top.stp
   ├──Case_bottom.stp
   ├──PCB.stp
   ├──stx882.stp
   └──KS-3X Full Black Switch KS-3A10B060NN-X.stp
   
KiCad/
├──Makropad/
   ├──Makropad.kicad_pro
   ├──Makropad.kicad_pcb
   ├──Makropad.kicad_sch
   └── Footprint Libarys (.pretty)
├──Symbol Libarys (.sym)
├──Gerber (and .zip)
└──Pick&Place.csv
BOM.csv
```
