import re
import time
import logging
import subprocess

import stats_db

from datetime import datetime
from typing import List, Dict


def update_average(avg_dict: Dict, avg_type: str, number: float) -> None:
    avg_dict[avg_type].append(number)


def calculate_average(avg_dict: Dict, avg_type: str) -> float:
    if len(avg_dict[avg_type]) == 0:
        return 0.00
    return round( ( sum( avg_dict[avg_type] ) / len( avg_dict[avg_type] ) ) , 2 )
    

# Define some globals here
stats_database = 'test.db'
logname = 'test.log'
averages = {'min': [],
            'avg': [],
            'max': [],
            'mdev': [],
            'per': []
            }  # type: Dict
server = '8.8.8.8'

check_time = 60  # check_time and pings should both be the same right now, I need to make this better
pings = 10

# Compile some regex objections for searching stat output
loss_re = re.compile(r'(\d{1,3})\%')
stats_re = re.compile(r'=\s(.+)\sms')


if __name__ == '__main__':
    # Set up database
    stats_db.create_db(stats_database)

    # Set up log file
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filename=logname,
                        level=logging.INFO
                        )
    log = logging.getLogger()
    log.info(f'Using database {stats_database}')

    # Start a timer, we'll use this to dump averages every ~1 minute
    start = time.time()

    while True:
        try:
            # Create ping process
            # Sleep same number of seconds as number of pings for process to finish
            response = subprocess.check_output(['ping', '-q', '-c', str(pings), server])
            
            time.sleep(pings)  # this only really works if 1 ping ~ 1 second, might need to find a better way to do this here

            # Parse output of ping process for ping stats
            decoded = response.decode()
            loss = re.findall(loss_re, decoded)
            match = re.findall(stats_re, decoded)

            # If we found a match
            if match:
                index = 0  # need something to track which part of min/avg/max/mdev we are on
                avs = match[0].split('/')
                results_dict = {'per': loss[0],
                                'min': avs[0],
                                'avg': avs[1],
                                'max': avs[2],
                                'mdev': avs[3],
                                }

                for key in averages:
                    # Update current dict value with average of current + ping output
                    # Print and iterate index variable
                    update_average(averages, key, float(results_dict[key]))
                    index += 1
        except subprocess.CalledProcessError:
            pass

        if time.time() >= start + check_time:  # if we go over our check_time interval, dump stats
            stats_list = [datetime.now().replace(microsecond=0).isoformat(sep=" "),
                          calculate_average(averages, 'per'),
                          calculate_average(averages, 'min'),
                          calculate_average(averages, 'avg'),
                          calculate_average(averages, 'max'),
                          calculate_average(averages, 'mdev')
                          ]
            log.info(f'RAW || Per: {averages["per"]}, Min: {averages["min"]}, Avg: {averages["avg"]}, Max: {averages["max"]}, Mdev: {averages["mdev"]}')
            log.info(f'AVG || Per: {stats_list[1]}, Min: {stats_list[2]}, Avg: {stats_list[3]}, Max: {stats_list[4]}, Mdev: {stats_list[5]}')
            
            stats_db.add_record(stats_database, stats_list)  # dump stats to database
            
            for key in averages.keys():  # reset our averages dictionary
                averages[key] = []

            start = time.time()  # reset our timer
