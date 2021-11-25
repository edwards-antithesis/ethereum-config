import argparse
import requests
from time import sleep

def get_with_retry(url, desired_response_code=200, timeout=5, retries=30, retry_delay=15):
    print(f"Attempting {url}")
    attempt = 1
    last_response = None
    while attempt <= retries:
        status_code = 500
        try:
            last_response = requests.get(url, timeout=timeout)
            status_code = last_response.status_code
            print(f"status_code={status_code}; response={last_response.json()}")
        except:
            pass
        if status_code != desired_response_code:
            print(f"\tattempt={attempt}/{retries}; delay={retry_delay}s")
            sleep(retry_delay)
            attempt += 1
        else:
            break
    return last_response

# Python 3.x replacement for the Python 2.x execfile function
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Antithesis experiment control")
    parser.add_argument(
        'beacon_node',
        help='Hostname (and optional port) to a beacon node to use for API calls')
    parser.add_argument(
        'workload',
        help='Full path to the workload script to use')
    parser.add_argument(
        '--genesis-retries',
        dest='genesis_retries',
        default=30,
        type=int,
        help='Number of attempts to get a successful genesis reponse')
    parser.add_argument(
        '--genesis-retry-delay',
        dest='genesis_retry_delay',
        default=15,
        type=int,
        help='Seconds to delay between retry attempts')
    parser.add_argument(
        '--slot',
        dest='target_slot',
        default=64,
        type=int,
        help='Target slot to detect before running workload')
    parser.add_argument(
        '--slot-retries',
        dest='slot_retries',
        default=30,
        type=int,
        help='Number of attempts to get a successful status reponse on the target slot')
    parser.add_argument(
        '--slot-retry-delay',
        dest='slot_retry_delay',
        default=60,
        type=int,
        help='Seconds to delay between retry attempts')

    params = parser.parse_args()

    # wait for genesis
    print(f"wrapper: waiting for genesis (retries={params.genesis_retries}; retry_delay={params.genesis_retry_delay})")
    r = get_with_retry(
        f"http://{params.beacon_node}/eth/v1/beacon/genesis",
        retries=params.genesis_retries,
        retry_delay=params.genesis_retry_delay)
    if(r is None or r.status_code != 200):
        print(f"antithesis: terminate experiment -- no genesis block detected after {params.genesis_retries * params.genesis_retry_delay} seconds")
        exit(-1)

    # wait for the first 2 epocs (2 * 32 slots) before starting the workload
    print(f"wrapper: waiting for slot {params.target_slot} (retries={params.slot_retries}; retry_delay={params.slot_retry_delay})")
    r = get_with_retry(
        f"http://{params.beacon_node}/eth/v1/beacon/headers/{params.target_slot}",
        retries=params.slot_retries,
        retry_delay=params.slot_retry_delay)
    if(r is None or r.status_code != 200):
        print(f"antithesis: terminate experiment -- did not detect slot {params.target_slot} after {params.slot_retries * params.slot_retry_delay} seconds")
        exit(-1)

    # kick-off workload
    print(f"wrapper: starting workload '{params.workload}'")
    execfile(params.workload)
