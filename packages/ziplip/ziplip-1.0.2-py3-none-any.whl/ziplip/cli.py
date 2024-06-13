#!/usr/bin/env python3
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Find password for a zip file")
    parser.add_argument("--zip", help="Path to the zip file", required=True)
    parser.add_argument("--pass", help="Path to the password list file", required=True)
    parser.add_argument("--unzip", help="Extract the zip file if password is found", action="store_true")
    parser.add_argument("--save", help="Save the found password to a file")
    parser.add_argument("--silent", help="Suppress output of password attempts", action="store_true")
    return parser.parse_args()

def try_password(zip_file, password):
    try:
        subprocess.check_output(['unzip', '-t', '-P', password, zip_file], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    args = parse_arguments()
    
    with open(args.pass, 'r') as pass_file:
        passwords = pass_file.read().splitlines()

    print(f"Trying to find the password for {args.zip}...")
    
    attempt = 0
    for password in passwords:
        attempt += 1
        if not args.silent:
            print(f"[{attempt:02d}] Trying password: {password}")
        if try_password(args.zip, password):
            print(f"Password found: {password}")
            if args.save:
                with open(args.save, 'w') as save_file:
                    save_file.write(password)
                print(f"Password saved to {args.save}")
            if args.unzip:
                subprocess.run(['unzip', '-P', password, args.zip])
                print("Zip file extracted.")
            return

    print("Error: Password not found in the list.")

if __name__ == "__main__":
    main()
