#!/usr/bin/env python3

import importlib
import os
import sys
import argparse
from stats import astrophotography_stats, detailed_panel_stats, session_stats


def display_menu():
    print("\nSelect an option:")
    print("1. Generate Overall Statistics")
    print("2. Generate Detailed Panel Statistics")
    print("3. Generate Session Statistics")
    print("4. Exit")

def validate_root_directory(root_dir):
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        print("\nUsage: python3 entry_point.py [root_dir]")
        print("If 'root_dir' is not provided, it defaults to 'Lights'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate statistics.')
    parser.add_argument('root_dir', nargs='?', default='Lights', help='Root directory for your Lights')
    args = parser.parse_args()
    root_dir = args.root_dir

    validate_root_directory(root_dir)

    os.system('clear')

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            astrophotography_stats.main(root_dir=root_dir)
        elif choice == '2':
            detailed_panel_stats.main(root_dir=root_dir)
        elif choice == '3':
            panels_input = input("Enter list of panels (separated by space, or leave empty for all panels): ")
            panels = panels_input.split() if panels_input else None
            session_stats.main(root_dir=root_dir, panels=panels)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
