# Discord Webhook Relay Bot with Email Mentions

A Discord automation bot that listens for webhook embed messages, extracts email fields, maps them to Discord user IDs, and forwards filtered embeds to multiple destination webhooks with optional user mentions.

Built for real-time checkout alerts, reselling groups, and automated Discord notifications.

---

## Overview

This bot monitors a specific Discord channel for webhook messages containing embeds. When an embed includes an email field, the bot attempts to match that email to a Discord user ID and automatically mentions the user when forwarding the message to other Discord servers via webhooks.

The bot is designed to be lightweight, secure, and easily extendable.

---

## Features

- Monitors webhook messages in a target Discord channel
- Detects and processes embed-based webhook messages
- Extracts email fields from embeds
- Maps emails to Discord user IDs
- Automatically mentions users when matched
- Forwards filtered embeds to multiple destination webhooks
- Reduces embed clutter by filtering fields
- Adds optional announcement fields
- Owner-only slash commands for managing mappings
- Secure configuration using environment variables

---

## Tech Stack

- Python
- discord.py
- Discord Webhooks
- dotenv
- requests

---

## How It Works

1. A webhook sends an embed message to a monitored Discord channel  
2. The bot detects the webhook message  
3. Embed fields are scanned for an email field  
4. The email is matched against stored email-to-user mappings  
5. A checkout alert message is generated  
6. The embed is filtered and forwarded to destination webhooks  
7. The mapped user is mentioned automatically if found  

---

## Example Output

CHECKOUT! @username

Forwarded embeds may include:
- Original Price
- Retail Price
- Quantity
- Product images
- Optional announcement message

---

## Slash Commands

### /adduser
Maps an email address to a Discord user ID.

Owner only.

Example:
/adduser email:user@example.com user:@username

---

### /removeuser
Removes an existing email-to-user mapping.

Example:
/removeuser email:user@example.com

---

## Configuration

All sensitive values are stored using environment variables.

### Required `.env` file
BOT_TOKEN=your_discord_bot_token
webhook_1=https://discord.com/api/webhooks/
...
webhook_2=https://discord.com/api/webhooks/
...
webhook_3=https://discord.com/api/webhooks/
...
webhook_4=https://discord.com/api/webhooks/
...

### User Mapping File

This file stores email-to-user ID mappings in the format:
email@example.com=123456789012345678

Do NOT commit `.env` or `user_map.env` to GitHub.

---

## Project Structure
webhook-discord-bot/
├── bot.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
└── user_map.env

---

## Running the Bot

Install dependencies:
pip install -r requirements.txt

Run the bot:
python bot.py

---

## Use Cases

- Sneaker checkout notifications
- Reselling group automation
- Inventory alerts
- Email-based Discord user mentions
- Multi-server webhook relays
- Real-time Discord automation

---

## Security Notes

- Never expose your bot token
- Never commit webhook URLs publicly
- Regenerate tokens if accidentally leaked
- Use `.gitignore` to protect sensitive files

---

## Future Improvements

- Database-backed user mappings
- Role mentions
- Embed templates
- Web dashboard for mapping management
- Logging and monitoring
- Rate-limit handling

---

## License

MIT License

---

## Why This Project Matters

This project demonstrates:
- Event-driven programming
- Discord bot development
- Secure environment configuration
- Real-world automation
- Data extraction from structured embeds
- Scalable webhook relay architecture
