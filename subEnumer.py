import requests
import sys
from threading import Thread, Lock
from queue import Queue

q = Queue()
list_lock = Lock()
subs = []

def scan_subdomains(domain):
    global q
    while True:
        # Get next sub from queue
        subdomain = q.get()
        # Scan the subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered:", url)
            # Add sub to global list
            with list_lock:
                subs.append(url)

        # Done checking this subdomain
        q.task_done()


def main(domain, n_threads, subdomains):
    global q

    # Queue all subdomains
    for subdomain in subdomains:
        q.put(subdomain)

    for t in range(n_threads):
        # Start threads
        worker = Thread(target=scan_subdomains, args=(domain,))
        # Set workers to daemons
        worker.daemon = True
        worker.start()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Faster Subdomain Scanner using Threads")
    parser.add_argument("-d", "--domain", help="Domain to scan for subdomains without protocol (e.g without 'http://' or 'https://')")
    parser.add_argument("-w", "--wordlist", help="File that contains all subdomains to scan, line by line.")
    parser.add_argument("-t", "--num-threads", help="Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    parser.add_argument("-o", "--out-file", help="Specify the output text file to write discovered subdomains. Default is discovered-subdomains.txt", default="discovered-subdomains.txt")
    
    args = parser.parse_args()
    # Verify a domain was supplied
    if not args.domain:
        print("[-] No domain specified. See --help for more info")
        sys.exit(1)
    domain = args.domain

    # Verify a wordlist was supplied
    if not args.wordlist:
        print("[-] No wordlist specified. See -h/--help for more info")
        sys.exit(1)
    wordlist = args.wordlist

    # Grab defaults or passed args
    num_threads = args.num_threads
    out_file = args.out_file

    main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()

    # Save output to file
    with open(out_file, "w") as f:
        for url in subs:
            print(url, file=f)