import sys
from threads.threads import Threads, Thread, Message
import json, html

THREAD_TAG = '<div class="thread">'
MESSAGE_TAG = '<div class="message">'

def main(messages_path, out_path):

  with open(messages_path) as fp:
    messages_html = fp.read()

  threads = parse_html(messages_html)

  with open(out_path, "w") as fp:
    json.dump(threads, fp, indent=2)

def parse_html(msgs_html):
  threads = Threads()

  h1_open = msgs_html.find("<h1>") + len("<h1>")
  h1_close = msgs_html.find("</h1>", h1_open)
  threads.owner = html.unescape( msgs_html[h1_open:h1_close].strip() )

  next_thread = msgs_html.find(THREAD_TAG, h1_close) + len(THREAD_TAG)
  while (next_thread < len(msgs_html) ):
    thread_index = next_thread
    next_thread = msgs_html.find(THREAD_TAG, thread_index)
    next_thread = next_thread + len(THREAD_TAG) if next_thread != -1 else len(msgs_html)

    thread = get_thread_for_people(msgs_html, thread_index, threads)

    next_msg = msgs_html.find(MESSAGE_TAG, thread_index) + len(MESSAGE_TAG)
    while (next_msg < next_thread):
      msg_index = next_msg
      next_msg = get_message(msgs_html, msg_index, thread)
      next_msg = next_msg + len(MESSAGE_TAG) if next_msg != -1 else next_thread

    # --- end of thread ---
    messages_to_list(thread)

  # --- end of all threads ---
  for people in threads.threads:
    thread = threads[people]
    threads[people] = {
      'messages': thread.message_list,
      'size': len(thread.message_list)
    }

  return threads.__dict__

def messages_to_list(thread):
  message = thread.messages

  start = len(thread.message_list)
  thread.message_list.extend( [None] * thread.size )

  for i in range(start, start + thread.size):
    thread.message_list[i] = {
      'sender': message.sender,
      'created_at': message.created_at,
      'content': message.content
    }
    message = message.next_msg

  thread.size = 0
  thread.messages = Message()

def get_thread_for_people(msgs_html, start, threads):
  # TODO: multi thread threads
  end = msgs_html.find(MESSAGE_TAG, start)
  people = html.unescape( msgs_html[start:end].strip() ).split(', ')
  people = [p.strip('@facebook.com') for p in people]
  people.sort()
  people = " ".join(people)

  if not threads[people]: threads[people] = Thread()
  return threads[people]

def get_message(msgs_html, start, thread):
  next_msg = msgs_html.find(MESSAGE_TAG, start)
  msg_html = msgs_html[start:next_msg].strip().strip("\n")

  sender = get_tag(msg_html, '<span class="user">', '</span>')
  created_at = get_tag(msg_html, '<span class="meta">', '</span>')
  content = get_tag(msg_html, '<p>', '</p>')

  thread.prepend_message( Message(sender, created_at, content) )
  thread.size += 1
  return next_msg

def get_tag(string, tag_open, tag_close):
  start = string.find(tag_open) + len(tag_open)
  close = string.find(tag_close, start)
  return html.unescape( string[start:close].strip() )


if not len(sys.argv) == 3:
  print("ERROR need in and out path")
  sys.exit()

main(sys.argv[1], sys.argv[2])
