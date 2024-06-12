import getpass
from termcolor import colored
import pyfiglet

def banner():
    # Create a fancy banner using pyfiglet
    ascii_banner = pyfiglet.figlet_format("Open redirect tool")
    
    # Display the banner with colors
    print(colored(ascii_banner, 'red'))
    
    print("Hey", getpass.getuser())
    # Additional information
    info = """
    Description: This tool helps in finding open 
    redirect vulnerabilities in web applications
    """
    print(colored(info, 'yellow'))

if __name__ == "__main__":
    banner()
    # Your main script logic here
