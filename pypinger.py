import concurrent.futures
import logging
import os
import sys
from logging import INFO, Logger
from subprocess import run, CalledProcessError, DEVNULL


def create_logger() -> Logger:
    """ Return custom logger """
    logging.basicConfig(format='%(message)s', level=INFO)
    return logging.getLogger('pypinger')


def ping(host: str, failed: list) -> bool:
    """ Ping ip and return bool indicating success """
    command = ['ping', '-c', '1', '-t', '1', host]
    try:
        run(command, check=True, stdout=DEVNULL, stderr=DEVNULL)
        return True
    except CalledProcessError:
        failed.append(host)
        return False


def print_output(log, failed: list):
    """ Print out failures """
    if len(failed) == 0:
        log.info('No errors')
    else:
        log.info('Failures')
        for fail in failed:
            log.info(fail)


if __name__ == '__main__':
    logger = create_logger()
    logger.debug('start')

    failures = []
    ips = ['www.google.com', 'junk.junk', 'www.yahoo.com']
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for ip in ips:
            executor.submit(ping, ip, failures)

    print_output(logger, failures)
    logger.debug('end')
