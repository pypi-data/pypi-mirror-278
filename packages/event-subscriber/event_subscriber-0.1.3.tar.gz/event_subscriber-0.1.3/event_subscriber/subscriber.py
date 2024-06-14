import argparse
from web3 import Web3
import asyncio
import json
import colorama
from colorama import Fore, Style
import pyfiglet
import logging
from datetime import datetime

# Initialize colorama module
colorama.init()

# Print welcome message
print(pyfiglet.figlet_format("5m477 Events", font="slant"))

# Set threshold for detecting large withdrawals
LARGE_WITHDRAWAL_THRESHOLD = Web3.toWei(10, 'ether')  # Example threshold

def setup_logging():
    logging.basicConfig(filename='event.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_valid_url():
    while True:
        url = input("Enter connection URL for Ethereum node (e.g. http://127.0.0.1:8545, default is Ganache http://127.0.0.1:8545): ") or "http://127.0.0.1:8545"
        try:
            web3 = Web3(Web3.HTTPProvider(url))
            if web3.isConnected():
                return url
            else:
                print("Unable to connect to the URL. Please try again.")
        except Exception as e:
            print(f"Invalid URL: {e}. Please try again.")

def get_contract():
    target_address = input("Enter contract address: ")
    abi_file_path = input("Enter path to contract ABI file: ")

    try:
        with open(abi_file_path, 'r') as abi_file:
            target_ABI = json.load(abi_file)

        web3 = Web3(Web3.HTTPProvider(get_valid_url()))
        target = web3.eth.contract(address=target_address, abi=target_ABI)
        return target, web3
    except Exception as e:
        print(f"Error loading contract: {e}")
        return None, None

def get_valid_integer_input(prompt, default=None):
    while True:
        value = input(prompt)
        if value == "":
            if default is not None:
                return default
            else:
                print("Value cannot be empty. Please try again.")
        elif not value.isdigit():
            print("Invalid input. Please enter a numeric value.")
        else:
            return int(value)

def get_event_filters(contract):
    from_block = get_valid_integer_input("Enter starting block number for event filter (default is 'latest'): ", default="latest")
    to_block = get_valid_integer_input("Enter ending block number for event filter (default is 'latest'): ", default="latest")
    
    event_filters = []
    while True:
        event_name = input("Enter event name to filter for (or leave empty to finish): ")
        if not event_name:
            break

        # Get event object from contract ABI
        event_abi = [e for e in contract.abi if e["type"] == "event" and e["name"] == event_name]
        if not event_abi:
            print("Invalid event name. Please try again.")
            continue

        event = contract.events[event_name]
        event_filter = event.createFilter(fromBlock=from_block, toBlock=to_block)
        event_filters.append((event_name, event_filter))

    return event_filters, from_block, to_block

# Define event handler function
def event_handler(event, event_name):
    # Extract event data
    block_number = event.blockNumber
    tx_hash = event.transactionHash.hex()

    # Extract argument values
    args = {k: v for k, v in event.args.items() if not k.startswith('__')}

    log_message = f"New {event_name} event detected! Block Number: {block_number}, Transaction Hash: {tx_hash}, Arguments: {args}"
    print(log_message)
    logging.info(log_message)

    # Check for malicious activity
    if event_name == 'Withdrawal' and args.get('amount', 0) >= LARGE_WITHDRAWAL_THRESHOLD:
        alert_message = f"{Fore.RED}Alert! Large withdrawal detected: {args.get('amount')} Wei at {datetime.now()} {Style.RESET_ALL}"
        print(alert_message)
        logging.warning(alert_message)
        # Additional actions (e.g., sending an alert email) can be added here

    # Log event data
    print(f"{Fore.GREEN}New {event_name} event detected!")
    print(f"Block Number: {block_number}")
    print(f"Transaction Hash: {tx_hash}")
    print(f"Arguments: {args}{Style.RESET_ALL}\n")

async def event_loop(event_filters, interval):
    while True:
        for event_name, event_filter in event_filters:
            for event in event_filter.get_new_entries():
                event_handler(event, event_name)
        await asyncio.sleep(interval)

def simulate_transaction(web3, contract):
    account = web3.eth.accounts[0]  # Using the first Ganache account for simplicity
    tx = {
        'from': account,
        'to': contract.address,
        'value': web3.toWei(0.1, 'ether'),  # Example transaction value
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }

    # Replace 'functionName' with an actual function from your contract
    # and 'args' with the appropriate arguments for that function.
    tx_hash = contract.functions.functionName(args).transact(tx)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Transaction receipt: {receipt}")

def main():
    parser = argparse.ArgumentParser(description="Event Subscriber for Ethereum Smart Contracts")
    parser.add_argument('--simulate', action='store_true', help="Simulate a transaction")
    args = parser.parse_args()

    setup_logging()
    # Prompt for contract address and ABI
    target, web3 = get_contract()
    if not target:
        exit()

    # Prompt for polling interval
    interval = get_valid_integer_input("Enter polling interval in seconds: ")

    # Get event filters for specified events
    event_filters, from_block, to_block = get_event_filters(target)
    if not event_filters:
        exit()

    # Simulate a transaction (optional)
    if args.simulate:
        simulate_transaction(web3, target)

    # Run event loop with user-specified options
    try:
        print(f"{Fore.YELLOW}Starting event loop...")
        for event_name, _ in event_filters:
            print(f"Filtering for event '{event_name}' from block {from_block} to {to_block}.")
        print(f"Polling every {interval} seconds.{Style.RESET_ALL}\n")
        asyncio.run(event_loop(event_filters, interval))
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nEvent loop stopped by user.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
