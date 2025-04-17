import discord
import asyncio

# === Configuration ===
BOT_TOKEN = "ABC123FIXME"  # Replace with your bot's token

# === Intents & Client Setup ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

async def list_channels():
    """
    Fetch and print all text channels across all guilds. Return a flat list of channels.
    """
    channels = []
    for guild in client.guilds:
        print(f"\nServer: {guild.name}")
        for ch in guild.text_channels:
            channels.append(ch)
            print(f"[{len(channels)-1}] #{ch.name}")
    return channels

async def interactive_loop():
    # Initial channel list and no selection
    channels = await list_channels()
    selected = None

    # Prompt until a valid channel is selected
    while selected is None:
        cmd = input("\nEnter command (list, switch <idx>, help, exit) or type your message: ").strip()
        lc = cmd.lower()

        if lc == 'list':
            channels = await list_channels()
        elif lc.startswith('switch'):
            parts = cmd.split()
            if len(parts) >= 2 and parts[1].isdigit():
                idx = int(parts[1])
                if 0 <= idx < len(channels):
                    selected = channels[idx]
                    print(f"Switched to #{selected.name}")
                else:
                    print("Invalid channel index.")
            else:
                print("Usage: switch <channel_index>")
        elif lc == 'help':
            print("Commands:\n list          List all channels\n switch <idx>  Switch to channel by index\n help          Show this help\n exit          Quit the bot\nAny other text will be sent as a message once a channel is selected.")
        elif lc == 'exit':
            await client.close()
            return
        else:
            print("No channel selected. Use 'list' then 'switch <idx>' first or 'help' for commands.")

    print("\nYou can now send messages. Type 'help' for commands.")

    # Main message loop
    while True:
        cmd = input("> ").strip()
        lc = cmd.lower()

        if lc == 'exit':
            break
        elif lc == 'list':
            channels = await list_channels()
        elif lc.startswith('switch'):
            parts = cmd.split()
            if len(parts) >= 2 and parts[1].isdigit():
                idx = int(parts[1])
                if 0 <= idx < len(channels):
                    selected = channels[idx]
                    print(f"Switched to #{selected.name}")
                else:
                    print("Invalid channel index.")
            else:
                print("Usage: switch <channel_index>")
        elif lc == 'help':
            print("Commands:\n list          List all channels\n switch <idx>  Switch to channel by index\n help          Show this help\n exit          Quit the bot")
        else:
            if not cmd:
                continue
            try:
                await selected.send(cmd)
                print(f"Sent to #{selected.name}")
            except Exception as e:
                print(f"Error sending message: {e}")

    await client.close()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Start the terminal interaction
    asyncio.create_task(interactive_loop())

if __name__ == "__main__":
    print("Starting Terminal Messenger Bot...")
    asyncio.run(client.start(BOT_TOKEN))
