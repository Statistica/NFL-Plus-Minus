# Written by Jonathan Saewitz, released October 4th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

import csv, plotly.plotly as plotly, plotly.graph_objs as go
from collections import Counter

#obtain data for team plus/minuses
plus_minuses = []
with open('team_plus_minuses.csv') as f:
	reader=csv.reader(f)
	reader.next()
	for row in reader:
		plus_minuses.append({'season': row[0], 'team': row[1], '+/-': int(row[2])})

#write the eagles' plus/minuses
eagles_plus_minuses = []
w=csv.writer(open('eagles_plus_minuses.csv', 'w'))
w.writerow(["Season", "+/-"])

for team in plus_minuses:
	if team['team'] == "Eagles":
		w.writerow([team['season'], team['+/-']])
		eagles_plus_minuses.append({"season": team['season'], "+/-": team['+/-']})

#eagles' average plus/minus
total=0
for plus_minus in eagles_plus_minuses:
	total+=plus_minus['+/-']

print "Average Plus/Minus:", float(total)/len(eagles_plus_minuses)

#create the graph:
trace=go.Scatter(
	x=[plus_minus['season'] for plus_minus in eagles_plus_minuses],
	y=[plus_minus['+/-'] for plus_minus in eagles_plus_minuses]
)

layout=go.Layout(
	title="Philadelphia Eagles Plus/Minus In NFL Through Week 3 By Season",
	xaxis=dict(
		title="Season",
	),
	yaxis=dict(
		title="Plus/Minus",
	)
)

data=[trace]
fig=dict(data=data, layout=layout)
plotly.plot(fig)