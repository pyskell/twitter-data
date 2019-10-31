from twarc import Twarc
from neo4j import GraphDatabase
from secrets import *

t = Twarc(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

# Reminder: run the docker container for this
uri = "bolt://localhost:8687"
driver = GraphDatabase.driver(uri, auth=(neo4j_user, neo4j_pass))

target_username = 'pyskell'

followers = t.follower_ids(target_username)
follower_usernames = t.user_lookup(followers)

following = t.friend_ids(target_username)
following_usernames = t.user_lookup(following)

with driver.session() as session:
  statement = '''
  MATCH (a: User {screen_name: {screen_name_a}})
  MATCH (b: User {screen_name: {screen_name_b}})
  MERGE (a)-[r:FOLLOWS]->(b)
  '''

  for fu in follower_usernames:
    tx = session.begin_transaction()
    session.run(statement, screen_name_a=fu['screen_name'], screen_name_b=target_username)
    tx.commit()

  for fu in following_usernames:
    tx = session.begin_transaction()
    session.run(statement, screen_name_a=target_username, screen_name_b=fu['screen_name'])
    tx.commit()

# with open('./output/my_followers_usernames.txt', 'w') as output:
#   for fu in follower_usernames:
#     output.write(fu['screen_name'])
#     output.write('\n')

# with open('./output/my_following_usernames.txt', 'w') as output:
#   for fu in following_usernames:
#     output.write(fu['screen_name'])
#     output.write('\n')