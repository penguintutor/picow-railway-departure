from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime
import ujson

url = "http://192.168.0.2:8080/departures.py?platform="


text_x = 0 # start point for text in x-dir
text_y = 0 # start point for text in y-dir
text_y_space = 12 # space between text in y-dir
oled = None
oled1 = None
# Assume wireless required - any problems (config or connect etc.) then set to False
wireless_enabled = True

def main():
    global oled, oled1, wireless_enabled
    width  = 128 # SSD1306 horizontal resolution
    height = 32   # SSD1306 vertical resolution
    i2c_dev = I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)  # start I2C on I2C0 (GP 16/17) physical 21/22
    i2c_dev1 = I2C(1,scl=Pin(19),sda=Pin(18),freq=200000)  # start I2C on I2C1 (GP 18/19) physical 24/25

    oled = SSD1306_I2C(width, height, i2c_dev) # oled controller
    oled1 = SSD1306_I2C(width, height, i2c_dev1) # oled controller
   
    
    try:
        cfgfile = open('secrets.json', 'r')
        config = ujson.loads(cfgfile.read())
    
        ssid = config['SSID']
        wpass = config['WPASS']
    except:
        display_message ("Error config file", "No secrets.json")
        wireless_enabled = False
    
    
    if (wireless_enabled):
        try:
            # Display message
            display_message ("Connecting...", ssid)
        
            import network
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(ssid, wpass)
        except:
            # If unable to connect to network switch to offline
            display_message ("Unable to connect", ssid)
            wireless_enabled = False
    
    if wireless_enabled:
        # Wait for connection
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            utime.sleep(1)
            
        # Handle connection error
        if wlan.status () != 3:
            display_message ("Network failed", ssid)
            # pause so user sees message
            utime.sleep (10)
            wireless_enabled = False
        else:
            status = wlan.ifconfig()
            display_message("Connected", status[0])
            utime.sleep (5)
    

    while (1):
        display_message (*get_train_list(0), 0)
        display_message (*get_train_list(1), 1)
        # check every 30 seconds
        utime.sleep (30)
        
        
def display_message (line1 = "", line2 = "", line3 = "", display=-1):
    # no display specified - use both
    if (display == -1):
        _disp_msg(line1,line2,line3,0)
        _disp_msg(line1,line2,line3,1)
    elif (display == 1):
        _disp_msg(line1,line2,line3,1)
    else:
        _disp_msg(line1,line2,line3,0)

        
# internal method only update one display
def _disp_msg (line1, line2, line3, display):
    global oled, oled1
    if (display == 1):
        disp = oled1
    else:
        disp = oled
    disp.fill(0)
    disp.text(line1, text_x, text_y)
    disp.text(line2, text_x, text_y + text_y_space)
    disp.text(line3, text_x, text_y + (text_y_space*2))
    disp.show()

# Returns 3 lines of text 
def get_train_list(platform=0):
    # Generic error message if no other messages
    text_list = ["Departure board", "Out of order", "**********"]
    
    if wireless_enabled:
        try:
            import urequests
            this_url = url+str(platform)
            request = urequests.get(this_url)
            #print (request.content)
            train_data = ujson.loads(request.content)
            #print (str(train_data))
            request.close()
            
        except Exception as e:
            print ("Error retrieving from url {}{}".format(url, platform))
            print (str(e))
            return text_list
        
        # limited format checking, just trims entries that don't fit

        # format lines 16 characters per line
        # This is less than other displays so only show time and destination
        # time[5], space, destination [10]
        if 'train1' in train_data:
            text_list[0] = train_data['train1'][0][:5]
            text_list[0] += " "
            text_list[0] += train_data['train1'][1][:10]
            
        if 'train2' in train_data:
            text_list[1] = train_data['train2'][0][:5]
            text_list[1] += " "
            text_list[1] += train_data['train2'][1][:10]
            
        # time is a single entry - 
        if 'time' in train_data:
            # 5 spaces
            text_list[2] = "     "
            text_list[2] += train_data['time'][:5]
            
    return text_list
    
    
    
if __name__ == "__main__":
    main()