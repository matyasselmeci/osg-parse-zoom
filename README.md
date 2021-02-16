OSG AHM 2020 Data
=================


This repo contains all of the AHM attendee data as well as the script to parse
and generate graphs, `parse.py`.  The parsing has a useful help option
(`--help`) to describe the arguments.  But the command to generate all days of
the processing is:

    $ python parse.py "Day 1=participants_day1.csv" "Day 2=participants_day2.csv" "Day 3=participants_day3.csv" "Day  4=participants_day4.csv" "Day 5=participants_day5.csv"

When exporting from Zoom, do **NOT** check the "Export with meeting data".

Data
----

Included in this repo is all the data from the AHM.  The generic `participants_dayX.csv` is the daytime participants of the AHM. The `participants_dayX_*.csv` files are the attendees of the breakout sessions by name.

`all.csv` is all attendees, during the entire AHM.  They are not uniqued, and are roughly all of the `dayX.csv` concatonated together.  `output.csv` is largely a debugging output and is too large to be useful for human readable.

Running the processing
----------------------

A `requirements.txt` is provided to install the dependencies needed to run processing.  To prep the environment to run the processing, run:

    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
