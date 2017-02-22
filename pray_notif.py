import re
import time
import argparse
import datetime

from luma.led_matrix import legacy
from luma.led_matrix.device import max7219
from luma.core.serial import spi, noop
from luma.core.render import canvas
from Library.praytimes import PrayTimes
from datetime import date
from datetime import datetime

cascade = 10
orientation = "horizontal"

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=cascade or 1, block_orientation=orientation)
print("Created device")

def demo(cascade,orientation):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=cascade or 1, block_orientation=orientation)
    print("Created device")

    prayTimes = PrayTimes()
    times = prayTimes.getTimes(date.today(),(-6.917,107.619), +7)
    
##    for i in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']:
    for i in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
        msg = times[i.lower()]
        print(msg)
        legacy.show_message(device,msg, fill="white", font=legacy.proportional(legacy.CP437_FONT))
        time.sleep(1)

def checkTime():
    minute = time.strftime("%M",time.localtime())
    msg = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
    waktu = time.strftime("%H:%M",time.localtime())
    prayTimes = PrayTimes()
    times = prayTimes.getTimes(date.today(),(-6.917,107.619), +7)
    
    if minute == "00":
        pesan = "Waktu menunjukkan pukul: "+waktu
##        print("Waktu menunjukkan pukul: "+waktu)
        legacy.show_message(device,pesan, fill="white", font=legacy.proportional(legacy.CP437_FONT))

    
    for i in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
        waktuSolat = times[i.lower()]
        wsTime = datetime.strptime(waktuSolat,"%H:%M");
        nowTime = datetime.strptime(waktu,"%H:%M");
        
        if(wsTime.time() == nowTime.time()):
            pesan2 = "Waktunya Solat " + i
            print("Waktunya Solat " + i)
            legacy.show_message(device,pesan2, fill="white", font=legacy.proportional(legacy.CP437_FONT))
    

if __name__ == "__main__":
    try:
##        demo(2,"horizontal")
        while True:
            checkTime()
            time.sleep(50)
    except KeyboardInterrupt:
        pass
