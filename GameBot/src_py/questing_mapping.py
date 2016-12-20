class Node(object):
	"""
	each node may have a siblings, in which share the same parent,
	sibling node pos (x,y) value stored is relative to the first sibling
	if pos (x,y) is (0,0) it means the node is the first sibling
	later sibling pos is calculated (x1-xm,y1-ym) with (xm,ym) is the first sibling real coordinate
	"""
	LENGTH = 0
	childs = []
	#~ parent = None
	explored = False
	ID = 0
	pos = (0,0) #relative post for data accosiation
	
	def __init__(self):
		self.childs = []
		self.ID = Node.LENGTH
		self.pos = [0,0]
		Node.LENGTH += 1

class MappingMakin(object):
	node_map = []
	current_node = 0
	
	def __init__(self):
		first_node = Node()
		self.node_map = []
		self.current_node = 0
		self.node_map.append(first_node)
		self.last_changed_curnode = 0
	
	def restart(self):
		self.current_node = 0
	
	def add_and_decide(self, node_positions, accociate_min=40):
		"""
		add or accociate nodes as a child of node_map[current_node],
		and decide which one to go 
		@param node_positions format is [[x0,y0], [x1,y1], [x2,y2], ...]
		
		@return (x,y) coordinate of node to go
		"""
		if len(node_positions)<2:
			raise Exception("wrong input, node position must be at least 2 nodes")
		
		print("current node is",self.current_node)
		
		first_bro_pos 		= node_positions[0]
		#get first_bro short by lowest y, then lowest x
		min_x = 50000
		min_y = 50000
		for node_pos in node_positions:
			if node_pos[1]<min_y:
				min_y = node_pos[1]
				min_x = node_pos[0]
				first_bro_pos = node_pos
			elif node_pos[1]==min_y and node_pos[0]<min_x:
				min_y = node_pos[1]
				min_x = node_pos[0]
				first_bro_pos = node_pos
		
		
		if self.node_map[self.current_node].childs != []:
			#current node is not in the end of mapped nodes, and has childs
			
			for node_pos in node_positions:
				#check if found new
				print("check if found new")
				relative_pos 	= (node_pos[0]-first_bro_pos[0], node_pos[1]-first_bro_pos[1])
				
				is_new = self.node_accociate(relative_pos[0], relative_pos[1], self.node_map[self.current_node].childs, accociate_min)
				if is_new:
					print("found new")
					new_node = Node()
					new_node.pos = relative_pos
					self.node_map[self.current_node].childs.append(new_node)
				else:
					print("no new found")
			priority = []
			for i in range(len(self.node_map[self.current_node].childs)):
				node = self.node_map[self.current_node].childs[i]
				use_this_node = False
				if node.explored and node.childs!=[]:
					print("explored node has childs, check if has unexplored childs")
					to_check = []
					to_check[0:0] = node.childs
					i = 0
					while i<len(to_check):
						if to_check[i].childs!=[]:
							#child has childs
							#~ to_check[-1:] = childs #appending list childs to list to_check
							to_check[len(to_check):] = to_check[i].childs
						if not to_check[i].explored:
							print("has unexplored child, using this if no other later childs refer to this")
							priority.append(node)
							break
						i += 1
						

				if not node.explored:
					print("return unexplored node First")
					node.explored = True
					self.last_changed_curnode = self.current_node
					try:
						self.current_node = self.node_map.index(node)
					except ValueError:
						print("Warning! the node is not registered. working to register it")
						self.node_map.append(node)
						self.current_node = self.node_map.index(node)
					return (first_bro_pos[0]+node.pos[0],first_bro_pos[1]+node.pos[1]) #real coordinate may variative per call, not saved.. what saved is relative coordinate
			if priority!=[]:
				print("pick most effective route")
				node = priority[-1]
				node.explored = True
				self.last_changed_curnode = self.current_node
				try:
					self.current_node = self.node_map.index(node)
				except ValueError:
					print("Warning! the node is not registered. working to register it")
					self.node_map.append(node)
					self.current_node = self.node_map.index(node)
				return (first_bro_pos[0]+node.pos[0],first_bro_pos[1]+node.pos[1]) #real coordinate may variative per call, not saved.. what saved is relative coordinate
				
			#all is explored, return last
			print("all is explored, return last")
			target = self.node_map[self.current_node].childs[-1].pos
			target = (first_bro_pos[0]+target[0], first_bro_pos[1]+target[1])
			self.last_changed_curnode = self.current_node
			try:
				self.current_node = self.node_map.index(self.node_map[self.current_node].childs[-1])
			except ValueError:
				print("Warning! the node is not registered. working to register it")
				node = self.node_map[self.current_node].childs[-1]
				self.node_map.append(node)
				self.current_node = self.node_map.index(node)
			return target
				
		else:
			#as current node has no child, all is new
			print("as current node has no child, all is new (accociation must be done in questing.py)")
			new_node = None
			for node_pos in node_positions:
				relative_pos 	= (node_pos[0]-first_bro_pos[0], node_pos[1]-first_bro_pos[1])
				new_node = Node()
				new_node.pos = relative_pos
				print("saving",node_pos)
				self.node_map[self.current_node].childs.append(new_node)
				self.node_map.append(new_node)
			print(node_positions[0])
			
			new_node.explored = True
			self.last_changed_curnode = self.current_node
			self.current_node = self.node_map.index(new_node)
			return (first_bro_pos[0]+new_node.pos[0],first_bro_pos[1]+new_node.pos[1])
	
	
	
	
	def node_accociate(self, x,y, world, accociate_min=40):
		"""
		check whether node (x,y) is new or should be accociated to existing node, in a map world
		
		@param world is the existing Node() array formated [Node0, Node1, Node2, ...] with NodeX is a Node object
		@return 
			if not accociated to any node:
				return True
			if accociated :
				return False
		"""
		for node in world:
			if abs(node.pos[0]-x)<accociate_min and abs(node.pos[1]-y)<accociate_min:
				return False
		return True

	def print_map(self):
		def pad(x,l=3):
			return (str(x)+(" "*l))[:l]
		node_map = self.node_map
		lines = [pad("0")]
		d = 1
		queue = []
		queue[0:0] = node_map[0].childs
		queue_depth = [1]*len(queue)
		while len(queue)>0:
			#~ d += 1
			lines[-1] += pad(node_map.index(queue[0]))
			if queue[0].childs==[]:
				#nochild
				p = ""
				d = queue_depth[0]
				for r in range(d):
					p += pad(" ")
				lines.append(p)
				del queue[0]
				del queue_depth[0]
			else:
				childs = queue[0].childs
				queue[0:0] = childs#insert
				queue_depth[0:0] = [queue_depth[0]+1]*len(childs)
				del queue[len(childs)]
				del queue_depth[len(childs)]
		for line in lines:
			print(line)


