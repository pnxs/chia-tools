#!/usr/bin/env python3
import sqlite3
from datetime import datetime
import argparse
import os

def get_coins(puzzle_hash, blockchain):
        """Show all coins for a given puzzle-hash.
           Prints "timestamp;coin-amount;height"
        """
        con = sqlite3.connect(os.path.expanduser(blockchain))
        cur = con.cursor()

        for row in cur.execute(f"SELECT timestamp, amount, confirmed_index FROM coin_record WHERE puzzle_hash = '{puzzle_hash}' ORDER BY timestamp, amount;"):
                epoch, amount_bytes, confirmed_idx = row
                ts = datetime.fromtimestamp(epoch)
                mojo = int.from_bytes(amount_bytes, byteorder="big", signed=False)
                xch = mojo / 10**12
                print(f"{ts};{xch};{confirmed_idx}")

        con.close()

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Chia-Blockchain-Tool')
        parser.add_argument('-p', '--puzzlehash', dest='puzzle_hash', help='Puzzle-Hash to search for')
        parser.add_argument('-b', '--blockchain', dest='blockchain', help='Specifiy blockchain DB')

        args = parser.parse_args()

        blockchain_file = '~/.chia/mainnet/db/blockchain_v1_mainnet.sqlite'
        if args.blockchain:
                blockchain_file = args.blockchain

        get_coins(args.puzzle_hash, blockchain_file)
