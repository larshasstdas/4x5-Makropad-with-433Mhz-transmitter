# 4x5-Makropad-with-433Mhz-transmitter

This project is about a Makropad that has 20 keys in a 4x5 matrix with a 433Mhz transmitter that is used to power my PC. Every key has an indiviually LED that will be changeable with an app on the PC.

---

##Motivation

In a previous project i made a wireless power switch for my PC but as it is only a singular button it feels quite chunky. And i also always had the interest in controlling my LED strips in my room and my PC lighting i got the idea of making a makropad that combines all those features. It should also have usual makropad funktion like adjusting the sound volume and shortcuts. 

---

##PCB

I am using the RP2040 as a microcontroller it has everything i need and can be soldered onto the pcb with castelladed pads. The same goes for the 433MHz transmitter module the STX882. I also have the option to add a display but I am leaving that open as of now. Furthermore there are Hotswap pockets so i can easily spwap broken switches. And for the LED I am using the SK6812MINI-E, a reverse mount LED.

All the PCB files are in the KiCad Folder.

---

##Files

```
KiCad/
├──Makropad/
   ├──Makropad.kicad_pro
   ├──Makropad.kicad_pcb
   ├──Makropad.kicad_sch
   ├──Gerber (and .zip)
   └── Footprint Libarys (.pretty)
└──Symbol Libarys (.sym)
```
