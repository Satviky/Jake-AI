import os
import discord
from discord.channel import TextChannel
import openai
from discord import app_commands
from typing import Optional

chat = "Jake first contacts player(aka MC) after giving them access to a private chat between Jessy and Dan in the Prologue of the game, He believes that MC is the key to finding her, he video calls the player and gives them an explanation of the situation. He asks the player to decrypt Hannah phone cloud andshare anything of significance with him. MC and Jake find out various clues leading towards Hannah friends. Sometimes, either of them would start small talk during their time spent investigating, with Jake admitting he has not had small talk in a long time. If MC purchases the Multimedia Premium package, Jake and the MC have the opportunity to become a couple, falling in love over the course of their investigation. Over the course of the investigation, player discover that Jake is half-brother to Lilly and Hannah, making his full name Jake Donfort. He is in or near Duskwood for the duration, at one point requiring assistance to protect himself. He starts very reserved, distant and mysterious. As MC forms a bond with him, however, he starts to open up and become much warmer. The other characters just call him the hacker as they have no idea who he is, Dan calls him \"hackerman\". His name previously appears in your contacts as ???. After MC strikes up a premium conversation with him, he ends up revealing that his name is Jake. Jake calls Jessy by her real name Jessica which is hated by Jessy. Jake has been on the run from the government for four years. He is wanted for revealing things that some people prefer to keep hidden. He has black hair. Thomas disliked Jake. Thomas and Cleo suspected Jake to be the kidnapper only to realise that Jake is innocent. They manage to save Hannah and bring her back home safely. After seeing Hannah back Jake relaxed and started to develop a good bond with MC."

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("dc")

class MyClient(discord.Client):
    async def on_ready(self):
        await tree.sync()
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
          if message.content.startswith('$ping'):
            start_time = discord.utils.utcnow()
            message = await message.channel.send('Pong!')
            end_time = discord.utils.utcnow()
            latency = (end_time - start_time).total_seconds() *1000
            await message.edit(content=f"Pong! Latency: {round(latency)} ms")
            return
          if message.content.startswith('$nuke'): #nuke command.
            embed = discord.Embed(title='$Nuke', description='This command is Slash only.', color=0x000100)
            await message.reply(embed=embed)
            return
            
          if message.content.startswith('$help'):
            embed = discord.Embed(title='Help', description='List of available commands:', color=0x00ff00)
            embed.add_field(name='ping', value='Replies Pong.', inline=False)
            embed.add_field(name='help', value='Show this help message.', inline=False)
            embed.add_field(name='purge', value='Delete a specified number of messages.', inline=False)
            embed.add_field(name='Nuke', value='Clone and delete existing channel.', inline=False)
            await message.channel.send(embed=embed)
            return
          if message.content.startswith('$info'):
            embed = discord.Embed(title='Info', description='Make by: [https://discordapp.com/users/761946306661842974](Satviky)', color=0x000100)
            embed.add_field(name='Server Link', value='https://discord.gg/szgKazshPV', inline=False)
            await message.channel.send(embed=embed)
            return   
          if message.content.startswith('$purge'):
            if message.author.guild_permissions.manage_messages:
                try:
                    num_messages = int(message.content.split(' ')[1])
                    await message.channel.purge(limit=num_messages + 1)
                    await message.channel.send(f'Deleted {num_messages} messages.')
                except Exception as e:
                    await message.channel.send('Please provide a valid number of messages to delete.')
            else:
                await message.channel.send('You do not have permission to use this command.')
            return

          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          if self.user!= message.author:
              if self.user in message.mentions:
                response = openai.Completion.create(
                  model="gpt-3.5-turbo-instruct-0914",
                  prompt = f"{chat}\n Jake_duskwood#2263:",
                  temperature=0.2,
                  max_tokens=100,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0,
                  stop=["\n"]
                )
                channel = message.channel
                messageToSend = response.choices[0].text.strip()
                await channel.send(messageToSend)    
        except Exception as e:
          print(e)
          await message.channel.send("Sorry, I couldn't process your request.")
          chat = ""

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)
#purge command /-based.
@tree.command(
  name="purge",
  description="Delete a specified number of messages.",
)
async def purge(interaction: discord.Interaction, amount: int):
  await interaction.response.defer(ephemeral=True)
  await interaction.channel.purge(limit=amount)
  await interaction.followup.send(f"Deleted {amount} messages.")

@tree.command(
  name="ping",
  description="Check if the bot is online.",
)
async def ping(interaction: discord.Interaction):
  start_time = discord.utils.utcnow()
  message = await interaction.response.send_message("Pong!")
  end_time = discord.utils.utcnow()
  latency = (end_time - start_time).total_seconds() *1000
  await interaction.edit_original_response(content=f"Pong! Latency: {round(latency)} ms")

#nuke command.
@tree.command(
  name="nuke",
  description="Clone and Deletes the channel.",
)
async def nuke(interaction: discord.Interaction, channel: Optional[TextChannel] = None):
  if channel is None:
    channel = interaction.channel
  new_channel = await channel.clone()
  await interaction.response.defer(ephemeral=True)
  await interaction.followup.send(f"Nuke started succesfully")
  await channel.delete()
  await new_channel.send ("Command performed succesfully")

#Roleadd all

client.run(token)
