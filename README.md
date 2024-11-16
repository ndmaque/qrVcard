# QRGenerator
vCard generator is flexible, loosely written and easilly abused! 
** Requires pip installs segno and PIL (Pillow)
contact/wifi/url types will use the values from the json file
contact/wifi types will also create a .vcf file that can be pasted into any online qr generator
2 labels can be added by either hard coding them and/or using and data in the json file

# Description
Creates contact/wifi/url images from the contact.json file
The image will trigger your phone to do something when scanned: link, email, contact import, wifi import
QR images are always square and the image size will depend on the amount of data, a vCard has more data pixels.
The segno class decides the smallest/optimal image size by default but you can set the output size.
You can add 2 labels, head/foot, each has its own individual font and position properties

The .vcf files can be pasted in as text to any qr generator websites and will work as expected.
You can get or set any of properties in QRgenerator.py __init__ 
TODO: The photo property for the vCard doesn't seem to work, it might be my scan app?

Edit the json and run: python3 example.py
The file gets parsed, it creates a folder based on the user name to store the .png and .vcf files.

# Simplest vCard useage: 
qr = QRGenerator()
args = type, size, filename
qr.createPNG('contact', 200, 'myContactfile') 

or...
qr.createPNG('wifi', 200, 'mywifi') 
qr.createPNG('url', 300, 'myurl_300') 
or use any free text
populate the freeText property and give it a freeText type
qr.freeText = 'upto 3k aplpanumeric or 7k numbers can go in here'
qr.createPNG('freeText', 300, 'warAndPeace') 


# Change the border size
add padding around the image to allow for any text
qr.qrBorder = 15
qr.createPNG('contact', 200, 'myfile')

# Add labels head/foot
both labels can have it's own text/font/size/color and position
arg1 posXY is a tuple, the text is any string use setHeadTexyPos()
qr.setHeadTextPos((40, 5), f"{qr.contact['firstName']} {qr.contact['lastName']}")
qr.setFootTextPos((180, 5), "some footer text")

# font size and color
set all globally 
qr.setFontSizeColor(font, size, color)

or individually 
qr.head['font'] = 'fonts/Roboto/Roboto-Black.ttf'
qr.head['size'] = 15
qr.head['color'] = '#000000'
color accepts rgb hex octets or common names 'lightblue', 'red', '#00FF00'

qr.createPNG('contact', 300, 'myfile')
use the segno auto sizing by setting the size to 0
qr.createPNG('contact', 0, 'myfileAutoSized')


# Coloring in
the squares have a purpose, it could be a timing mark or a finder or the actual data
each type can have it's own color
most types can have a dark and a light color, make sure they contrast

Types:  light, dark, data_light , data_dark, alignment_light , alignment_dark, dark_module, finder_light, finder_dark, format_light, format_dark, quiet_zone, separator, timing_light, timing_dark, version_light, version_dark

set the properties using any/all fields above
less is more, images tends to get ugly with multiple colors like in the example below

qr.qrColors = {
    'light': '#ffffff', 
    'dark': '#7209b7',
    'finder_dark': '#ff595e'
    'quiet_zone': '#00ff00' ,
    'timing_dark': '#6a4c93'
}
qr.createPNG('contact', 0 , 'myfile')
to reset the colours
qr.qrColors = {}

# Wifi
populate the labels from custom text and json data

qr.head['text'] = f'SSID: {qr.contact["wifiSSID"]}'
qr.head['posXY'] = (21, 2)
qr.foot['text'] = f'PASS: {qr.contact["wifiPassword"]}'
qr.foot['posXY'] = (20, 90)
qr.foot['size'] = 8
qr.createPNG('wifi', 0 , 'mywifi')

# Url
the 'url' type uses the json 'url' property for the link
you can have a csv of urls in the json 'abc.com, xyz.com'

hard coded labels
qr.head['text'] = 'INSTAGRAM'
qr.foot['text'] = '/myUserName'

qr.createPNG('url', 250, 'my_url_250')

# Resources

segno qr image creator 
https://segno.readthedocs.io/en/latest/make.html

vCard basic info
https://en.wikipedia.org/wiki/VCard#Properties

image manipulation
https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#using-the-image-class

ttf files 
fonts.google
