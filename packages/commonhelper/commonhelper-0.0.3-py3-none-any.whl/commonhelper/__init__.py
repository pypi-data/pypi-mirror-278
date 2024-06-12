import importlib
import inspect
from collections import defaultdict

def reimport(namespace, moduleobj, varname = None, altname=None):
	'''
	Reimport the module using importlib. This function is useful when you need to update the library module.
	
	
	:param namespace: define where the import goes. Example: `globals()` or `locals()`
	:param moduleobj: The module name or the module
	:param varname: The variable name, if a variable is imported from the module
	:param altname: Alternative name

	Example usage: 
	
	.. code-block:: python
		
		# Reimport the following usage
		
		# import collections
		reimport(locals(), "collections")
		
		# import matplotlib.pyplot as plt
		reimport(locals(), "matplotlib.pyplot", altname = "plt")
		
		# from collections import defaultdict
		reimport(locals(), "collections", "defaultdict")
		
		# from collections import defaultdict as dd
		reimport(locals(), "collections", "defaultdict", altname = "dd")
		

	'''
	
	
	if inspect.ismodule(moduleobj):
		modname = moduleobj.__name__
	elif isinstance(moduleobj, str):
		modname = moduleobj

	module = importlib.reload(importlib.import_module(modname))
	
	# Import the module
	if varname is None:
		if altname is None:
			basemodename = modname.split(".")[0]
			namespace[basemodename] = importlib.import_module(basemodename)
			
		else:
			namespace[altname] = module
	# Import the variable
	else:
		# wild card case
		if varname == "*":
			try:
				varnames = module.__all__
			except AttributeError:
				varnames = [name for name in module if not name.startswith('_')]
			for varname in varnames:
				namespace[varname] = getattr(module, varname)
		# normal case
		else:
			if altname is None:
				altname = varname
			namespace[altname] = getattr(module, varname)
def convert_to_bool(s):
	'''
	A method to parse string (case insensitive) to boolean according to the text meaning.
	
	| true, yes, t, y, 1 are all regarded as True
	| false, no, f, n, 0 are all regarded as False
	
	Note that boolean(s) has a different meaning.
	
	This function is usually used in argument parsing
	
	.. code-block:: python
	
		convert_to_bool("yes") # True
		
		convert_to_bool("NO") # False
		
		convert_to_bool("ambiguous") # Exception raised
		
	'''
	if s.lower() in ("true", "yes", "t", "y", "1"):
		return True
	elif s.lower() in ("false", "no", "f", "n", "0"):
		return False
	else:
		raise Exception("Unable to interpret boolean value from: " + s)
	
def safe_inverse_zip(data, length):
	'''
	Wrapper for inverse zip.
	'''
	if len(data) == 0:
		return tuple(() for _ in range(length))
	else:
		if any(len(d) != length for d in data):
			raise Exception("Length and data not matched.") 
		return tuple(zip(*data))

def distribute_items_evenly(size, ngroup):
	'''
		Distribute items evenly and yield the beginindex (inclusive) and endindex (exclusive) of each group
		 
		Example usage: 
	
		.. code-block:: python
		
			distribute_items_evenly(5, 2) 
			# [(0, 3), (3, 5)]
			
			distribute_items_evenly(6, 2) 
			# [(0, 3), (3, 6)]
			
			
			
			# In conjunction with MultiProcessRun
			
			## Your custom function
			def _square(arr1):
				return [element * element for element in arr1]
			
			## Initialization
			CPU_NO = 40
			arr1 = [i for i in range(0, 10000)]
			
			## Body
			with MultiProcessRun(CPU_NO, _square) as mr:
				for (start, end) in distribute_items_evenly(len(arr1), CPU_NO):
					mr.run(args=[arr1[start:end]])
				results = mr.get(wait=True)
			## Final results	
			final_results = list(itertools.chain.from_iterable(results))
			
	'''
	if size < ngroup:
		raise Exception
	group_size = size // ngroup
	extra = size - ngroup * group_size
	prev_index = 0 
	for i in range(ngroup):
		index = prev_index + group_size + (1 if extra > i else 0)
		yield (prev_index, index)
		prev_index = index
	assert index == size
	

def isIterable(obj):
	'''
	Returns True if the obj is iterable.
	
	Example usage:
	
	.. code-block:: python
		
		print(isIterable([1,2,3])) # True
		
		print(isIterable("This is iterable")) # True
		
		print(isIterable(123)) # False
	'''
	
	try:
		iter(obj)
		return True
	except TypeError:
		return False
	
	
def _nested_default_dict(depth, default_factory):
	if depth > 1:
		return lambda: defaultdict(_nested_default_dict(depth - 1, default_factory))
	elif depth == 1:
		return lambda: defaultdict(default_factory)
	else:
		raise Exception("Invalid depth")

def nested_default_dict(depth, default_factory):
	'''
	A method to create nested defaultdict
	
	.. code-block:: python
	
		# The following are equivalent
		nested_default_dict(1, list)
		defaultdict(list)
		
		# The following are equivalent
		nested_default_dict(3, list)
		defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
		
	'''
	return _nested_default_dict(depth, default_factory)()	

def load_func(path, funcname):
	spec = importlib.util.spec_from_file_location("__main__", path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	func = getattr(module, funcname)
	return func

def sort_multiple_ordered_lists(lists):
	'''
	For items from multiple lists, try to sort them so that they follow the order of all lists. 
	
	sort_multiple_ordered_lists(['abc', 'bcdg', 'acef'])
	# ['a', 'b', 'c', 'd', 'g', 'e', 'f']
	
	sort_multiple_ordered_lists(['abc', 'bca'])
	# Exception thrown
	'''
	g_rev = {}
	g_fwd = {}
	for l in lists:
		for e in l:
			g_fwd[e] = set()
			g_rev[e] = set()

	for l in lists:
		for i, j in zip(l[:-1], l[1:]):
			g_fwd[i].add(j)
			g_rev[j].add(i)
	final_order = []
	outgoing = None
	while len(g_rev) > 0:
		found = []
		for k, v in g_rev.items():
			if len(v) == 0:
				found.append(k)
		if len(found) == 0:
			raise Exception("Contradicting order of elements exists in lists")
		if outgoing is None:
			k = found[0]
		else:
			best_candidates = [candidate for candidate in found if candidate in outgoing]
			if len(best_candidates) == 0:
				k = found[0]
			else:
				k = best_candidates[0]
		final_order.append(k)
		g_rev.pop(k)
		outgoing = g_fwd.pop(k)
		for i in outgoing:
			g_rev[i].remove(k)
	return final_order

def cluster_by_linkages(linkages):
	'''
	Given an iterable of linkage, cluster the elements (which must be hashable) 
	
	Example usage:
	
	.. code-block:: python
		
		linkages = [(1, 3), (1, 5), (2, 6), (3, 6, 9)]
		cluster_by_linkages(linkages)
		# Output: {1: {1, 2, 3, 5, 6, 9}, 3: {1, 2, 3, 5, 6, 9}, 5: {1, 2, 3, 5, 6, 9}, 2: {1, 2, 3, 5, 6, 9}, 6: {1, 2, 3, 5, 6, 9}, 9: {1, 2, 3, 5, 6, 9}}
		
		linkages = [(1, 3), (1, 5), (2, 6), (6, 9)]
		cluster_by_linkages(linkages)		
		# Output: {1: {1, 3, 5}, 3: {1, 3, 5}, 5: {1, 3, 5}, 2: {9, 2, 6}, 6: {9, 2, 6}, 9: {9, 2, 6}}
		
		linkages = [(1, 3), (1, 5), (2, 6), (6, 9)]
		list({id(cluster):cluster for cluster in cluster_by_linkages(linkages).values()}.values())
		# Output: [{1, 3, 5}, {9, 2, 6}]
	'''
	cluster_map = dict()
	for linkage in linkages:
		element_with_largest_cluster = max(linkage, key=lambda element: len(cluster_map[element]) if element in cluster_map else 0)
		if element_with_largest_cluster in cluster_map: 
			largest_cluster = cluster_map[element_with_largest_cluster]
		else:
			largest_cluster = set()
	
		for element in linkage:
			if element in cluster_map:
				if cluster_map[element] is not largest_cluster:
					for e in list(cluster_map[element]):
						largest_cluster.add(e)
						cluster_map[e] = largest_cluster
			else:
				largest_cluster.add(element)
				cluster_map[element] = largest_cluster
	
	return cluster_map