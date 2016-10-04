# Written by Jonathan Saewitz, released October 4th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

import csv, plotly.plotly as plotly, plotly.graph_objs as go
from collections import Counter

plus_minuses = []
best_plus_minuses = []
for season in range(1978, 2017): #loop from 1978 -> 2016 (years with data available)
	c = Counter() #initialize a new counter
	with open('seasons/nfl ' + str(season) + '.csv') as f:
		reader=csv.reader(f)
		reader.next() #skip the header row
		for row in reader: #loop through the games
			week = int(row[1])
			if week<=3: #only loop if it's the 1st, 2nd, or 3rd week
				home_team = row[3]
				visiting_team = row[6]
				home_team_score = int(row[4])
				visiting_team_score = int(row[5])
				c[home_team] += int(home_team_score - visiting_team_score)
				c[visiting_team] += int(visiting_team_score - home_team_score)
			else:
				break

	for team, plus_minus in c.iteritems(): #loop through the teams and plus minuses
		plus_minuses.append({'season': season, 'team': team, '+/-': plus_minus})

	highest_plus_minus = c.values()[0] #initialize the highest plus/minus to the first team
	highest_plus_minus_team = c.keys()[0]

	for team, plus_minus in c.iteritems(): #loop through the teams
		if plus_minus > highest_plus_minus: #update the highest plus/minus if the current team has a higher plus/minus
			highest_plus_minus = plus_minus
			highest_plus_minus_team = team

	best_plus_minuses.append({'season': season, 'team': highest_plus_minus_team, '+/-': highest_plus_minus})


#write the data to a csv:
w=csv.writer(open('team_plus_minuses.csv', 'w'))
w.writerow(["Season", "Team", "+/-"])
for team in plus_minuses:
	w.writerow([team['season'], team['team'], team['+/-']])

#statistics:
print "Logged +/- data for %s teams" % len(plus_minuses)

total=0
for best_plus_minus in best_plus_minuses:
	total+=best_plus_minus['+/-']

print "Average Best Plus/Minus:", float(total)/len(best_plus_minuses)

#create the graph:
trace=go.Scatter(
	x=[best_plus_minus['season'] for best_plus_minus in best_plus_minuses],
	y=[best_plus_minus['+/-'] for best_plus_minus in best_plus_minuses],
	text=[best_plus_minus['team'] for best_plus_minus in best_plus_minuses],
)

layout=go.Layout(
	title="Best Plus/Minus In NFL Through Week 3 By Year",
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