from QRGenerator import QRGenerator


def contactNoLabel():
    qr.clearText()
    # get the 'contact' values from json
    qr.createPNG('contact', 300, 'contact_300')

def defaultSize():
    # set the size = 0 and let segno auto handle the output size
    # empty the text overlay as it's prolly too tiny anyway
    qr.clearText()
    qr.createPNG('contact', 0, 'contact_autoSize')
    qr.createPNG('url', 0, 'url_autoSize')
    qr.createPNG('wifi', 0, 'wifi_autoSize')

def contactLabeled():
    # display the actual info on the head and foot
    qr.setHeadTextPos((40, 5), f"{qr.contact['firstName']} {qr.contact['lastName']}")
    qr.setFootTextPos((80, 317), f"Tel: {qr.contact['phone']}")
    # add image padding to allow for text
    qr.qrBorder = 10

    # get the 'contact' values from json
    qr.createPNG('contact', 350, 'contact_labeled_350')

def contactNoAddress():
    # privacy? address also adds complexity and a bigger image required
    qr.contact['address'] = ''
    qr.createPNG('contact', 300, 'contact_noaddress_300')

def wifiNoLabel():
    qr.clearText()
    # get the 'wifi' values from json
    qr.createPNG('wifi', 200, 'wifiNoLabel_200')

def wifiLabeled():
    # display the actual info on the head and foot
    qr.setHeadTextPos((25, 3), f"SSID: {qr.contact['wifiSSID']}")
    qr.setFootTextPos((25, 268), f"PASS: {qr.contact['wifiPass']}")
    # get the 'wifi' values from json
    qr.createPNG('wifi', 300, 'wifi_labeled_300')

def urlLabeled():
    # hardcode the labels or use contact.json values
    qr.setHeadTextPos((45, 8), 'INSTAGRAM')
    qr.setFootTextPos((67, 318), '/caroline_bonenfant_art')
    
    # get the 'url' value from json
    qr.createPNG('url', 350, 'url_labeled_350')

def freeText():
    qr.clearText()
    qr.qrBorder = 10
    qr.setHeadTextPos((70, 1), "War & Peace")

    # set the text directly into the qr.freetext property \r\n for a new line 
    qr.freeText = 'What can be stored in a QR Code?\r\nUp to 7089 digits or 4296 characters, including punctuation marks and special characters, can be entered in one Code.\r\nIn addition to numbers and characters, words and phrases (e.g. Internet addresses) can be encoded as well. As more data is added to the QR Code, the Code size increases and the Code structure becomes more complex'

    qr.createPNG('freeText', 250, 'freeTxt_250')

def coloredQR():
    qr.clearText()
    qr.qrBorder = 3
    # populate the qr.Colors property directly before creating the image
    # contrast is critical and 2-3 colors is usually enough
    qr.qrColors = {
        #'light': '#93b5c6', #'white', #'#93b5c6', 
        'dark': '#7209b7',#'#6a4c93', '#d81159', '#1d3557', '#d81159', #' #'#0a2472', #d7816a', 
        'finder_dark': '#1d3557', # '#ff595e',#'#d62828', #, #
        'quiet_zone': 'white' # 'skyblue' ,
        #'timing_dark': '#6a4c93', #'d62828'  
    }
    qr.createPNG('contact', 250, 'contact_color_325')
    # to reset the colors at any ytime
    qr.qrColors = {}



def examples():
    # Tip: set all font and sizes globally and just change as needed
    qr.setFontSizeColor('./fonts/Roboto/Roboto-Black.ttf', 22, '#000000')
    # image preview: crashes if too many files are created
    qr.showImageInTerminal = True

    contactNoLabel()
    contactLabeled()
    # defaultSize()
    # urlLabeled()
    # wifiNoLabel()
    # wifiLabeled()
    # freeText()
    # coloredQR()


# go!
qr = QRGenerator()
examples()

