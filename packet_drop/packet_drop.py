import re
import time
import logging
from typing import List, Dict
from subprocess import check_output

# Ping returns results in:
# rtt min/avg/max/mdev = 9.576/11.802/16.541/2.482 ms


# def average(numbers: List[float]) -> float:
#     return round( ( ( numbers[0] + numbers[1] ) / 2.00 ) , 2 )

def update_average(avg_dict: Dict, avg_type: str, number: float) -> float:
    avg_dict[avg_type].append(number)
    
    avg = 0
    for num in avg_dict[avg_type]:
        avg += num
    
    return round( avg / len(avg_dict[avg_type]) , 2 )
    

# Define some globals here
averages = {'min': [],
            'avg': [],
            'max': [],
            'mdev': [],
            }
stats_re = re.compile(r'=\s(.+)\sms')
server = '8.8.8.8'
pings = 3


if __name__ == '__main__':
    # Start a timer, we'll use this to dumb averages every ~1 minute
    start = time.time()

    while True:
        # Create ping process
        # Sleep same number of seconds as number of pings for process to finish
        ping = check_output(['ping', '-q', '-c', str(pings), server])
        time.sleep(pings)

        # Parse output of ping process for ping stats
        match = re.findall(stats_re, ping.decode())

        # If we found a match
        if match:
            index = 0  # need something to track which part of min/avg/max/mdev we are on
            avs = match[0].split('/')
            for key in averages:
                # Update current dict value with average of current + ping output
                # Print and iterate index variable
                print(update_average(averages, key, float(avs[index])))
                index += 1
