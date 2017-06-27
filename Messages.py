class Messages:
  def __init__(self, _owner="", _threads=None):
    self.owner = _owner
    self.threads = _threads

class Thread:
  def __init__(self, people):
    self.people = people
    self.messages = None
    self.last_msg = None

  def add_message(self, sender, created_at, content):
    message = Message(sender, created_at, content, prev_msg=self.last_msg)
    self.last_msg.next_msg = message
    self.last_msg = message

class Message:
  def __init__(self, sender, created_at, content, prev_msg=None, next_msg=None):
    self.sender = sender
    self.created_at = created_at
    self.content = content
    self.prev_msg = prev_msg
    self.next_msg = next_msg
