from easyhid import Enumeration
import time

def parse_hid(hid_bytes, device_idx):
    strb = hid_bytes.hex()
    if strb[5:8] == "40b":
        # status frame
        print("["+str(device_idx)+"] Status frame ["+str(lsb_shift_hex_to_int(strb[8:12]))+"]")
    if strb[5:8] == "13c":
        # event frame
        trackpad_x = strb[40:44] # lsb
        trackpad_y = strb[44:48] # lsb
        trigger_pos = strb[52:56] # lsb
        grip_btn = strb[18] # 4 = pressed
        trackpad_click = strb[21] # 4 = pressed
        trig_click = strb[17] # 1 = pressed
        menu_click = strb[18] # 1 = pressed
        battery_status = strb[124:128] # lsb

        # convert values
        trackpadx_int = lsb_shift_hex_to_int(trackpad_x)
        trackpady_int = lsb_shift_hex_to_int(trackpad_y)
        trigger_pos_int = lsb_shift_hex_to_int(trigger_pos)
        battery_status_int = lsb_shift_hex_to_int(battery_status)

        # shift trackpad values, because we want 0 = center, negative left or down, positive right or up
        if trackpadx_int > 32768:
            trackpadx_int = trackpadx_int - 65536
        if trackpady_int > 32768:
            trackpady_int = trackpady_int - 65536

        if trackpad_click == "4":
            trackpad_click = True
        else:
            trackpad_click = False

        if grip_btn == "4":
            grip_btn = True
        else:
            grip_btn = False

        if trig_click == "1":
            trig_click = True
        else:
            trig_click = False

        if menu_click == "1":
            menu_click = True
        else:
            menu_click = False

        # print status
        print("["+str(device_idx)+"] Event frame ["+str(int(strb[10:12]+strb[8:10], 16))+"]")
        print("\tTrackpad: ")
        print("\t\t(x, y, click)\t"+str(trackpadx_int)+", "+str(trackpady_int)+", "+str(trackpad_click))
        print("\tTrigger: ")
        print("\t\t(pos, click)\t"+str(trigger_pos_int)+", "+str(trig_click))
        print("\tBattery: ")
        print("\t\t(percent)\t"+str(battery_status_int)+" %")
        print("\tGrip Button: ")
        print("\t\t(click)\t"+str(grip_btn))
        print("\tMenu Button: ")
        print("\t\t(click)\t"+str(menu_click))

def lsb_shift_hex_to_int(lsbstring):
    return int(lsbstring[2:4]+lsbstring[0:2],16)


# Stores an enumeration of all the connected USB HID devices
en = Enumeration()

# return a list of devices based on the search parameters
vive_wands = en.find(vid=0x28de, pid=0x2012, interface=2)
vive_wand_0 = False
vive_wand_1 = False

if len(vive_wands) == 1:
    vive_wand_0 = vive_wands[0]
if len(vive_wands) == 2:
    vive_wand_1 = vive_wands[1]


if len(vive_wands) > 0:
    if vive_wand_0:
        vive_wand_0.open()
    if vive_wand_1:
        vive_wand_1.open()

    while True:
        if vive_wand_0:
            parse_hid(vive_wand_0.read(), 0)
        if vive_wand_1:
            parse_hid(vive_wand_0.read(), 1)

        # use this to get raw values:
        # print(vive_wand_0.read().hex())

    # this is never reached...just do it, if you communicate in production
    if vive_wand_0:
        vive_wand_0.close()
    if vive_wand_1:
        vive_wand_1.close()
else:
    print("No Vive wands found!")
