import pycom
import time
from machine import Pin
from dth import DTH

# Disable LED heartbeat (so we can control the LED)
pycom.heartbeat(False)
# Assign 'P3' as input pin or sensor read
th = DTH('P3',0)

print("\n*** Sensor Node successfully booted! ***\n")
