# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 15:37:11 2021

@author: thijn
"""
### SPI-der interface for MCP4822 and Arduino NANO ###
import time

def setup(arduino):
    # Sets up DAC for Arduino NANO
    #SPI: 10 (SS), 11 (MOSI), 12 (MISO), 13 (SCK).
    
    # Setup pins    
    global cs
    global mosi
    global sck
    
    cs = 1
    time.sleep(1)
    
    cs = arduino.get_pin('d:10:o') #SS
    mosi = arduino.get_pin('d:11:o') #MOSI
    sck = arduino.get_pin('d:13:o') #SCLK
        
    # Deselect DAC
    cs.write(1)
    sck.write(0) # Ensure clock output at low
        
    # Confirm setup
    global DACisSetUp
    DACisSetUp = True
        
def fastWrite(voltage, DAC='A'): 
    # Ulgy code that should run faster
    # Defaults to DAC A, Clock frequency in Hz
    assert voltage <= 5, 'The requested voltage out is too high'
    assert DAC == 'A' or DAC == 'B', 'Please input as string either A or B'
    assert DACisSetUp , 'Please set up the DAC first'

    # **DETERMINE CORRECT DAC SETTINGS**
    # Set to 0 for DAC A. Set to 1 for DAC B
    gain_select = 1
    if voltage > 2.04975: gain_select = 0
    
    # Set to 1 for unity gain. Set to 0 for gain = 2.
    dac_select = 0
    if DAC == 'B': dac_select = 1
    
    # **CALCULATE OUTPUT SIGNAL**
    # Max 4095 --> 2.04975V
    signal = int(voltage*4095/(2.04975*(2-gain_select)) )
    
    # Generate config bits and write full datastream
    config = str(dac_select)+'0'+str(gain_select)+'1'
    data = format(signal, '012b')
    data = config + data
    
    # Select DAC Chip
    cs.write(0)
    #time.sleep(.1)    
    
    # Send
    for ii in range(16):
        mosi.write(int(data[ii]))   # Send single bit
        #time.sleep(1/freq*.5)
        sck.write(1)                # Clock HIGH
        #time.sleep(1/freq*.5)
        sck.write(0)                # Clock LOW
    
    # Deselect DAC Chip
    #time.sleep(.1)  
    cs.write(1)
    return
    
def write(voltage, DAC='A', freq=18): 
    # Overkill frequency to make sure this runs as fast as possible
    # Defaults to DAC A, Clock frequency in Hz
    assert voltage <= 5, 'The requested voltage out is too high'
    assert DAC == 'A' or DAC == 'B', 'Please input as string either A or B'
    assert DACisSetUp , 'Please set up the DAC first'

    # **DETERMINE CORRECT DAC SETTINGS**
    # Set to 0 for DAC A. Set to 1 for DAC B
    gain_select = 1
    if voltage > 2.04975: gain_select = 0
    
    # Set to 1 for unity gain. Set to 0 for gain = 2.
    dac_select = 0
    if DAC == 'B': dac_select = 1
    
    # **CALCULATE OUTPUT SIGNAL**
    # Max 4095 --> 2.04975V
    signal = int(voltage*4095/(2.04975*(2-gain_select)) )
    
    # Generate config bits and write full datastream
    config = str(dac_select)+'0'+str(gain_select)+'1'
    data = format(signal, '012b')
    data = config + data
    
    # Select DAC Chip
    cs.write(0)
    time.sleep(.1)    
    
    # Send
    start = time.time()
    
    for ii in range(16):
        mosi.write(int(data[ii]))   # Send single bit
        time.sleep(1/freq*.5)
        sck.write(1)                # Clock HIGH
        time.sleep(1/freq*.5)
        sck.write(0)                # Clock LOW
    
    # Deselect DAC Chip
    time.sleep(.1)  
    cs.write(1)
    
    final_freq = int(1/(time.time()-start/16))
    
    return final_freq

def shutdown(DAC='A', freq=10):
    # Defaults to DAC A, Clock frequency in Hz
    assert DAC == 'A' or DAC == 'B', 'Please input as string either A or B'
    assert DACisSetUp , 'Please set up the DAC first'

    global cs
    global mosi
    global sck
    global arduino

    # **DETERMINE CORRECT DAC SETTINGS**
    # Set to 0 for DAC A. Set to 1 for DAC B
    dac_select = 0
    if DAC == 'B': dac_select = 1
    
    # **CALCULATE OUTPUT SIGNAL**
    # Generate config bits and write full datastream
    data = str(dac_select)+'010000000000000'
    
    # Select DAC Chip
    cs.write(0)
    time.sleep(.1)    
    
    # Send
    for ii in range(16):
        mosi.write(int(data[ii]))   # Send single bit
        time.sleep(1/freq*.5)
        sck.write(1)                # Clock HIGH
        time.sleep(1/freq*.5)
        sck.write(0)                # Clock LOW
    
    # Deselect DAC Chip
    time.sleep(.1)  
    cs.write(1)

