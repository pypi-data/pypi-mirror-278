from massiprecon import massiprecon

if __name__ == "__main__":
    # Importing argparse
    print(''' _____ ______   ________  ________   ________  ___  ________  ________  _______   ________  ________  ________      
|\\   _ \\  _   \\|\\   __  \\|\\   ____\\ |\\   ____\\|\\  \\|\\   __  \\|\\   __  \\|\\  ___ \\ |\\   ____\\|\\   __  \\|\\   ___  \\    
\\ \\  \\\\\\__\\ \\  \\ \\  \\|\\  \\ \\  \\___|_\\ \\  \\___|\\ \\  \\ \\  \\|\\  \\ \\  \\|\\  \\ \\   __/|\\ \\  \\___|\\ \\  \\|\\  \\ \\  \\\\ \\  \\   
 \\ \\  \\\\|__| \\  \\ \\   __  \\ \\_____  \\\\ \\_____  \\ \\  \\ \\   ____\\ \\   _  _\\ \\  \\_|/_\\ \\  \\    \\ \\  \\\\\\  \\ \\  \\\\ \\  \\  
  \\ \\  \\    \\ \\  \\ \\  \\ \\  \\|____|\\  \\\\|____|\\  \\ \\  \\ \\  \\___|\\ \\  \\\\  \\\\ \\  \\_|\\ \\ \\  \\____\\ \\  \\\\\\  \\ \\  \\\\ \\  \\ 
   \\ \\__\\    \\ \\__\\ \\__\\ \\__\\____\\_\\  \\ ____\\_\\  \\ \\__\\ \\__\\    \\ \\__\\\\ _\\\\ \\_______\\ \\_______\\ \\_______\\ \\__\\\\ \\__\\
    \\|__|     \\|__|\\|__|\\|__|\\_________\\\\_________\\|__|\\|__|     \\|__|\\|__|\\|_______|\\|_______|\\|_______|\\|__| \\|__|
                            \\|_________\\|_________|                                                                ''')
    import argparse

    # Define the parser function
    def parser():
        
        # Create the base argument parser
        parser = argparse.ArgumentParser(description="massiprecon args")
        parser.add_argument("-i", "--infile", required=True,  help="list of ips")
        parser.add_argument("-o", "--outfile", required=True, help="json or csv file to write to")

        
        # Return parsed arguments
        args = parser.parse_args()
        return args

    args = parser()
    f=massiprecon.FileMaker(args.infile,args.outfile)
    print(f.generate())