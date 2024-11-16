import os
import re
import shutil
import segno
from PIL import Image, ImageFont, ImageDraw 
import json

class QRGenerator:
    font = 'fonts/Roboto/Roboto-Black.ttf'

    def __init__(self):
        
        self.imageSize = (200, 200)
        self.qrBorder = 10
        self.qrScale = 10
        self.qrColors = {}
        self.head = {'size': 14, 'font': self.font, 'color': '#000000', 'posXY': (0,0), 'text': ''}
        self.foot = {'size': 14, 'font': self.font, 'color': '#000000', 'posXY': (0,20), 'text': ''}
        self.dstFolder = './qrOutput'
        self.contact = {}
        self.contactVcf = ''
        self.wifiVcf = ''
        self.freeText = ''
        self.showImageInTerminal = False
        # populate the contact properties from json
        self.loadContactJSON('./contact.json')
        self.setDestinationFolder('./qrOutput')

    def loadContactJSON(self, srcFile):
        try:
            f = open(srcFile, "r")
            self.contact = json.load(f)
            f.close()
        except:
            print(f"Invalid json file: {srcFile}")
        
    def setDestinationFolder(self, path):
        # creates a sub-folder inside dstFolder from user_name for all the png and vcf files
        subFolder = self.contact['firstName'] + '_' + self.contact['lastName']
        subFolder = re.sub(r'\W+', '', subFolder.lower().replace(" ", "_"))
        self.dstFolder = f'{path}/{subFolder}'

        if not os.path.exists(self.dstFolder):
            os.makedirs(self.dstFolder)
      
    def fileExistsOrDie(self, filePath):
        try:
            f = open(filePath, "r")
            f.close()
        except:
            print(f"Error: fileExistsOrDie 404 {filePath}")
            os._exit(0)

    def createContactVcf(self):
        lines = []
        lines.append(f"BEGIN:VCARD")
        lines.append(f"VERSION:4.0")
        lines.append(f"N:{self.contact['lastName']};{self.contact['firstName']};{self.contact['middleName']};;")
        lines.append(f"FN:{self.contact['firstName']} {self.contact['lastName']}")
        lines.append(f"ORG:{self.contact['organisation']}")
        lines.append(f"TEL;TYPE=cell:{self.contact['phone']}")
        lines.append(f"EMAIL;TYPE=work:{self.contact['email']}")
        lines.append(f"URL:{self.contact['url']}")
        lines.append(f"ADR;TYPE=work:;;{self.contact['address']}")
        lines.append(f"PHOTO;MEDIATYPE=image/png:{self.contact['photo']}")
        lines.append(f"LOGO;MEDIATYPE=image/png:{self.contact['photo']}")
        lines.append(f"END:VCARD")

        self.contactVcf = "\r\n".join(lines)
        self.saveVcfFile(self.contactVcf, 'contact.vcf')

    def createWifiVcf(self):
        self.wifiVcf = f"WIFI:S:{self.contact['wifiSSID']};T:WPA;P:{self.contact['wifiPass']};;"
        self.saveVcfFile(self.wifiVcf, 'wifi.vcf')

    def saveVcfFile(self, content, fileName):
        try:
            f = open(f"{self.dstFolder}/{fileName}", "w")
            f.write(content)
            f.close()
        except:
            print(f'Error saveVcfFile {fileName}')

    # using segno to create image from vcf format or plain text
    def createPNG(self, type, size, fileName):
        
        self.imageSize = (size, size)

        if type == 'contact':
            self.createContactVcf()
            qr = segno.make(self.contactVcf)
            self.qrSavePng(qr, fileName)

        elif type == 'wifi':
            self.createWifiVcf()
            qr = segno.make(self.wifiVcf)
            self.qrSavePng(qr, fileName)

        elif type == 'url':
            qr = segno.make(self.contact['url'])
            self.qrSavePng(qr, fileName)

        elif type == 'freeText':
            qr = segno.make(self.freeText)
            self.qrSavePng(qr, fileName)

        else:
            print(f"Error createPNG type not found: {type}")

    def qrSavePng(self, qr, fileName):
        fileName = f'{fileName}.png'
        dstFile = f"{self.dstFolder}/{fileName}"
        # if imageSize = 0 remove the scale property and let segno resize
        options = {} if self.imageSize[0] == 0 else {'scale': self.qrScale}

        qr.save(
            dstFile,
            border = self.qrBorder,
            **options,
            **self.qrColors
        )

        if self.imageSize[0] >0:
            self.resizePNG(dstFile)

        self.addLabel(dstFile)
        
        if self.showImageInTerminal:
            image = Image.open(dstFile)
            image.show()
        
    def resizePNG(self, srcFile):
        self.fileExistsOrDie(srcFile)
        image = Image.open(srcFile)
        image = image.resize(self.imageSize)
        image.save(srcFile)
        
    def addLabel(self, fileName):
        imageFile = f"{fileName}"
        self.fileExistsOrDie(imageFile)

        with Image.open(imageFile).convert("RGBA") as base:
            # make a blank image for the text, initialized to transparent text color
            txtLayer = Image.new("RGBA", base.size, (255, 255, 255, 0))

            headFont = ImageFont.truetype(self.head['font'], self.head['size'])
            footFont = ImageFont.truetype(self.foot['font'], self.foot['size'])

            # get a drawing context
            d = ImageDraw.Draw(txtLayer)
            # add the text
            d.text(self.head['posXY'], self.head['text'], font=headFont, fill=(self.head['color']))
            d.text(self.foot['posXY'], self.foot['text'], font=footFont, fill=(self.foot['color']))

            out = Image.alpha_composite(base, txtLayer)
            out.save(imageFile)

    def clearText(self):
        self.head['text'] = ''
        self.foot['text'] = ''

    def setFontSizeColor(self, font, size, color):
        self.head['font'] = font
        self.head['size'] = size
        self.head['color'] = color
        self.foot['font'] = font
        self.foot['size'] = size
        self.foot['color'] = color

    def setHeadTextPos(self, posXY, text):
        self.head['text'] = text
        self.head['posXY'] = posXY

    def setFootTextPos(self, posXY, text):
        self.foot['text'] = text
        self.foot['posXY'] = posXY
