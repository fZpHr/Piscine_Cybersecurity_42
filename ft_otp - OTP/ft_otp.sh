#!/bin/bash

# This script is used to generate a new key, encrypt it and generate a new temporary key

RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'
encrypt_key='42'

is_hex() {
    value=$(cat $1)
    if [[ ${value} =~ ^[0-9a-fA-F]{64}$ ]]; then
        return 0
    else
        return 1
    fi
}

is_crypted() {
    output=$(openssl enc -aes-256-cbc -pbkdf2 -d -in ft_otp.key -pass pass:wrongpassword 2>&1)
    if echo "$output" | grep -q "bad decrypt"; then
        return 0
    elif echo "$output" | grep -q "error reading input file"; then
        echo -e "${RED}The file $2 is not encrypted with AES-256-CBC.${NC}"
        return 1
    else
        echo -e "${RED}The file $2 is likely not encrypted.${NC}"
        return 1
    fi
}

generate_key() {
    if [ -z "$1" ]; then
        echo -e "${RED}Please provide a hexadecimal key of at least 64 characters${NC}"
        exit 1
    fi

    key_content="$1"
    if is_hex "$key_content"; then
        echo -n "$key_content" | openssl enc -aes-256-cbc -pbkdf2 -salt -out ft_otp.key -pass pass:${encrypt_key}
        echo -e "${GREEN}Key stored securely in ft_otp.key${NC}"
    else
        echo -e "${RED}Key is not in hex format or is too short${NC}"
        exit 1
    fi
}

generate_random_key() {
    if [ -z "$1" ]; then
        echo -e "${RED}Please provide the name of the key${NC}"
        exit 1
    fi

    openssl rand -hex 32 | tr -d '\n' > "$1.hex"
    echo -e "${GREEN}Key generated and saved in $1.hex${NC}"
}

generate_otp() {
    if [ "$1" != "ft_otp.key" ]; then
        echo -e "${RED}Please generate the key with -g or provide the key name ft_otp.key${NC}"
        exit 1
    fi

    if [ ! -f "$1" ]; then
        echo -e "${RED}Encrypted key file ft_otp.key not found${NC}"
        exit 1
    fi

    if ! is_crypted; then
        echo -e "${RED}The file $1 is not generated by this script${NC}"
        exit 1
    fi

    key=$(openssl enc -aes-256-cbc -pbkdf2 -d -in "$1" -pass pass:${encrypt_key})
    if [ -z "$key" ]; then
        echo -e "${RED}Failed to decrypt the key${NC}"
        exit 1
    fi

    if ! is_hex "$key"; then
        echo -e "${RED}Decrypted key is not in hex format${NC}"
        exit 1
    fi

    count_file=$(mktemp)
    if [ ! -s "$count_file" ]; then
        echo 0 > "$count_file"
    fi

    count=$(cat "$count_file")
    ((count++))
    echo $count > "$count_file"
    count=$((count + $(date +%s)))

    hex_count=$(printf "%016x" $count)
    hmac=$(echo -n "$hex_count" | openssl dgst -sha1 -mac HMAC -macopt hexkey:$key | sed 's/^.* //')

    offset=$((0x${hmac: -1} & 0xf))

    bin_code=$(( ((0x${hmac:$((offset*2)):2} & 0x7f) << 24 ) | \
                ((0x${hmac:$((offset*2+2)):2} & 0xff) << 16 ) | \
                ((0x${hmac:$((offset*2+4)):2} & 0xff) << 8 ) | \
                (0x${hmac:$((offset*2+6)):2} & 0xff) ))

    bin_code=$((bin_code & 0x7fffffff))

    hotp=$((bin_code % 1000000))

    printf "${GREEN}%06d\n" $hotp
}

if [ "$#" -gt 2 ]; then
    echo -e "${RED}Too many arguments${NC}"
    exit 1
fi

case "$1" in
    -g)
        generate_key "$2"
        ;;
    -n)
        generate_random_key "$2"
        ;;
    -k)
        generate_otp "$2"
        ;;
    *)
        echo -e "${BLUE}Possible options are:   -n : Generate a new key 64 hex characters
                        -g : Encrypt the key
                        -k : Generate a new temporary key${NC}"
        ;;
esac