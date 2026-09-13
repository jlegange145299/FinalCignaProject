#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create config.toml with server settings
cat > ~/.streamlit/config.toml <<EOF
[general]
email = ""

[server]
headless = true
enableCORS = false
port = \$PORT

[theme]
primaryColor = "#0066FF"
backgroundColor = "#000033"
secondaryBackgroundColor = "#000066"
textColor = "#E8F4FD"
font = "sans serif"
EOF

# Create secrets.toml from environment variables
cat > ~/.streamlit/secrets.toml <<EOF
OPENAI_API_KEY = "$OPENAI_API_KEY"
EOF
