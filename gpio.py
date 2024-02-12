pins = [140,156,155,138,136,139,137,135,134,39,133,132,38,37,121,36,32,61,33,54,34,55,35,50,56,51,59]
pinMux = {
    140 : "/sys/kernel/debug/omap_mux/mcspi1_cs3",
    156 : "/sys/kernel/debug/omap_mux/uart4_tx",
    155 : "/sys/kernel/debug/omap_mux/uart4_rx",
    138 : "/sys/kernel/debug/omap_mux/mcspi1_cs1",
    136 : "/sys/kernel/debug/omap_mux/mcspi1_simo",
    139 : "/sys/kernel/debug/omap_mux/mcspi1_cs2",
    137 : "/sys/kernel/debug/omap_mux/mcspi1_cs0",
    135 : "/sys/kernel/debug/omap_mux/mcspi1_somi",
    134 : "/sys/kernel/debug/omap_mux/mcspi1_clk",
    39 : "/sys/kernel/debug/omap_mux/gpmc_ad15",
    133 : "/sys/kernel/debug/omap_mux/i2c4_sda",
    132 : "/sys/kernel/debug/omap_mux/i2c4_scl",
    38 : "/sys/kernel/debug/omap_mux/gpmc_ad14",
    37 : "/sys/kernel/debug/omap_mux/gpmc_ad13",
    121 : "/sys/kernel/debug/omap_mux/h_dmtimer11_pwm",
    36 : "/sys/kernel/debug/omap_mux/gpmc_ad12",
    32 : "/sys/kernel/debug/omap_mux/gpmc_ad8",
    61 : "/sys/kernel/debug/omap_mux/gpmc_wait0",
    33 : "/sys/kernel/debug/omap_mux/gpmc_ad9",
    54 : "/sys/kernel/debug/omap_mux/gpmc_nwp",
    34 : "/sys/kernel/debug/omap_mux/gpmc_ad10",
    55 : "/sys/kernel/debug/omap_mux/gpmc_clk",
    35 : "/sys/kernel/debug/omap_mux/gpmc_ad11",
    50 : "/sys/kernel/debug/omap_mux/gpmc_ncs0",
    56 : "/sys/kernel/debug/omap_mux/gpmc_nadv_ale",
    51 : "/sys/kernel/debug/omap_mux/gpmc_ncs1",
    59 : "/sys/kernel/debug/omap_mux/gpmc_nbe0_cle"
}   

exportedPins = []



def unexport(num):
    assert num in pins, "Provided pin does not exist"
    del exportedPins[exportedPins.index(num)]
    with open("/sys/class/gpio/export", "w") as unexport:
        unexport.write(str(num))
        

def setDir(num, dir):
    assert dir == "in" or dir == "out", "Direction must be either \"in\" or \"out\""
    with open("/sys/class/gpio/gpio" + str(num) + "/direction") as direction:
        direction.write(dir)

def getValue(num):
    assert num in pins, "Provided pin does not exist"
    with open("/sys/class/gpio/gpio" + str(num) + "/value") as valueFile:
        return valueFile.readline()

def setValue(num, value):
    `assert num in pins, "Provided pin does not exist"
     assert value == 1 or value == 0, "Value must either be 0 or 1"
        with open("/sys/class/gpio/gpio" + str(num) + "/value") as valueFile:
            valueFile.write(str(value))

def checkInputs(num, dir, pull):
    assert num in pins, "Provided pin does not exist"
    assert dir == "in" or dir == "out", "Direction must be either \"in\" or \"out\""
    assert pull == "down" or pull == "up", "Pull direction must be either \"up\" or \"down\""

def setup(num, dir, pull):
    checkInputs(num,dir,pull)
    exportedPins.append(num)

    #Adding gpio to export
    with open("/sys/class/gpio/export", "w") as export:
        export.write(str(num))

    #Setting the pins' direction
    with open("/sys/class/gpio/gpio" + str(num) + "/direction", "w") as direction:
        direction.write(dir)

    #Muxing the pins from function no. 1 to gpio
    with open(pinMux[num], "w") as mux:
        if pull == "down":
            mux.write("0x10b")
        elif pull == "up":
            mux.write("0x11b")

def cleanup():
    for x in exportedPins:
        unexport(x)

    
