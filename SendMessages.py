import discord
import asyncio

BOT_TOKEN = "ABC123FIXME"  # Replace this with your bot token

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Fetching channels...")

    # Wait until all guild data is available
    await asyncio.sleep(1)

    channels = []
    for guild in client.guilds:
        print(f"\nServer: {guild.name}")
        for i, channel in enumerate(guild.text_channels):
            channels.append(channel)
            print(f"[{len(channels) - 1}] #{channel.name}")

    # Channel selection input
    while True:
        try:
            index = int(input("\nSelect a channel index to send messages to: "))
            if 0 <= index < len(channels):
                selected_channel = channels[index]
                print(f"Selected channel: #{selected_channel.name}")
                break
            else:
                print("Invalid index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Message loop
    print("Type your messages below (type 'exit' to quit):")
    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            break
        if msg.strip() == "":
            continue

        try:
            await selected_channel.send(msg)
            print(f"Sent to #{selected_channel.name}")
        except Exception as e:
            print(f"Error sending message: {e}")

    await client.close()

# Run the client
if __name__ == "__main__":
    asyncio.run(client.start(BOT_TOKEN))