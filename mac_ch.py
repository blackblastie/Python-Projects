import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change")
    parser.add_argument("-m", "--macaddr", dest="new_mac", help="MAC Address to change")
    parser.add_argument("-r", '--reset', action="store_true", dest="reset", help="reset MAC to permanent MAC Address")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac and not options.reset:
         parser.error("[-] Please specify a MAC, use --help for more info")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface], text=True)
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read Mac Address")

def reset_mac(interface):
    perm_mac = subprocess.check_output(["ethtool", "-P", interface], text=True)
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", perm_mac)
    return new_mac.group(0)

#initialize arguments
options = get_arguments()

#handle reset flag
if options.reset == 1:
    options.new_mac = reset_mac(options.interface)

#intiliaze script
print("[+] Changing MAC Address for " + options.interface + " to " + options.new_mac)

#change MAC Address
change_mac(options.interface, options.new_mac)

#confirm MAC address changed
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC of " + options.interface + " changed to " + current_mac)
else:
    print("[-] MAC of " + options.interface + " did not get changed")