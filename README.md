# PatchChecker
This is a simple Python script that will check Debian/Ubuntu systems for available packages updates and cross-reference them against known Ubuntu CVEs.
This helps automate vulnerbaility management and patch tracking for small envrionments or personal servers. 

Requirements:
Python 3
Linux (Ubuntu/Debian systems)
Python 3.x
Packages:
  requests
  Access to the apt command

To install dependencies, run: 
pip3 install -r requirements.txt

Usage:
1. Clone the repository with:
   git clone https://github.com/YOUR_USERNAME/linux-patch-checker.git
   cd linux-patch-checker

2. Run the script: 
  sudo python3 patch_checker.py
  
   
