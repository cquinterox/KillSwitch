# KillSwitch
## Python application for Frontier Fios router users
**The problem:**

My child got obsessed with the internet a while back. I needed a convenient way to turn his access on and off without logging into the router every single time. 


**My solution:** 

I poked around and figured out how the Frontier router's API worked. I used that knowledge to build this application which despite its name simply allows you to turn rules from the router's ***Firewall > Access Control*** menu on and off without having to log into the router and doing it. 

>Note: USE AT YOUR OWN RISK. I made application to run in my controlled home network, it does not imply any security. If you let someone into your home network and they know the address and port of this application they can themselves control the access control rules. Most importantly this application requires and stores your router's admin password in order in its conf.json file to be able to log in and toggle the access control rules. 

#Recommended Setup 
1) Log into your Frontier router. 
2) Go to ***Firewall > Access Control*** and make a blocking rule.
   a) Select a device
   b) Protocol: ANY
   c) When should this rule occur? ALWAYS
##When you create rules their ruleID (required by this application) start from 0+. So your first rule will have the ruleId of 0, and the subsequent rule will have a ruleID of 1. https://drive.google.com/open?id=0B1YKXw12gaWYR3NDemhsR3QxSTA
3) Write down the ruleIDs, a descriptive name, and a description of the devices you wish to be able to toggle internet access for on the **conf.json*** file. Don't forget to also update the routerAddress and routerPassword fields.
4) Run the KillSwitch application by typing the following command on the terminal: 
python ./runserver.py
https://drive.google.com/open?id=0B1YKXw12gaWYZVFsRmxQblpHN1k
