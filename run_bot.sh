#!/bin/bash
cd "/Users/mason/Documents/vs files/Relay"
source .venv/bin/activate
export SSL_CERT_FILE="/Users/mason/Documents/vs files/Relay/.venv/lib/python3.12/site-packages/certifi/cacert.pem"
python -m Core.Integrations.discord_bot
