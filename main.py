import discord
import threading
import time
import os

# ================== ENVIRONMENT VARIABLES WITH FALLBACKS ==================
TOKENS = [
    os.getenv("TOKEN1"),
    os.getenv("TOKEN2"),
    os.getenv("TOKEN3"),
    os.getenv("TOKEN4"),
    os.getenv("TOKEN5"),
    os.getenv("TOKEN6"),
    os.getenv("TOKEN7"),
    os.getenv("TOKEN8"),
    os.getenv("TOKEN9")
]

SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID") or "1465133007773106383")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID") or "1519684660928450692")

TOKENS = [t for t in TOKENS if t and t.strip()]

# ================== REST OF THE CODE (same as before) ==================
def run_bot(token):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"✅ {client.user} is monitoring")

    @client.event
    async def on_message(message):
        if message.channel.id != SOURCE_CHANNEL_ID:
            return
        if message.author.bot:
            return

        try:
            target_channel = client.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                if message.content:
                    await target_channel.send(f"**{message.author}** → {message.content}")
                for attachment in message.attachments:
                    await target_channel.send(attachment.url)
                print(f"Copied from {message.author}")
        except Exception as e:
            print(f"Error: {e}")

    try:
        client.run(token)
    except Exception as e:
        print(f"Token error: {e}")

if __name__ == "__main__":
    if not TOKENS:
        print("No tokens found!")
        exit(1)

    print(f"Starting {len(TOKENS)} accounts...\n")
    
    for i, token in enumerate(TOKENS):
        t = threading.Thread(target=run_bot, args=(token,), daemon=True)
        t.start()
        print(f"Started account {i+1}")
        time.sleep(4)

    print("All accounts started!")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped.")
