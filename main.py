"""
Author: Jim Li
Date: 12th May 2019
Python Version: 3

This program will grab a list of Melee tournaments from the
Super Smash Bros. Wiki Website. The program will clean up
messy / invalid data that's fetched from the site, and
it will output a trend stating the number of entrants
over Melee tournaments.

Super Smash Bros. Melee is a Nintendo fighting game released in 2001.
It quickly gained a competitve scene since its release, and the scene
grew over time due to the technical, fast-paced, edge-guarding reliant
features of the game. Recently, there has been concerns where Melee's
community is declining due to the recent release and rise of Super Smash
Bros. Ultimate this year, and Melee's reliant on older technologies
(e.g. CRT screens) that are no longer produced. This program will
collect data and represent the state of Melee's competitive scene.

NOTE: This program MIGHT not work IF SSBWiki Admins decide to change
the formatting of their site, or if wiki editors mess up the tables!
"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# List of Pokemon Table URLs
url_secure="https://www.ssbwiki.com/List_of_national_tournaments#Super_Smash_Bros._Melee"

# To be on the safe side, we disguise this request as a Web Browser
# request by adding this header.
#
# The request MIGHT successfully work without this header.
myHeader = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

# Send a request, and receive the web page data from the
# SSBWiki website.
request = requests.get(url_secure, headers=myHeader)

# Extract tournament history tables from the web page.
tables = pd.read_html(request.text)
tourneyTable = tables[0]

# Filter only Melee tournaments.
tourneyTable.columns = tourneyTable.iloc[2]
tourneyTable.columns.name = ""
tourneyTable = tourneyTable[112:329]

# Remove Melee tournaments with non-numerical Entrants values,
# such as TBD, 100+, ?, and so forth.
# Convert numerical values in Entrants to integer type.
myFilter = tourneyTable["Entrants"].str.isdigit()
tourneyTable = tourneyTable[myFilter]
tourneyTable["Entrants"].astype("int64")

# Re-number the Melee tournaments to 1,2,3,4,5, ...
entrants = tourneyTable["Entrants"].astype("int64")
numOfTourneys = entrants.index.values.size
entrants.index = np.arange(1, numOfTourneys+1)
tourneyTable.index = np.arange(1, numOfTourneys+1)


# Output graph, HTML page, and stats descriptions

htmlSrc = tourneyTable.to_html()
htmlSrc = """
<html>
<head> <title> Melee Tournament Info </title> </head>
<body>
<h1> <u> List of Super Smash Bros. Melee Tournaments </u> </h1>
""" + htmlSrc

description = entrants.describe()
ax = entrants.plot() 
ax.set_title("Number of Entrants in Melee Tournaments Over Time")
ax.set_ylabel("Number of Entrants")
ax.set_xlabel("Tournament Number")

# Plot the Moving Average too! 
windowValue=int(len(entrants.index.values)/25)
ax.plot(entrants.rolling(windowValue).mean(),\
        label="Moving Average")
ax.legend(loc="best")

# Graph goes to jpeg file
# Along with stats.
imgFileName = "my_graph.jpeg"
plt.savefig(imgFileName)
htmlSrc = htmlSrc + """
<br />
<h1> <u> Stats </u> </h1>
""" 

dictStats = dict(zip(description.index, description.values))
for stat in dictStats.keys():
    value = dictStats[stat]
    htmlSrc += (stat + ": " + str(value) + "<br />")

htmlSrc += """
<br /> 
<h1> <u> Graph of Entrants over Tournaments </u> </h1>
<img src="%s" />
</body>
</html>
""" %(imgFileName,)

htmlFile = open("tourneys.html", 'w')
htmlFile.write(htmlSrc)
htmlFile.close()






