import getpass

def help_banner():
    banner = f"""
    Hey \033[96m{getpass.getuser()},
    \033[92m  


                            Open Redirect Bug Scanner v2.0

 _____                 ______         _ _               _    
|  _  |                | ___ \       | (_)             | |   
| | | |_ __   ___ _ __ | |_/ /___  __| |_ _ __ ___  ___| |_  
| | | | '_ \ / _ \ '_ \|    // _ \/ _` | | '__/ _ \/ __| __| 
\ \_/ / |_) |  __/ | | | |\ \  __/ (_| | | | |  __/ (__| |_  
 \___/| .__/ \___|_| |_\_| \_\___|\__,_|_|_|  \___|\___|\__| 
      | |                                                    
      |_|                      Developed By Yuvaraj                             

\x1b[31;1m Open Redirect Scan : Tool for Web Pentesters and Bug Bounty Hunters

\x1b[31;1m$ \033[92mOpen Redirect\033[0m [option]

 Usage:  \033[92mOpen Redirect\033[0m [options]

Options:
  -u, --url     URL to scan                                openredirectscan -u https://target.com
  -i, --input   <filename> Read input from txt             openredirectscan -i target.txt
  -o, --output  <filename> Write output in txt file        openredirectscan-i target.txt -o output.txt
  -b, --blog    Read about Open Redirect Bug               openredirectscan -b
  -h, --help    Help Menu
    """
    print(banner)

def banner():
    banner = f"""
     \033[94m
    Hey \033[96m{getpass.getuser()},
      \033[92m


                            Open Redirect Bug Scanner v2.0

 _____                 ______         _ _               _    
|  _  |                | ___ \       | (_)             | |   
| | | |_ __   ___ _ __ | |_/ /___  __| |_ _ __ ___  ___| |_  
| | | | '_ \ / _ \ '_ \|    // _ \/ _` | | '__/ _ \/ __| __| 
\ \_/ / |_) |  __/ | | | |\ \  __/ (_| | | | |  __/ (__| |_  
 \___/| .__/ \___|_| |_\_| \_\___|\__,_|_|_|  \___|\___|\__| 
      | |                                                    
      |_|                      Developed By Yuvaraj                             

\x1b[31;1m Open Redirect scan: Tool for Web Pentesters and Bug Bounty Hunters

\033[0m"""
    print(banner)