# KillSwitch
## For Frontier Fios router users
**The problem:**


My child got obsessed with the internet a while back. I needed a convenient way to turn his access on and off without logging into the router every single time. 


**My solution:** 


I poked around and figured out how the Frontier router's API worked. I used that knowledge to build this application which despite its name simply allows you to turn rules from the router's ***Firewall > Access Control*** menu on and off without having to log into the router and doing it. 

>Note: USE AT YOUR OWN RISK. I made application to run in my controlled home network, it does not imply any security. If you let someone into your home network and they know the address and port of this application they can themselves control the access control rules. Most importantly this application requires and stores your router's admin password in order in its conf.json file to be able to log in and toggle the access control rules. 
