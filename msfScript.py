# Python program to explain os.system() method 
	
# importing os module 
import os, argparse
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-o", "--Output", help = "Set Output File")
parser.add_argument("-i", "--Input", help = "Set Input File")
parser.add_argument("-p", "--Project", help = "Set Project Name(Same as in MSF if not Input ile is given!)")
parser.add_argument("-t", "--Type", help = "Set Type of Operation: msfToOpen, msfToFerox")

# Read arguments from command line
args = parser.parse_args()

# Command to execute 
# Using Windows OS command 
def nmapBanner():
	if args.Input:
		grep = f'''egrep -v "^#|Status: Up" {args.Input} | cut -d\' \' -f2,4- | awk -F, \'{{split($1,a," "); split(a[2],b,"/"); print a[1] " " b[1]; for(i=2; i<=NF; i++) {{ split($i,c,"/"); print a[1] c[1] }}}}\' | xargs -L1 nc -v -w1 > {args.Project}_banner_grab.txt'''
		os.system(grep)
	else:
		print("Nmap Banner grab needs NMAP input File!")

def msfToOpenNmap():
        project = args.Project
        cmd = f'msfconsole -q -x " workspace {project}; db_import *.xml; services -u -o {project}_ports_msf; exit "'

        file= f'cat {project}_ports_msf | grep -v "info" | cut -d \'"\' -f4 | sort -u | xargs | tr " " "," > {project}_open_ports.txt'
# Using os.system() method 
        if args.Input:
                fileIn = f'cat {args.Input} | grep -v "info" | cut -d \'"\' -f4 | sort -u | xargs | tr " " "," > {project}_open_ports.txt'
                os.system(fileIn)
        else:   
                print("Loading Metasploit, opening Workspace, exporting open ports")
                os.system(cmd)
                print("Format the outputfile")
                os.system(file)  
                print(f"Outputfile is {project}_open_ports.txt")


def msfToFerox():    
	project = args.Project
	cmdHTTPS = f'msfconsole -q -x " workspace {project}; db_import *.xml; services -u -p 443 -o {project}_https_targets; exit "'
	cmdHTTP = f'msfconsole -q -x " workspace {project}; db_import *.xml; services -u -p 80 -o {project}_http_targets; exit "'
	if args.Input:

                if "https" in args.Input:
                        fileHTTPS = f'cat {args.Input} | grep -v "info" | cut -d \'"\' -f2 | sed \'s#^#https://#\' > {project}_https_targets.txt'
                        os.system(fileHTTPS)
                else:
                	fileHTTP = f'cat {args.Input} | grep -v "info" | cut -d \'"\' -f2 | sed \'s#^#http://#\' > {project}_http_targets.txt'
                	os.system(fileHTTP)
	else:
		fileHTTPMSF = f'cat {project}_http_targets | grep -v "info" | cut -d \'"\' -f2 | sed \'s#^#http://#\' > {project}_http_targets.txt'
		fileHTTPSMSF = f'cat {project}_https_targets | grep -v "info" | cut -d \'"\' -f2 | sed \'s#^#https://#\' > {project}_https_targets.txt'
		os.system(cmdHTTPS)
		os.system(cmdHTTP)
		os.system(fileHTTPMSF)
		os.system(fileHTTPSMSF)

def main():
	print("Starting...")
	if args.Project:
		if args.Type == "msfToOpen":
			msfToOpenNmap()
		elif args.Type == "msfToFerox":
			msfToFerox()
		elif args.Type == "nmapBanner":
			nmapBanner()
	else:
		print("Please give a Project Name")

if __name__ == "__main__":
        main()
