"""
Main CLI entry point for Token Scalper Bot
"""

import argparse
import logging
from scalper_bot import TokenScalper
from wallet_generator import main as wallet_gen_main
from airdrop_finder import AirdropFinder

logging.basicConfig(level=logging.INFO)

def run_bot(config_path):
    bot = TokenScalper(config_path)
    bot.search_and_participate_airdrops()
    # You can add more bot actions here (e.g., start trading loop)

def search_airdrops():
    finder = AirdropFinder()
    airdrops = finder.get_good_airdrops()
    for a in airdrops:
        print(f"{a.get('title', a.get('name', 'unknown'))}: {a.get('website')}")
    print(f"Total good airdrops found: {len(airdrops)}")

def generate_wallets():
    wallet_gen_main()

def main():
    parser = argparse.ArgumentParser(description="Token Scalper Bot CLI")
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('run', help='Run the scalper bot')
    subparsers.add_parser('airdrops', help='Search for good airdrop opportunities')
    subparsers.add_parser('genwallets', help='Generate wallets and export to .env')

    args = parser.parse_args()

    if args.command == 'run':
        run_bot(args.config)
    elif args.command == 'airdrops':
        search_airdrops()
    elif args.command == 'genwallets':
        generate_wallets()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
