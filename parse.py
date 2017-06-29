import sys
from threads.threads import Threads, Thread, Message

def parse(messages_path):
  threads = Threads()

  with open(messages_path) as fp:
    messages_html = fp.read()

  h1_tag_index = messages_html.find("<h1>", 0) + len("<h1>")
  # start increments forward as threads are read
  start = messages_html.find("</h1>", h1_tag_index)

  threads.owner = messages_html[h1_tag_index:start].strip()

  tag = '<div class="thread">'
  start = messages_html.find(tag, 0)
  while(start != -1):
    start += len(tag)

    # get thread participants
    if tag == '<div class="thread">':
      # people list ends where the first message starts
      people_end = messages_html.find('<div class="message">', start)
      people = get_people(messages_html, start, people_end)

    # skip group chats
    if len(people) > 2:
      tag = '<div class="thread">'
      start = messages_html.find(tag, start)
      continue

    start = messages_html.find(tag, start)

def get_people(string, start, end):
  people = string[start:end].strip().strip("\n").split(', ')
  people = [person.strip('&#064;facebook.com') for person in people]
  return frozenset(people)

parse(sys.argv[1])
