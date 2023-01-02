AS=mips-mti-elf-as
DOS2UNIX=dos2unix
LD=mips-mti-elf-ld
OBJCOPY=mips-mti-elf-objcopy

%.hex: %.elf
	${OBJCOPY} -O ihex $< $@
	${DOS2UNIX} $@

%.elf: %.o
	${LD} -e main -Map=$*.map -N -o $@ $<

%.o: %.s
	${AS} -a=$*.lst -o $@ $<

all: \
helloworld.hex \
read.hex \
tetris.hex \
time.hex \
tt.be.hex \
tt.dir.hex \
tt.fpu.bare.hex \
tt.le.hex
# the following use .kdata or .ktext which we cannot handle yet:
# exceptions.hex
# timer.hex
# tt.alu.bare.hex
# tt.bare.hex
# tt.core.hex
# tt.io.hex

clean:
	rm -f *.elf *.hex *.lst *.map *.o
