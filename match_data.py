from twarc import Twarc
from neo4j import GraphDatabase
from sys import argv
from secrets import *

t = Twarc(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

def get_connections(target_username):
  followers = t.follower_ids(target_username)
  follower_usernames = t.user_lookup(followers)

  following = t.friend_ids(target_username)
  following_usernames = t.user_lookup(following)

  return (follower_usernames, following_usernames)

def save_to_db(target_username):
  # Reminder: run the docker container for this
  # TODO: Make environment variable, same for secrets
  uri = "bolt://localhost:8687"
  driver = GraphDatabase.driver(uri, auth=(neo4j_user, neo4j_pass))

  follower_usernames, following_usernames = get_connections(target_username)

  with driver.session() as session:
    statement = '''
    MERGE (a: User {
      id:coalesce({user_a_props}.id,0),
      screen_name:coalesce({user_a_props}.screen_name, ""),
      friends_count: coalesce({user_a_props}.friends_count, 0),
      description: coalesce({user_a_props}.description, "")
      })
    MERGE (b: User {
      id:coalesce({user_a_props}.id,0),
      screen_name:coalesce({user_a_props}.screen_name, ""),
      friends_count: coalesce({user_a_props}.friends_count, 0),
      description: coalesce({user_a_props}.description, "")
      })
    MERGE (a)-[r:FOLLOWS]->(b)
    '''
    user = {'screen_name' : target_username}

    for fu in follower_usernames:
      tx = session.begin_transaction()
      session.run(statement, user_a_props=fu, user_b_props=user)
      tx.commit()

    for fu in following_usernames:
      tx = session.begin_transaction()
      session.run(statement, user_a_props=user, user_b_props=fu)
      tx.commit()

def save_to_txt(target_username):
  follower_usernames, following_usernames = get_connections(target_username)
  with open(f'./output/{target_username}_followers.txt', 'w') as output:
    for fu in follower_usernames:
      output.write(fu['screen_name'])
      output.write('\n')

  with open(f'./output/{target_username}_following.txt', 'w') as output:
    for fu in following_usernames:
      output.write(fu['screen_name'])
      output.write('\n')

if __name__ == "__main__":
  if len(argv) < 3:
    print(f'Usage: {argv[0]} <db or txt> <username>')

  target_username = argv[2]

  if argv[1] == 'db':
    save_to_db(target_username)
  elif argv[1] == 'txt':
    save_to_txt(target_username)
  else:
    print('Invalid command, choose "db" or "txt"')
    exit()