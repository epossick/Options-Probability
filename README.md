About Program
Program contains 1 file called main.py. main.py contains 2 classes (ChangeSD & OptionsProb). 
ChangeSD plots the daily price fluctuations over the past year in standard deviations relative to the historical volatility on a 20-day sliding window (historical volatility of last 20 days, sliding over one day for every iteration). This can help you visualize how well a security will fit the normal distribution, and therefore our tail-risk selling strategy. Seeing price movements consistently going past 3 sd could indicate that you should either leave the security alone or go further OTM to reduce risk (you could use Chebyshev's Inequality to find probability in this case). OptionsProb uses a continuum of butterfly spreads to get a series of costs for any equadistant price range, and divides those costs by the payoff of the position, leaving us with the options implied probability. The program then plots the distribution of probabilitites to help us find a good place to take a trade. 



Important notes
For some of the securities with larger amount of strikes (ex.TSLA), you might need to increase the width of each bar in the OptionsProb chart. Sometimes their are too many strikes so some of the bars are not visible. You can find the chart in the main() function under #plot OptionsProb. I have only ever needed 0.2 or 0.5 for my width, but its still something to consider.
This also requires you to install a few modules, if you do not know how just google it.
