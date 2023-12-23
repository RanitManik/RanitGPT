import os

import discord
import openai

token = os.environ['SECRET_KEY']
openai.api_key = os.getenv("OPENAI_API_KEY")


class MyClient(discord.Client):

  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    print(f'Message from {message.author}: {message.content}')
    if self.user != message.author and self.user in message.mentions:
      response = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{
              "role": "system",
              "content": "You are a helpful assistant."
          }, {
              "role": "user",
              "content": message.content
          }],
          temperature=1,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0)
      channel = message.channel
      messageToSend = response.choices[0].message.content
      await channel.send(messageToSend)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
