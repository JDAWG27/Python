class Node:
	def __init__(self, ext_data):
		self.data = ext_data
		self.link = None

	def set_node_link(self, ext_node):
		self.link = ext_node

	def set_node_data(self, ext_data):
		self.data = ext_data

	def get_node_data(self):
		return self.data

	def get_node_link(self):
		return self.link


def create_linked_list():
	head_node = None
	tail_node = None
	temp_node = None

	while True:
		user_data = input("(x) to Exit, Please enter user data: ")

		if(user_data == 'x'):
			break

		temp_node = Node(user_data)

		if(head_node == None):
			head_node = temp_node 
			tail_node = temp_node
		else:
			tail_node.set_node_link(temp_node)
			tail_node = temp_node
	return head_node

def print_linked_list(node):

	if(node.get_node_data() == None):
		return
	else:
		print(node.get_node_data())

	if(node.get_node_link() == None):
		return
	else:
		temp_node = node.get_node_link()
		print_linked_list(temp_node)


linkedlist = create_linked_list()
print_linked_list(linkedlist)

