class ParseMessages:

	def __init__():
		self.users = Users
		self.owner = None


	class Thread(ParseMessages):
		def __init__(self, thread_id):
			self.people = []
			self.messages = None
			self.last_msg = None
			self.thread_id = thread_id

		def add_person(self, users, person_id):
			if not (person = users.get_person(person_id)):
				person = Person(person_id)
				person.add_thread(self)
			self.people.append(person)

		def add_message(self, sender, created_at, content)
			if len(self.people) <= 2:
				if not self.people[0] in self.users.users and sender != self.owner:
					users.users[self.people[0]] = sender
			message = Message(sender, created_at, content, self.last_msg)
			self.last_msg.next_msg = message
			self.last_msg = message

	class Message(ParseMessages):
		def __init__(self, sender, created_at, content, prev_msg=None):
			self.sender = sender
			self.created_at = created_at
			self.content = content
			self.prev_msg = prev_msg
			self.next_msg = next_msg


	class Users(ParseMessages):
		def __init__(self):
			self.users = {}

		def get_person(self, person_id):
			if person_id in self.users:
				return self.users[person_id]
			else:
				return None


	class Person(ParseMessages):
		def __init__(self, fb_id):
			self.messages_by_group = {}
			self.threads = {}
			self.name = name
			self.fb_id = fb_id

		def add_message_by_group(self, thread, group, messages):
			if not self.messages_by_group[group]:
				self.messages_by_group[group] = [messages]
			else:
				self.messages_by_group[group].append(messages)

		def add_thread(self, thread):
			self.threads[thread.thread_id] = thread
