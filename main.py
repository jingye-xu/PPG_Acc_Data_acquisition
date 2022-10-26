import time
import argparse
import RPi.GPIO as GPIO
import time
from max30102 import MAX30102
from mma8452Q import MMA8452Q
import threading
import csv


class data_acquisition():
    def __init__(self, filename="test", gpio_pin=7):
        
        self.filename = filename + ".csv"
        self.interrupt = gpio_pin
        self.data_raw = []

        # set gpio mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.interrupt, GPIO.IN)

    # save the results in the file
    def save_result(self, destination_file, result):
        with open(destination_file, "a") as fr:
            csv_write = csv.writer(fr)
            csv_write.writerow(result)

    # save contents of list to file
    def save_list_to_file(self, destination_file, listname):
        for i in listname:
            self.save_result(destination_file, i)
    
    # main run function
    def run(self):

        sensor1 = MAX30102(channel=1)
        accelerometer = MMA8452Q(channel=1)

        # run until told to stop
        while not self._thread.stopped:
            
            # when inturrupt pin is pulled down by ppg sensor
            if GPIO.input(self.interrupt) == 0:
                red, ir = sensor1.read_fifo()
                x, y, z = accelerometer.read()
                datestamp_s_uni = time.time()
                datestamp_f_uni = time.strftime("%H:%M:%S", time.localtime(datestamp_s_uni))
                self.data_raw.append([datestamp_s_uni, datestamp_f_uni, red, ir, x, y, z])
                print(datestamp_s_uni, red, ir, x, y, z)

        sensor1.shutdown()
    
    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.stopped = False
        self._thread.start()
        print("start collecting data")

    def stop(self, timeout=2.0):
        self._thread.stopped = True
        self._thread.join(timeout)

        # save the lists to files
        print("save raw data to files")
        save_start = time.time()
        head_data_raw = ["date_s", "date_f", "red", "ir", "x", "y", "z"]
        self.save_result(self.filename, head_data_raw)
        self.save_list_to_file(self.filename, self.data_raw)
        save_end = time.time()
        print("save process finished and cost %s seconds" % (save_end - save_start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and print data from mma8452Q")
    parser.add_argument("-t", "--time", type=int, default=30, help="duration in seconds to read from sensor, default 30")
    parser.add_argument("-n", "--name", type=str, default="text", help="prefix of the filename")

    args = parser.parse_args()

    instance1 = data_acquisition(filename=args.name)

    instance1.start()

    try:
        time.sleep(args.time)
    except KeyboardInterrupt:
        print("interrupted")

    instance1.stop()
