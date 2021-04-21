# Options-Probability
In order to run these programs, you need:
1. Python
2. IDE (optional but suggested, I use VS code)
3. Modules numpy, pandas, matplotlib, mplcursors, and yfinance are needed to run the code

options_prob.py
options_prob.py reads a csv file and makes graph plotting the option implied distribution 
  of the markets expectations of the option price at a given expiration.

Steps:
1. Download TOS option chain csv file to folder containing the program
2. Run the program
3. Copy csv file path and paste it to command line saying "Enter csv file: "


changes_in_sd.py 
changes_in_sd.py uses a yahoo finance API to make a graph plotting the daily price changes as standard deviations
  to help display how well a security follows the normal distribution. This helps a trader stay vigilant for large price swings and 
  manage risk for taking tail-end risk in options.
  
Steps:
1. Run the program
2. Type the ticker of the security in the command line saying "Enter ticker: "
