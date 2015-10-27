# parse-location-history.py
Parse Google Location History from Google Takeout and output KML

First download your location history from https://www.google.com/settings/takeout and then parse out the desired dates.

Usage: parse_location_history.py [-f | --file] inputJSON [-s | --start] month/day/year [-e | --end] month/day/year [-o | --output] outputKML

KMLs can then be imported as a custom map. The script is currently setup to make a new track for every day, but can easily be changed to a single track.