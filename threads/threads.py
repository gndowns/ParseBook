class Threads:
  def __init__(self, _owner="", _threads=None):
    self.owner = _owner
    # dictionary with keys as frozensets of fb id's
    self.threads = _threads if _threads else {}
    self.people = {}

  def __setitem__(self, people, thread):
    self.threads[people] = thread

  def __getitem__(self, people):
    return self.threads.get(people)

class Thread:
  def __init__(self, people):
    self.people = people
    # this is a pointer to linked list of 
    # messages, the first being empty
    # use self.messages to access first non-empty message
    self.message_list = Message()
    self.last_msg = self.message_list

  def __getattr__(self, key):
    if key == "messages":
      if self.message_list.next_msg:
        return self.message_list.next_msg
      else:
        return self.message_list
    else:
      return -1
    
  def add_message(self, message):
    message.prev_msg = self.last_msg
    self.last_msg.next_msg = message
    self.last_msg = message

class Message:
  def __init__(self, sender=None, created_at=None, content=None, prev_msg=None, next_msg=None):
    self.sender = sender
    self.created_at = created_at
    self.content = content
    self.prev_msg = prev_msg
    self.next_msg = next_msg
