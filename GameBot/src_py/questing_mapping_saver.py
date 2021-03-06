def save(mapping_object, saving_object="app.mapping.node_map"):
	"""
	generate load file
	@param mapping_object is the QuestingMakin object
	@param saving_object is the previx node_map name complete (e.g. app.mapping.node_map
	"""
	node_map = mapping_object.node_map
	code = "#this is autogenerated \n"
	
	code += "def load():"+"\n"
	code += "\t" + (saving_object + " = [None]*%d"%len(node_map))+"\n"
	
	for i in range(len(node_map)):
		nname = "node%d"%i
		code += "\t" + (nname + " = Node()")+"\n"
		code += "\t" + (nname + ".pos = "+ str(node_map[i].pos))+"\n"
		code += "\t" + (nname + ".explored = "+str(node_map[i].explored))+"\n"
	
	code += "\t" + (saving_object + " = [")+"\n"
	for i in range(len(node_map)):
		code += "\t" + ("\tnode%d,"%i)+"\n"
	code += "\t" + ("]")+"\n"
		
	for i in range(len(node_map)):
		nname = "node%d"%i
		for child in  node_map[i].childs:
			code += "\t" + (nname + ".childs.append( " + saving_object + "[%d"%node_map.index(child)+"] )")+"\n"
	code += "\t" +saving_object[:saving_object.find(".node_map")]+".current_node = "+str(mapping_object.current_node)+"\n"
	print (code)
	f = open("questing_map_saved.py","w")
	f.write(code)
	f.close()



def print_map(mapping):
	def pad(x,l=3):
		return (str(x)+(" "*l))[:l]
	node_map = mapping.node_map
	lines = [pad("0")]
	d = 1
	queue = []
	queue[0:0] = node_map[0].childs
	while len(queue)>0:
		lines[-1] += pad(node_map.index(queue[0]))
		if queue[0].childs==[]:
			#nochild
			for r in range(d):
				lines.append(pad(" "))
			del queue[0]
			d -= 1
		else:
			d += 1
			childs = queue[0].childs
			queue[0:0] = childs#insert
			del queue[len(childs)]
	for line in lines:
		print(line)
