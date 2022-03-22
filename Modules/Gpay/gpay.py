# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

import glob

class Gpay:
    def __init__(self):
        
        # Custom font style and font size
        self.myFont45 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 45)
        self.myFont47 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 47)
        self.myFont80 = ImageFont.truetype('Utils/Fonts/Helvetica.ttf', 150)
    
    def parse(self, message):
        # Open an Image
        self.img = Image.open("Modules/Gpay/gpay.png")
        
        # Call draw Method to add 2D graphics in an image
        self.I1 = ImageDraw.Draw(self.img)

        content = message.content
        params = content.split(' ')
        if len(params) < 3:
            return "'$gpay' requires 2 parameters.\nExample: '$gpay <user> <amount>'"
        if len(params) > 3:
            return "Too many parameters bro"
        if not message.mentions:
            return "You haven't mentioned anyone bro"
        if message.mentions[0].id == message.author.id:
            return "You cannot send money to yourself bro"
        if not params[2].isdigit():
            return "You have to enter a valid amount bro"
        
        receiver = message.mentions[0]
        amount = int(params[2])

        if amount > 999999:
            return "You cannot send more than ₹999999 bro"

        receiver_name = receiver.name
        receiver_nickname = receiver.display_name
        author = message.author
        author_name = author.name
        author_nickname = author.display_name
        # # Pfp
        # self.img.paste(Image.open(open("Temp/gpay_receiver.png", 'rb')), (20, 500))
        # Receiver
        self.I1.text((500-len(str(amount))*10, 265), f'To {receiver_name}', font=self.myFont47, fill =(255, 255, 255))

        #Cost
        self.I1.text((430-len(str(amount))*20, 380), "₹{:,}".format(amount), font=self.myFont80, fill =(255, 255, 255))

        # Date time "March 20, 2022 at 7:33 PM"
        self.I1.text((457, 606), datetime.now().strftime("%B %d, %Y at %I:%M %p"), font=self.myFont45, fill =(255, 255, 255))

        # To
        self.I1.text((171, 1210), receiver_name, font=self.myFont47, fill =(255, 255, 255))

        #ToUPI
        self.I1.text((98, 1275), f"{receiver_nickname.replace(' ', '')}@gigachad", font=self.myFont47, fill =(255, 255, 255))

        # From
        self.I1.text((222, 1375), author_name, font=self.myFont47, fill =(255, 255, 255))

        #FromUPI
        self.I1.text((98, 1440), f"{author_nickname.replace(' ', '')}@gigachad", font=self.myFont47, fill =(255, 255, 255))

        # Save the edited image
        self.img.save("Temp/gpay_edited.png")

