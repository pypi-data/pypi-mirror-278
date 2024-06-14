# Event Subscriber

A tool to subscribe and handle Ethereum events.

## Installation

```bash
pip install event_subscriber

Usage
The event_subscriber command can be used to start the event listener. Here is a step-by-step guide on how to use the tool:

Enter contract address: Provide the Ethereum contract address you want to monitor.

Example
event_subscriber

Follow the prompts to provide the necessary information:
Enter contract address: //Contract address
Enter path to contract ABI file: abi.json
Enter connection URL for Ethereum node (e.g. http://127.0.0.1:8545, default is Ganache http://127.0.0.1:8545: //Make sure you are connecting to a live node or test node like ganache
Enter polling interval in seconds: 2
Enter starting block number for event filter (default is 'latest'): 
Enter ending block number for event filter (default is 'latest'): 
Enter event name to filter for (or leave empty to finish): Withdraw //Examole
Enter event name to filter for (or leave empty to finish): Deposit  //Examole
Enter event name to filter for (or leave empty to finish): 

The tool will then start monitoring the specified events and provide real-time updates in the console.

Optional: Simulate a transaction: If you want to simulate a transaction for testing purposes, you can use the --simulate flag.
event_subscriber --simulate


Use Cases
On-chain monitoring: Keep track of specific events occurring in a smart contract deployed on the Ethereum blockchain.
Development and testing: Use a local Ethereum node like Ganache to test and develop smart contracts by simulating events and transactions.
Purple teaming: Utilize the tool to monitor and analyze potential security threats and attacks on smart contracts in real-time.
Real-time event tracking: Get real-time information about events happening in the contract, such as large withdrawals or deposits.
Incident response: Quickly identify and respond to suspicious activities or anomalies in the contract behavior.


Troubleshooting
If you encounter issues, ensure that:

The Ethereum node URL is correct and accessible.
The contract address and ABI file path are correct.
The polling interval is set to a reasonable value to avoid rate limiting.
For more detailed logs, check the event.log file generated in the working directory.


