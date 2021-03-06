# Importing the PIL library
import logging
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from datetime import datetime
import pytz
import discord
from discord.ext import commands

logger = logging.getLogger('gigachad')


class Gpay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Custom font style and font size
        self.myFont45 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 45)
        self.myFont47 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 47)
        self.myFont80 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 150)
        logger.info("Gpay initialized")

    @commands.command(
        name='gpay',
        help='Send money through Google pay to a user and show receipt',
        usage='<user> <amount>',
    )
    async def gpay(self, ctx, receiver: discord.Member, amount: float):

        if amount > 9999999:
            await ctx.send("You cannot send more than ₹9,999,999 bro")
            return
        if receiver.id == ctx.author.id:
            await ctx.send("You cannot send money to yourself bro")
            return
        if "69" in str(amount):
            await ctx.send("Mu me lele 69")
            return
        
        if amount == int(amount):
            amount = int(amount)
        else:
            amount = round(amount, 2)
        
        receiver_name = receiver.name
        receiver_nickname = receiver.display_name
        author = ctx.author
        author_name = author.name
        author_nickname = author.display_name

        await receiver.avatar_url_as(static_format='png', size=256).save("Temp/gpay_receiver.png")

        self.process_image(amount, receiver_name, receiver_nickname, author_name, author_nickname)

        await ctx.send(file=discord.File("Temp/gpay_edited.png"))


    def process_image(self, amount, receiver_name, receiver_nickname, author_name, author_nickname):
        # Open an Image
        self.img = Image.open("Modules/Gpay/gpay.png")

        # Call draw Method to add 2D graphics in an image
        self.I1 = ImageDraw.Draw(self.img)

        # Making pfp circular
        pfp = Image.open("Temp/gpay_receiver.png")
        offset = 0
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pfp.size[0] - offset, pfp.size[1] - offset), fill=255)
        background = Image.new(pfp.mode, pfp.size, ImageColor.getrgb("#1f2124"))

        # Resizing pfp
        result = Image.composite(pfp, background, mask)
        basewidth = 175
        wpercent = (basewidth / float(result.size[0]))
        hsize = int((float(result.size[1]) * float(wpercent)))
        result = result.resize((basewidth, hsize), Image.ANTIALIAS)

        # Adding pfp to image
        self.img.paste(result, (475, 60))

        # Receiver
        self.I1.text((550 - (len(str(receiver_name)) + 3) * 10, 265), f'To {receiver_name}', font=self.myFont47, fill=(255, 255, 255))

        # Cost
        self.I1.text((540 - (len("₹{:,}".format(amount))) * 35, 380), "₹{:,}".format(amount), font=self.myFont80, fill=(255, 255, 255))

        # Date time "March 20, 2022 at 7:33 PM"
        self.I1.text((457, 606), datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%B %d, %Y at %I:%M %p"), font=self.myFont45, fill=(255, 255, 255))

        # To
        self.I1.text((171, 1210), receiver_name, font=self.myFont47, fill=(255, 255, 255))

        # ToUPI
        self.I1.text((98, 1275), f"{receiver_nickname.replace(' ', '')}@gigachad", font=self.myFont47, fill=(255, 255, 255))

        # From
        self.I1.text((222, 1375), author_name, font=self.myFont47, fill=(255, 255, 255))

        # FromUPI
        self.I1.text((98, 1440), f"{author_nickname.replace(' ', '')}@gigachad", font=self.myFont47, fill=(255, 255, 255))

        # Save the edited image
        self.img.save("Temp/gpay_edited.png")
