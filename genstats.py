#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import collections
import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.ticker

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

def millions(x, pos):
    return int(round(x / 1000000))

formatter = matplotlib.ticker.FuncFormatter(millions)

def _s2date(s):
	if len(s) == 7:
		s = s[:7] + '0' + s[7:]
	assert len(s) == 8
	return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))

def readData(fn):
	#iprange,ipCount,dateStr,registry,status
	with open(fn) as f:
		dList = sorted([l.split() for l in f if l.split()[3] not in ['iana', 'var']], key=lambda d: _s2date(d[2]))
		allCounts = collections.defaultdict(int)
		for d in dList:
			allCounts[d[3]] += int(d[1])
		remaining = allCounts.copy()
		lastDate = None
		for d in dList:
			curDate = _s2date(d[2])
			if curDate != lastDate:
				if lastDate is not None:
					yield (lastDate, remaining.copy())
				lastDate = curDate
			if d[4] != 'rir':
				remaining[d[3]] -= int(d[1])
		yield (curDate, remaining.copy())

RIRS = ['apnic', 'ripencc', 'arin', 'lacnic', 'afrinic']

COLORS = {
	'ripencc': 'blue',
	'apnic': 'green',
	'arin': 'red',
	'afrinic': 'magenta',
	'lacnic': 'orange',
}

NAMES = {
	'ripencc': 'Europa',
	'apnic': 'Asien',
	'arin': 'USA',
	'afrinic': 'Afrika',
	'lacnic': 'S.Amerika',
}

def main():
	data = list(readData('prefixes.txt'))
	rirs = RIRS

	font = {'family' : 'normal',
			'weight' : 'bold',
			'size'   : 18}
	matplotlib.rc('font', **font)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	for rir in rirs:
		ax.plot([d[0] for d in data], [d[1][rir] for d in data], COLORS[rir], label=NAMES[rir], linewidth=3.5)

	# format the ticks
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)
	ax.yaxis.set_major_formatter(formatter)

	datemin = datetime.date(2009, 5, 24)
	datemax = datetime.date(2012, 5, 24)
	ax.set_xlim(datemin, datemax)
	ax.set_ylim(0, 350 * 1e6)

	# format the coords message box
	ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.grid(True)

	# rotates and right aligns the x labels, and moves the bottom of the
	# axes up to make room for them
	fig.autofmt_xdate()

	#plt.ylabel('Freie IPv4-Adressen (Millionen)')
	plt.title('Freie IPv4-Adressen (Millionen)')
	plt.legend(loc=1)
	plt.subplots_adjust(left=0.1, right=0.97, top=0.92, bottom=0.1)
	plt.savefig('remaining.svg')


if __name__ == '__main__':
	main()


