#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create config.toml with server settings
echo "\
[general]\n\
email = \"\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
\n\
[theme]\n\
primaryColor = \"#0066FF\"\n\
backgroundColor = \"#000033\"\n\
secondaryBackgroundColor = \"#000066\"\n\
textColor = \"#E8F4FD\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml

# Create secrets.toml from environment variables
echo "\
OPENAI_API_KEY = \"$OPENAI_API_KEY\"\n\
" > ~/.streamlit/secrets.toml
