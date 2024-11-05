#!/bin/bash

# This script is used to generate a new key, encrypt it and generate a new temporary key

RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'


if [ "$1" == "-g" ]; then 
    if [ -z "$2" ]; then
        echo -e "${RED}Please provide the key or generate it using -n${NC}"
    else
        if test -f "$2"; then
            otp=$(openssl rand -hex $2)
            echo -e "${GREEN}Generated OTP: $otp${NC}"
        else
            echo -e "${RED}Key file not found${NC}"
        fi
    fi
elif [ "$1" == "-n" ]; then
    if [ -z "$2" ]; then
        echo -e "${RED}Please provide the name of the file${NC}"
    else
        openssl rand -hex 32 | tr -d '\n' > $2.hex
        echo -e "${GREEN}Key generated and saved in $2.hex${NC}"
    fi
elif [ "$1" == "-k" ]; then
    if [ -z "$2" ]; then
        echo -e "${RED}Please provide the name of the file${NC}"
    else
        cat $2.hex
    fi
else
    echo -e "${BLUE}Possible options are:   -n : Generate a new key 64 hex characters
                        -g : Encrypt the key
                        -k : Generate a new temporary key${NC}"
fi
