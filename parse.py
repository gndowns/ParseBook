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

      if not threads[people]:
        threads[people] = Thread(people)
      thread = threads[people]

    elif tag == '<div class="message">':
      message_end = messages_html.find('<div class="message">', start)
      new_message = get_message(messages_html, start, message_end)
      # facebook gives the messages in reverse chrono order
      thread.prepend_message(new_message)

    next_message = messages_html.find('<div class="message">', start)
    next_thread = messages_html.find('<div class="thread">', start)

    tag = '<div class="message">' if next_message < next_thread else '<div class="thread">'
    start = messages_html.find(tag, start)

def get_message(string, start, end):
  message_html = string[start:end].strip().strip("\n")

  index = 0
  tag = '<span class="user">'

  sender_tag = message_html.find(tag, 0) + len(tag)
  index = message_html.find('</span>', sender_tag)
  sender = message_html[sender_tag:index]

  tag = '<span class="meta">'
  time_tag = message_html.find(tag, index) + len(tag)
  index = message_html.find('</span>', time_tag)
  created_at = message_html[time_tag:index]

  tag='<p>'
  p_tag = message_html.find(tag, index) + len(tag)
  p_tag_close = message_html.find('</p>', p_tag)
  content = message_html[p_tag:p_tag_close]

  return Message(sender, created_at, content)

def get_people(string, start, end):
  people = string[start:end].strip().strip("\n").split(', ')
  people = [person.strip('&#064;facebook.com') for person in people]
  return frozenset(people)

parse(sys.argv[1])
