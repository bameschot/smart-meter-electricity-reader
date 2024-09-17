import serial
import re
import time
import datetime
import calendar

from models import MeterReading, MeterReadings

class P1MeterReader:
    def __init__(self):
        self.lastReading = None
        self.meterReadings = MeterReadings([])
        
        
    def runReader(self):

        try:
            # Seriele poort confguratie
            ser = serial.Serial()

            #dsmr 4.0 > 
            ser.baudrate = 115200
            ser.bytesize = serial.EIGHTBITS
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
          

            ser.xonxoff = 0
            ser.rtscts = 0
            ser.timeout = 12
            ser.port = "/dev/ttyUSB0"
            ser.close()

            print("Reader Started")
            while True:
                ser.open()
                checksum_found = False

                t1TotalEnergyImportKwh = 0.0
                t2TotalEnergyImportKwh = 0.0
                t1TotalEnergyExportKwh = 0.0
                t2TotalEnergyExportKwh = 0.0
                currentEnergyImportW = 0.0
                currentEnergyExportW = 0.0

                while not checksum_found:
                    telegram_line = ser.readline()  # read line from serial port
                    #print('-------------------------------------')
                    #print(telegram_line.decode('ascii').strip())
                    strVal = telegram_line.decode('UTF-8')
                    
                    # check for obis and assign value
                    if("1-0:1.8.1" in strVal):
                        t1TotalEnergyImportKwh = float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])

                    if("1-0:1.8.2" in strVal):
                        t2TotalEnergyImportKwh = float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])

                    if("1-0:2.8.1" in strVal):
                        t1TotalEnergyExportKwh = float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])

                    if("1-0:2.8.2" in strVal):
                        t2TotalEnergyExportKwh = float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])

                    if("1-0:1.7.0" in strVal):
                        currentEnergyImportW = int(float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])*1000)

                    if("1-0:2.7.0" in strVal):
                        currentEnergyExportW = int(float(
                            strVal.split('(')[1].split(')')[0].split('*')[0])*1000)
                   
                    # Check if end of telegram and create the time serie object
                    if re.match(b'(?=!)', telegram_line):
                        #set current use
                        now = datetime.datetime.now()
                        
                        newReading = MeterReading(
                            now.isoformat().split('.')[0],
                            calendar.timegm(now.timetuple()),
                            currentEnergyImportW+-currentEnergyExportW
                        )
                        
                        self.lastReading = newReading
                        
                        #store the reading if the interval is correct
                        if len(self.meterReadings.readings) == 0 or newReading.timestamp - self.meterReadings.readings[-1].timestamp > 30:
                            self.meterReadings.readings.append(newReading)
                            print("Appending reading to readings, size: "+str(len(self.meterReadings.readings)))
                            
                        if len(self.meterReadings.readings) > 10000:
                            del self.meterReadings.readings[0]
                            
    
                        #Mark the reading of the frame as complete
                        checksum_found = True


                #close the serial connection
                ser.close()
        #except:
        #    print("No reader was started")
        finally:
            print("?")
            