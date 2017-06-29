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

    start = messages_html.find(tag, start)

parse(sys.argv[1])
