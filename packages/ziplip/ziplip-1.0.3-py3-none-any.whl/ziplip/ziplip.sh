#!/bin/bash

show_usage() {
    echo "Usage: $0 --zip <zip_file> --pass <password_list> [--unzip] [--save <file>] [--silent]"
    exit 1
}

# Initialize variables
zip_file=""
password_list=""
unzip_flag=false
save_file=""
silent_flag=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --zip)
            zip_file="$2"
            shift 2
            ;;
        --pass)
            password_list="$2"
            shift 2
            ;;
        --unzip)
            unzip_flag=true
            shift
            ;;
        --save)
            save_file="$2"
            shift 2
            ;;
        --silent)
            silent_flag=true
            shift
            ;;
        *)
            show_usage
            ;;
    esac
done

# Check if required arguments are provided
if [[ -z "$zip_file" || -z "$password_list" ]]; then
    show_usage
fi

# Check if the zip file exists
if [ ! -f "$zip_file" ]; then
    echo "Error: Zip file not found: $zip_file"
    exit 1
fi

# Check if the password list exists
if [ ! -f "$password_list" ]; then
    echo "Error: Password list not found: $password_list"
    exit 1
fi

# Function to attempt password extraction
try_password() {
    local password="$1"
    unzip -t -P "$password" "$zip_file" >/dev/null 2>&1
    return $?
}

# Counter for password attempts
attempt=0

# Attempt to find the correct password
while IFS= read -r password || [ -n "$password" ]; do
    ((attempt++))
    if ! $silent_flag; then
        printf "[%02d] Trying password: %s\n" "$attempt" "$password"
    fi

    if try_password "$password"; then
        echo "Password found: $password"
        
        if [ -n "$save_file" ]; then
            echo "$password" > "$save_file"
            echo "Password saved to $save_file"
        fi
        
        if $unzip_flag; then
            unzip -o -P "$password" "$zip_file"
            echo "Zip file extracted."
        fi
        exit 0
    fi
done < "$password_list"

echo "Error: Password not found in the list."
exit 1
