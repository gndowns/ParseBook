class Threads:
  def __init__(self, _owner="", _threads=None):
    self.owner = _owner
    # dictionary with keys as frozensets of fb id's
    self.threads = _threads if _threads else {}

  def __setitem__(self, people, thread):
    self.threads[people] = thread

  def __getitem__(self, people):
    return self.threads.get(people)

class Thread:
  def __init__(self):
    # this is a pointer to linked list of 
    # messages, the last being empty
    self.messages = Message()
    self.size = 0

  def prepend_message(self, message):
    message.next_msg = self.messages
    self.messages = message

class Message:
  def __init__(self, sender=None, created_at=None, content=None, next_msg=None):
    self.sender = sender
    self.created_at = created_at
    self.content = content
    self.next_msg = next_msg
