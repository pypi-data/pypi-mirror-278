import getopt
import socket
import sys


def process_cpuinfo():

    device_name = "0000000000000000"

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'm:')

    except getopt.GetoptError as err:
        # Print help information and exit:
        print(str(err))    # This will print something like "option -a not recognized"
        return device_name

    for option, argument in optlist:
        if option == "-m":
            device_name = argument
                              
    return device_name


def get_serial_number():

    # Extract serial from cpuinfo file
    cpu_serial = "0000000000000000"
    cpu_serial = process_cpuinfo()

    try:
        file = open('/proc/cpuinfo','r')

        for line in file:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        
        file.close()

    except:
        cpu_serial = "ERROR000000000"
 
    return cpu_serial


def get_ip_address():

    try:
        # Get the local hostname
        hostname = socket.gethostname()
        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)
    except socket.error:
        # If an error occurs, return a default IP address
        ip_address = "0.0.0.0"
            
    return ip_address