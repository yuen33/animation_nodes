def getNodeNameDictionary():
	nodes = []
	
	nodes.append(("Input", [
		"IntegerInputNode",
		"FloatInputNode",
		"StringInputNode",
		"ObjectInputNode",
		"TimeInfoNode",
		"ObjectInfoNode",
		"RandomNumberNode",
		"RandomStringNode",
		"CharactersNode",
		"FloatListInputNode",
		"StringListInputNode",
		"ObjectListInputNode",
		"SoundBakeNode",
		"SoundInputNode",
		"ColorInputNode" ] ))
		
	nodes.append(("Generate", [
		"mn_ReplicateObjectNode" ] ))
		
	nodes.append(("Output", [
		"TextOutputNode",
		"ObjectOutputNode",
		"AttributeOutputNode",
		"DebugOutputNode",
		"ModifierOutputNode",
		"CopyTransformsNode",
		"MaterialOutputNode" ] ))
		
	nodes.append(("Strings", [
		"CombineStringsNode",
		"ReplicateStringsNode",
		"SubstringNode",
		"StringAnalyzeNode" ] ))

	nodes.append(("Convert", [
		"mn_ToStringConversion",
		"mn_ToFloatConversion",
		"mn_ToIntegerConversion",
		"mn_CombineVector",
		"mn_SeparateVector" ] ))
	
	nodes.append(("Math", [
		"FloatMathNode",
		"VectorLengthNode" ] ))
		
	nodes.append(("List", [
		"GetListElementNode",
		"GetListLengthNode",
		"SetListElementNode",
		"SumListElementsNode",
		"CombineListsNode",
		"ShuffleListNode" ] ))
		
	nodes.append(("Script", [
		"ExpressionNode" ] ))
		
	nodes.append(("System", [
		"SubProgramNode",
		"SubProgramStartNode",
		"EnumerateObjectsStartNode",
		"EnumerateObjectsNode" ] ))
	return nodes