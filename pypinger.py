""" Simple pinging module """
from concurrent.futures import ThreadPoolExecutor
from logging import INFO, Logger, basicConfig, getLogger
from subprocess import run, CalledProcessError, DEVNULL


def create_logger() -> Logger:
    """ Return custom logger """
    basicConfig(format='%(message)s', level=INFO)
    return getLogger('pypinger')


def ping(host: str, failed: list) -> bool:
    """ Ping ip and return bool indicating success """
    command = ['ping', '-c', '1', '-t', '1', host]
    try:
        run(command, check=True, stdout=DEVNULL, stderr=DEVNULL)
        return True
    except CalledProcessError:
        failed.append(host)
        return False


def print_output(log: Logger, failed: list):
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
    hostnames = ['www.google.com', 'junk.junk', 'www.yahoo.com']
    with ThreadPoolExecutor(max_workers=100) as executor:
        for hostname in hostnames:
            executor.submit(ping, hostname, failures)

    print_output(logger, failures)
    logger.debug('end')
