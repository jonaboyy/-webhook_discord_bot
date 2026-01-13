import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# ─── CONFIG ─────────────────────────────────────────────────────────────

load_dotenv("/.env") 
bot_token = os.getenv("BOT_TOKEN")
webhook_1 = os.getenv("webhook_1")
webhook_2 = os.getenv("webhook_2")
webhook_3 = os.getenv("webhook_3")
webhook_4 = os.getenv("webhook_4")
destination_webhooks = [webhook_1, webhook_2, webhook_3, webhook_4]

TARGET_CHANNEL_ID = os.getenv("target_id")
OWNER_ID = os.getenv("Owner_id")

def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == OWNER_ID
    return app_commands.check(predicate)

# ─── LOAD USER MAP ──────────────────────────────────────────────────────
def append_user_map(email, user_id):
    with open("user_map.env", "a") as f:
        f.write(f"{email.lower()}={user_id}\n")
    user_map[email.lower()] = str(user_id)  # Update in-memory mapping too
    print(f"✅ Added {email.lower()}={user_id} to user_map.env")
def remove_user_map(email, file_path="user_map.env"):
    email = email.lower()
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        with open(file_path, "w") as f:
            for line in lines:
                if not line.strip().lower().startswith(email + "="):
                    f.write(line)
        print(f"✅ Removed mapping for {email} from {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error removing mapping: {e}")
        return False

def load_user_map(file_path):
    user_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if '=' in line:
                    parts = line.strip().split('=', 1)  # Only split at the first '='
                    if len(parts) == 2:
                        email, user_id = parts
                        user_map[email.lower()] = user_id
    except FileNotFoundError:
        print("❌ user_map.env file not found.")
    return user_map


user_map = load_user_map("user_map.env")

# ─── DISCORD SETUP ──────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ─── EVENTS ─────────────────────────────────────────────────────────────
 


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


@bot.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    channel_name = message.channel.name if hasattr(message.channel, "name") else "DM"
    print(f"\n Message received in #{channel_name}")

    print(f"- Webhook ID: {message.webhook_id}")
    print(f"- Embeds: {message.embeds}")

    if message.webhook_id and message.embeds:
        print("✅ Webhook embed message detected — forwarding")

        mention = ""
        email_found = None

        # Extract email from embed
        for embed in message.embeds:
            for field in embed.fields:
                if field.name.lower() == "email":
                    email_found = field.value.strip().lower()
                    user_id = user_map.get(email_found)
                    if user_id:
                        mention = f"<@{user_id}>"
                        print(f" Found user for email {email_found}: {mention}")
                    else:
                        print(f"⚠️ No user ID mapped for email: {email_found}")
                    break

        # Message content
        content = f"CHECKOUT! {mention}".strip()

        # Extra note on first webhook
        extra_note = "Unfortunately, I lost my account as you all can see in the announcement. Please join the new server https://discord.gg/V5yaJGfmD3"

        for idx, webhook_url in enumerate(destination_webhooks):
            if idx == 0:
                await post_to_webhook(webhook_url, message.embeds, content, extra_note)
            else:
                await post_to_webhook(webhook_url, message.embeds, content)

# ─── FUNCTION TO POST TO WEBHOOK ────────────────────────────────────────

async def post_to_webhook(webhook_url, embeds, content, extra_field=None):
    filtered_embeds = []

    for embed in embeds:
        new_embed = discord.Embed(
            title=embed.title,
            description=embed.description,
            url=embed.url,
            color=embed.color or discord.Color.default()
        )

        if embed.author:
            new_embed.set_author(
                name=embed.author.name,
                icon_url=getattr(embed.author, "icon_url", "")
            )

        allowed_fields = ["Original Price", "Retail Price", "Quantity"]
        count = 0
        for field in embed.fields:
            if field.name in allowed_fields or count < 2:
                new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
                count += 1

        if embed.thumbnail:
            new_embed.set_thumbnail(url=embed.thumbnail.url)
        if embed.image:
            new_embed.set_image(url=embed.image.url)
        if embed.footer:
            new_embed.set_footer(text=embed.footer.text)

        if extra_field:
            new_embed.add_field(name="ANNOUNCEMENT", value=extra_field, inline=False)

        filtered_embeds.append(new_embed)

    if not filtered_embeds:
        print("⚠️ No embeds to send.")
        return

    payload = {
        "content": content,
        "embeds": [e.to_dict() for e in filtered_embeds]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 204:
        print(f"✅ Posted to webhook: {webhook_url}")
    else:
        print(f"❌ Failed to post to webhook: {webhook_url} | Status: {response.status_code} | Response: {response.text}")

# ─── RUN ────────────────────────────────────────────────────────────────
@bot.tree.command(name="adduser", description="Map an email to a Discord user ID")
@is_owner()
@app_commands.describe(email="Email to map", user="User to mention")
async def adduser(interaction: discord.Interaction, email: str, user: discord.User):
    append_user_map(email, user.id)
    global user_map
    user_map = load_user_map("user_map.env")
    await interaction.response.send_message(f"✅ Added {email} → <@{user.id}>")

@bot.tree.command(name="removeuser", description="Remove an email mapping")
@app_commands.describe(email="The email to remove from user map")
async def removeuser(interaction: discord.Interaction, email: str):
    success = remove_user_map(email)
    if success:
        global user_map
        user_map = load_user_map("user_map.env")  # <-- Reload in memory
        await interaction.response.send_message(f"✅ Removed `{email}` from user map.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Failed to remove `{email}`.", ephemeral=True)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(" You do not have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ An error occurred.", ephemeral=True)
        raise error  # Re-raise for logging


bot.run(bot_token)
