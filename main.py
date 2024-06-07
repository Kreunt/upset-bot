import discord
from PIL import Image, ImageDraw, ImageFont


class MyClient(discord.Client):
    async def generateImage(self, firstFrame, secondFrame):
        img = Image.open("in.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 10)
        draw.text((180, 20), firstFrame, font=font, fill="black")
        draw.text((450, 40), secondFrame, font=font, fill="black")
        img.save("out.png")

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if (message.author.bot):
            return
        if message.content == '😡':
            secondFrame = ""
            firstFrame = ""
            async for prevMes in message.channel.history(limit=20):
                if prevMes.author != message.author:
                    if firstFrame != "":
                        break
                    secondFrame = prevMes.content + "\n" + secondFrame
                else:
                    if prevMes.content == '😡':
                        continue
                    firstFrame = prevMes.content + "\n" + firstFrame
            await self.generateImage(firstFrame, secondFrame)
            await message.channel.send(file=discord.File('out.png'))

                    


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('TOKEN')
