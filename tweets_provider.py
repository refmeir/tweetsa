from twitter.tweets_streamer import TweetsStreamer

'''
tweets streamer entry point  
'''

if __name__ == '__main__':
    # Read preson keywords
    fname = 'person-keywords.conf '
    with open(fname) as f:
        content = f.read().splitlines()

    person_keyword = ",".join(content)

    tw = TweetsStreamer()
    tw.statuses.filter(track=person_keyword)
