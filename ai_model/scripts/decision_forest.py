import numpy as np
import json

# # # # # # #
# Constants #
# # # # # # #
# Precision for rounding decimals
precision = 6

# Value of a weight providing a perfect 50/50 split
ideal_weight = 0.5

# Acceptable percent difference between deltas to compare using weights instead
acceptable_margin = 5

# Variable which controls the maximum possible standard deviation or minimum change in standard deviation for a leaf node
std_dev_threshold = {'wind_speed': 1.05, 'relative_humidity': 1.05, 'temperature': 1.2}
delta_threshold = {'wind_speed': 0.075, 'relative_humidity': 0.075, 'temperature':0.09}

# # # # # #
# Classes #
# # # # # #
""" Decision Forest Class 

	Attributes
		n_labels: Number of label columns in dataset (labels are assumed to be rightmost columns)
		n_trees: Number of trees in the forest
		batch_size: Number of bootstrap aggregated rows used to build each tree
		trees: List of DecisionTree objects
		avg_std_dev: Average standard deviation for each label in a forest
	"""
class DecisionForest():
	n_trees = 128
	batch_size = 1536

	def __init__(self, rows = None, n_labels = 1, n_trees = None, batch_size = None, forecast_col = None, obj_dict = None):
		if obj_dict!=None:
			self.n_labels = obj_dict['n_labels']
			self.n_trees = obj_dict['n_trees']
			self.batch_size = obj_dict['batch_size']
			self.trees = [DecisionTree(obj_dict=x) for x in obj_dict['trees']]
			self.avg_std_dev = obj_dict['avg_std_dev']
		else:
			self.n_labels = n_labels
			self.n_trees = DecisionForest.n_trees if n_trees==None else n_trees
			self.batch_size = DecisionForest.batch_size if batch_size==None else batch_size
			self.trees = build_forest(rows, n_labels, self.n_trees, self.batch_size, forecast_col=forecast_col)
			self.avg_std_dev = [np.mean([tree.leaf_mean[label] for tree in self.trees]) for label in range(n_labels)]

	# Method to get string of results
	def results_to_str(self): 
		results = 'Decision Tree Attributes:\nLabel #: {0} Batch Size: {1} Tree Count: {2}\nAvg Std Deviation: {3}'.format(self.n_labels, self.batch_size, self.n_trees, self.avg_std_dev)
		for i in range(len(self.trees)):
			results += '\nTree #: {0}\tDepth: {1}\tMean Std Dev: {2}\n\t\tFeatures: {3}'.format(i, self.trees[i].depth, self.trees[i].leaf_mean, self.trees[i].features)
		return results

	# Method to get the mean expected value from the forest
	def get_expected(self, features):
		tree_labels = []
		# Get labels from all trees
		for tree in self.trees:
			tree_labels += [tree.find_mean(features)]

		# Average values for all labels
		expected = [np.mean([label[i] for label in tree_labels]) for i in range(self.n_labels)]

		# Only returning 0th element now to manually get 1 label
		return expected[0]

	# Function to get the dictionary of standard deviations for all trees
	def get_std_dev(self):
		ans = []
		for tree in self.trees:
			ans += list(tree.get_std_dev().items())

		return dict(ans)


""" Decision Tree Class 

	Attributes
		root: Root Node object for the tree
		depth: Maximum distance between root Node & LeafNode
		features: Array holding subset of features used by this tree
		leaf_dev: Array of standard deviations for all leaf nodes
		leaf_mean: Mean standard deviation for labels in this tree

	"""
class DecisionTree():
	# Initialization function
	# obj_dict!=None: Load tree from dictionary
	# Else: Build new decision tree
	def __init__(self, rows=None, features=None, n_labels=None, forecast_col=None, obj_dict=None):
		if obj_dict!=None:
			if obj_dict['root']['isLeaf']:
				self.root = Leaf(obj_dict=obj_dict['root'])
			else:
				self.root = Node(obj_dict=obj_dict['root'])
			self.leaf_dev = obj_dict['leaf_dev']
			self.depth = obj_dict['depth']
			self.features = obj_dict['features']
			self.leaf_mean = obj_dict['leaf_mean']
		else:
			# Initial recursive call to build the tree
			self.root, self.leaf_dev = build_tree(rows, n_labels=n_labels, forecast_col=forecast_col)

			# Assign tree attributes
			self.depth = self.root.depth
			self.features = features
			self.leaf_mean = [np.mean([leaf[i] for leaf in self.leaf_dev]) for i in range(n_labels)]

	# Function to find the expected mean label values given the full list of features
	def find_mean(self, features):
		# Get the subset of feature values used for this tree
		tree_features = [features[x] for x in self.features]

		# Start recursive function to get the most appropriate leaf node
		leaf_node = find_leaf(self.root, tree_features)

		# Return the corresponding mean values
		return leaf_node.mean

	# Recursive function to build a string depicting the tree
	def to_str(self, node=None, indent=''):
		# If node is None it is initial call - assign node to root
		if node==None:
			node = self.root

		#is this a leaf node?
		if node.isLeaf:
			# Create string with leaf attributes
			node_str = 'Leaf - Std Dev: {0} Mean: {1}'.format(str(node.std_dev), str(node.mean))

			return node_str
		else:
			# Print node attributes
			node_str = 'Node - Key: {0} Val: {1} Delta: {2}'.format(str(node.index), str(node.value), str(node.avg_delta))
			
			# Concatente the recursive branch calls
			node_str += '\n{0}L->{1}'.format(indent, self.to_str(node.left_branch, indent + '\t'))
			node_str += '\n{0}R->{1}'.format(indent, self.to_str(node.right_branch, indent + '\t'))

			# Return the final string
			return node_str

	# Recursive function to get a dictionary of standard deviations at tree depths
	def get_std_dev(self, node=None, ans=None):
		# Handle initial recursive call
		if node==None or ans==None:
			node = self.root
			ans = {}
		
		# Add the node to the dictionary
		if node.depth in ans:
			ans[node.depth] += [node.std_dev]
		else:
			ans[node.depth] = [node.std_dev]


		# If the node isn't a leaf add the child nodes
		if not node.isLeaf:
			# Add the child nodes to the dictionary & return current node std_dev
			get_std_dev(node=node.left_branch, ans=ans)
			get_std_dev(node=node.right_branch, ans=ans)

		# If the initial recursive call is finishing then return the root
		if node == self.root:
			return ans

			

""" Class used for tree branch nodes 
	
	Attributes
		index: Column index being split on (Note: relative to input features, not total features)
		value: Value used to split the dataset
		std_dev: Standard deviations of labels inputted to this node
		delta: Weighted changes in std_dev from this input to the two outputs
		avg_delta: Mean of the deltas
		weight: Fraction (0->1) of rows being sent to the left branch
		isLeaf: Boolean indicator
		depth: Maximum possible depth from this node to a leaf
		left_branch: Node or LeafNode object
		right_branch: Node or LeafNode object
	"""
class Node():
	# Initialization function
	# obj_dict != None: Load node from json object
	# Else: Create new node

	def __init__(self, i = -1, v = None, obj_dict=None):
		if obj_dict!=None:
			# Assign the primitive types
			self.index = obj_dict['index']
			self.value = obj_dict['value']
			self.std_dev = obj_dict['std_dev']
			self.delta = obj_dict['delta']
			self.avg_delta = obj_dict['avg_delta']
			self.weight = obj_dict['weight']
			self.isLeaf = obj_dict['isLeaf']
			self.depth = obj_dict['depth']

			# Assign the left & right branches accordingly
			if obj_dict['left_branch']['isLeaf']:
				self.left_branch = Leaf(obj_dict=obj_dict['left_branch'])
			else:
				self.left_branch = Node(obj_dict=obj_dict['left_branch'])
			
			if obj_dict['right_branch']['isLeaf']:
				self.right_branch = Leaf(obj_dict=obj_dict['right_branch'])
			else:
				self.right_branch = Node(obj_dict=obj_dict['right_branch'])

		else:
			# Values used to split the node
			self.index = i
			self.value = v

			# Values resulting from the split
			self.std_dev = None
			self.delta = None
			self.avg_delta = None
			self.weight = None

			# Values relevant for the tree
			self.isLeaf = False
			self.depth = None

			# Define the two branches of the node
			self.left_branch = None
			self.right_branch = None


	# Function used to split the input for this node
	def split(self, rows):
		left = []
		right = []

		for row in rows:
			if (row[self.index]>=self.value):
				right += [row]
			else:
				left += [row]

		return left, right

	# Function used to compare self with input node, returning True if deemed "better"
	def compare(self, node):

		# Otherwise compare the average change in standard deviation
		return self.avg_delta > node.avg_delta

""" Class used for tree leaf nodes 
	
	Attributes
		labels: Array of each label assigned to this leaf node
		mean: Mean values for each label
		std_dev: Standard deviations for each label
		isLeaf: Boolean indicator
		depth: Value of 0 used to begin incrementing the recursive function
	"""
class Leaf():
	# Function to initialize the LeafNode:
	# Labels != None: Creating a new leaf node
	# obj_dict != None: Parsing a node from a json object
	def __init__(self, labels=None, obj_dict=None):
		# Creation
		if labels!=None:
			# 2 dimensional list of labels: 1 - label type, 2 - label row
			self.labels = [[row[i] for row in labels] for i in range(len(labels[0]))]

			# Mean & standard deviation for labels of this node
			self.mean = [np.round(np.mean(label), precision) for label in self.labels]
			self.std_dev = [np.round(np.std(label), precision) for label in self.labels]

			# Leaf node values
			self.isLeaf = True
			self.depth = 0
		# Loading
		elif obj_dict!=None:
			self.labels = obj_dict['labels']
			self.mean = obj_dict['mean']
			self.std_dev = obj_dict['std_dev']
			self.isLeaf = obj_dict['isLeaf']
			self.depth = obj_dict['depth']

# # # # # # #
# Functions #
# # # # # # #
""" Function that creates decisin trees using a subset of the provided features & bootstrap aggregated rows 

	Inputs
			rows: Two dimensional list of data - 1st = rows, 2nd = columns
			n_labels: Number of label columns in each row
			n_trees: Number of trees in the forst
			batch_size: Size of bootstrap aggregated dataset used for each tree

	Outpus
			Array of DecisionTree objects
	"""
def build_forest(rows, n_labels, n_trees, batch_size, forecast_col): 
	# Seed the RNG & initialize the tree list
	np.random.seed()
	forest = [None for i in range(n_trees)]

	# Variable storing total number of features
	n_features = len(rows[0]) - n_labels

	# Variable storing the number of features to be used per tree
	tree_size = int(np.floor(n_features/3))
	for i in range(n_trees):
		# Get a random subset of feature indices & row indices
		cut_features = np.random.choice([x for x in range(4, n_features-7)], size=tree_size*2, replace=False)
		curr_features = [x for x in range(n_features) if x not in cut_features]
		curr_rows = np.random.randint(len(rows), size=batch_size, dtype='int')

		# Get the bootstrap aggregated row set
		curr_batch = [[rows[x][y] for y in curr_features] + rows[x][-n_labels:] for x in curr_rows]

		# Build the tree & add it to the forest
		forest[i] = DecisionTree(rows=curr_batch, features=curr_features, n_labels=n_labels, forecast_col=forecast_col)

	return forest

""" Recursive function to build out a decision tree 
	
	Inputs
		rows: Two dimensional array of numbers; first dimension is rows, second dimension is columns
		n_labels: Number of label columns in each row; defaults to 1

	Outputs
		Node or LeafNode object
		Two dimensional array - 1st = leaves, 2nd = labels
	"""
def build_tree(rows, forecast_col, n_labels = 1): 
	# Find the best node split
	node = find_best_split(rows, n_labels)
	
	# If the change is below threshold value create leaf node
	if np.mean(node.std_dev)<=std_dev_threshold[forecast_col] or np.mean(node.avg_delta)<=delta_threshold[forecast_col]:
		return Leaf(labels=[row[-n_labels:] for row in rows]), [node.std_dev]

	# Otherwise build out the left & right branches of the node
	l, r = node.split(rows)
	node.left_branch, left_leaf_dev = build_tree(l, n_labels=n_labels, forecast_col=forecast_col)
	node.right_branch, right_leaf_dev = build_tree(r, n_labels=n_labels, forecast_col=forecast_col)

	# Append the leaf standard deviations to leaf_dev
	leaf_dev = left_leaf_dev + right_leaf_dev

	# Increment the depth from the child branches & return
	node.depth = max(node.left_branch.depth, node.right_branch.depth) + 1
	return node, leaf_dev

""" Function used to determine the best column/value pair for splitting the rows 

	Inputs
		node: Two dimensional array of numbers; first dimension is rows, second dimension is columns
		n_labels: Number of label columns in each row; defaults to 1

	Returns
		Node object
	"""
def find_best_split(node, n_labels): 
	# Get the standard deviation of the current node
	std_dev = [np.std([row[-label] for row in node]) for label in range(1, n_labels+1)]

	# Initialize best node variable & values
	best_node = Node()
	best_node.delta = [0 for x in range(n_labels)]
	best_node.avg_delta = np.round(np.mean(best_node.delta), precision)
	best_node.weight = 0

	# Loop over all feature columns
	col_count = len(node[0])-n_labels
	for col in range(col_count):

		# Loop over all unique feature values
		values = np.unique([row[col] for row in node])
		for val in values:
			# Build the current potential split
			curr_node = Node(i = col, v = val)

			# Build the left & right branches by splitting input
			curr_left, curr_right = curr_node.split(node)

			# Get the weighting between left & right branches
			curr_node.weight = len(curr_left) / (len(curr_left) + len(curr_right))

			# Determine the weighted change in standard deviation
			curr_node.delta = get_delta(std_dev, curr_left, curr_right, curr_node.weight, n_labels)
			curr_node.avg_delta = np.round(np.mean(curr_node.delta), precision)

			# If curr_node compares better than best_node, update
			if curr_node.compare(best_node):
				best_node = curr_node

	# Assign the current standard deviation to the best node & return
	best_node.std_dev = std_dev
	return best_node

""" Function that gets the weighted change in standard deviation for all labels 
	
	Inputs
		left: Two dimensional array of numbers
		right: Two dimensional array of numbers
		weight: Percentage (0<=weight<=1) of rows from input in left 
		n_labels: Number of label columns

	Output
		List of weighted changes in standard deviation for each label
	"""
def get_delta(std_dev, left, right, weight, n_labels): 
	# Initialize list of std_dev deltas
	delta = [None for i in range(n_labels)]
	
	# Compute std_dev for all labels
	for label in range(1, n_labels+1):
		# All elements on the left
		if weight == 1:
			std_left = np.std([x[-label] for x in left])
			std_right = 0
		# All elements on the right
		elif weight == 0: 
			std_left = 0
			std_right = np.std([x[-label] for x in right])
		# Elements split left & right
		else:
			std_left = np.std([x[-label] for x in left])
			std_right = np.std([x[-label] for x in right])

		# Add the change to the list
		delta[-label] = std_dev[-label] - (weight * std_left) - ((1 - weight) * std_right)
	# Return the mean of the standard deviation changes
	return delta

""" Function used to calculate percent difference between num1 & num2 
	
	Inputs
		num1, num2: Numbers

	Outputs
		Percentage between 0 & 100, or infinity if num2 is divisor incompatible
	"""
def pct_dif(num1, num2): 
	# Verify num2 compatibility
	if (num2==0 or num2==None):
		return float('inf')

	# Otherwise compute the percent difference
	return (abs(num1 - num2)/num2)*100

""" Function to recursively move down the tree until a leaf node is found for the given input features

	Inputs
		node: Node or LeafNode object - use tree.root to begin recursion
		row: Subset of row containing only the features used for this tree

	Outputs
		node: LeafNode providing best fit for the input features
	"""
def find_leaf(node, row):
	# If we have found a leaf node return
	if node.isLeaf:
		return node

	# Compare the row with node & make recursive call
	if row[node.index] >= node.value:
		return find_leaf(node.right_branch, row)
	else:
		return find_leaf(node.left_branch, row)