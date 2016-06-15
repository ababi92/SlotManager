TARGET=avr-zigbit
CONTIKI = ../..

#all: example-abc example-mesh example-collect example-trickle example-polite \
     example-rudolph1 example-rudolph2 example-rucb \
     example-runicast example-unicast example-neighbors

all: split crono

splitflash.hex: split.avr-zigbit
	avr-objcopy -j .text -j .data -O ihex split.avr-zigbit splitflash.hex

spliteeprom.hex: split.avr-zigbit
	avr-objcopy -j .eeprom -O ihex split.avr-zigbit spliteeprom.hex

split: splitflash.hex
	sudo avrdude -p m1281 -c dragon_jtag -P usb -U flash:w:splitflash.hex


cronoflash.hex: crono.avr-zigbit
	avr-objcopy -j .text -j .data -O ihex crono.avr-zigbit cronoflash.hex

cronoeeprom.hex: crono.avr-zigbit
	avr-objcopy -j .eeprom -O ihex crono.avr-zigbit cronoeeprom.hex

crono: cronoflash.hex
	sudo avrdude -p m1281 -c dragon_jtag -P usb -U flash:w:cronoflash.hex


CONTIKI_WITH_RIME = 1
include $(CONTIKI)/Makefile.include


clean:
	rm *~ *.avr-zigbit *.hex *.map
	rm -r avr-zigbit
