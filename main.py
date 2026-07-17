import discord
import threading
import time
import os

# Single variable with tokens separated by commas
TOKENS_STR = os.getenv("TOKENS", "")
TOKENS = [t.strip() for t in TOKENS_STR.split(",") if t.strip()]

SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", 1465133007773106383))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 1519684660928450692))

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
            target = client.get_channel(TARGET_CHANNEL_ID)
            if target:
                if message.content:
                    await target.send(f"**{message.author}** → {message.content}")
                for att in message.attachments:
                    await target.send(att.url)
                print(f"Copied by {client.user}")
        except:
            pass

    try:
        client.run(token)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not TOKENS:
        print("No tokens found!")
        exit(1)

    print(f"Starting {len(TOKENS)} accounts...\n")
    
    for i, token in enumerate(TOKENS):
        t = threading.Thread(target=run_bot, args=(token,), daemon=True)
        t.start()
        print(f"Started {i+1}")
        time.sleep(4)

    print("All started!")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped")
