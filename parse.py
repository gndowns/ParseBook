import sys
from threads.threads import Threads, Thread, Message
import json

def parse(messages_path, out_path):
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
      if len(people.split()) > 2:
        tag = '<div class="thread">'
        start = messages_html.find(tag, start)
        continue

      if not threads[people]:
        threads[people] = Thread()
      thread = threads[people]

    elif tag == '<div class="message">':
      message_end = messages_html.find('<div class="message">', start)
      new_message = get_message(messages_html, start, message_end)
      # facebook gives the messages in reverse chrono order
      thread.prepend_message(new_message)
      thread.size += 1

    next_message = messages_html.find('<div class="message">', start)
    next_thread = messages_html.find('<div class="thread">', start)

    # end of thread logic
    if next_message == -1 or (next_thread < next_message and next_thread != -1):
      message = thread.messages
      thread.messages = [None] * thread.size
      for i in range(0, thread.size):
        thread.messages[i] = {
          'sender': message.sender,
          'created_at': message.created_at,
          'content': message.content
        }
        message = message.next_msg

    if next_thread < next_message and next_thread != -1:
      tag = '<div class="thread">'
    else:
      tag = '<div class="message">'

    # tag = '<div class="message">' if next_message < next_thread else '<div class="thread">'
    start = messages_html.find(tag, start)

  for people in threads.threads:
    threads[people] = threads[people].__dict__

  with open(out_path, "w") as fp:
    json.dump(threads.__dict__, fp, indent=2)
def get_message(string, start, end):
  message_html = string[start:end].strip().strip("\n")

  sender = get_tag(message_html, '<span class="user">', '</span>')
  created_at = get_tag(message_html, '<span class="meta">', '</span>')
  content = get_tag(message_html, '<p>', '</p>')

  return Message(sender, created_at, content)

def get_tag(string, tag_open, tag_close):
  start = string.find(tag_open) + len(tag_open)
  close = string.find(tag_close, start)
  return string[start:close].strip().strip("\n")

def get_people(string, start, end):
  people = string[start:end].strip().strip("\n").split(', ')
  people = [person.strip('&#064;facebook.com').strip("@") for person in people]
  people.sort()
  return " ".join(people)

if not len(sys.argv) == 3:
  print("ERROR need in and out path")
  sys.exit()

parse(sys.argv[1], sys.argv[2])
