import pandas as pd
from matplotlib import pyplot
import sys
import argparse
import datetime
import numpy as np

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    parser = argparse.ArgumentParser(description='Process some attendance records')
    parser.add_argument('reports', type=str, nargs='+',
                    help='Reports in the form <name>=<file.csv>')
    parser.add_argument('--title', help="Graph Title")

    args = parser.parse_args()
    dfs = []
    sessions = []

    # For each argument, read in the CSV
    for report in args.reports:
        # Split the input by the equal sign
        session, csv_file = report.split("=")
        sessions.append(session)
        df = pd.read_csv(csv_file)
        df = df.assign(Session=lambda x: session)
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_csv("all.csv")
    # Name (Original Name),User Email,Join Time,Leave Time,Duration (Minutes)
    
    # Get list of all users in days 1-4
    def unqiue_to_session(session):
        combined = []
        for data_session in sessions:
            if data_session == session:
                continue
            combined += list(df[df['Session'] == data_session]['Name (Original Name)'].unique())
        session_users = list(df[df['Session'] == session]['Name (Original Name)'].unique())
        return len(set(session_users) - set(combined))
   
    # Print out all of the unique attendees
    for session in sessions:
        print("{} unique: {}".format(session, unqiue_to_session(session)))

    # Print out just the LHC users, not so useful generally
    #non_lhc = list(df[df['Session'] == "Day 1"]['Name (Original Name)'].unique())
    #non_lhc += list(df[df['Session'] == "Day 2"]['Name (Original Name)'].unique())
    #non_lhc += list(df[df['Session'] == "Day 3"]['Name (Original Name)'].unique())
    #non_lhc += list(df[df['Session'] == "Day 4"]['Name (Original Name)'].unique())
    #lhc_users = list(df[df['Session'] == "Day 5"]['Name (Original Name)'].unique())
    #unique_lhc_users = set(lhc_users) - set(non_lhc)
    #print(len(unique_lhc_users))

    # List of unique attendees
    print("Unique Attendees:", df['Name (Original Name)'].nunique())

    unique_df = pd.DataFrame(data=df['Name (Original Name)'].unique())
    
    # Remove duplicate names
    # Do an all to all, comparing unique name similarity
    # A similarity score of 0.7 was pick arbitrarily.
    # Only compare names before the first "("
    is_duplicate = []
    for i in range(len(unique_df.index)):
        detected_duplicate = False
        for a in range(i+1, len(unique_df.index)):
            # Compare the names
            namea = unique_df.iloc[i,0]
            nameb = unique_df.iloc[a,0]
            if similar(namea.split("(")[0], nameb.split("(")[0]) > 0.7:
                print("Names {} and {} are similar".format(namea, nameb))
                detected_duplicate = True
        is_duplicate.append(not detected_duplicate)

    print(is_duplicate)
    unique_df.loc[is_duplicate].to_csv("unique.csv")
    #unique_df.to_csv("unique.csv")


    # Convert the start times to date times, so it can be useful
    df['start_dt'] = pd.to_datetime(df['Join Time'])
    df['end_dt'] = pd.to_datetime(df['Leave Time'])
    print(df[df.start_dt.isnull()])

    # For each session, get only the join and leave time of the attendees, and every second inbetween
    # This is the first step of generating an attendee graph
    L = [pd.Series(r.Session, pd.date_range(r.start_dt, r.end_dt, freq='S')) for r in df.itertuples()]
    s = pd.concat(L)

    # Group each second, combining to a total of attendees at that particular second
    df1 = s.groupby(level=0).value_counts().unstack(fill_value=0)
    # Find the latest dates of each of the sessions, add 1 second, and set it to 0
    #print(df1)
    
    # Replace 0's with nan
    df1.replace(0, np.nan, inplace=True)

    #series = read_csv('output.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
    #series.plot()
    plot = df1.plot()
    fig = plot.get_figure()
    fig.set_size_inches(10, 7)
    fig.suptitle(args.title)
    fig.savefig('output.png', dpi=100)


if __name__ == "__main__":
    main()
