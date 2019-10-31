from twarc import Twarc
from secrets import *

t = Twarc(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
followers = t.follower_ids('pyskell')
follower_usernames = t.user_lookup(followers)

following = t.friend_ids('pyskell')
following_usernames = t.user_lookup(following)

with open('./my_followers_usernames.txt', 'w') as output:
  for fu in follower_usernames:
    output.write(fu['screen_name'])
    output.write('\n')

with open('./my_following_usernames.txt', 'w') as output:
  for fu in following_usernames:
    output.write(fu['screen_name'])
    output.write('\n')