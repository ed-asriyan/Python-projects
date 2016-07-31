from sys import argv
import fsuniquesearcher
import time
from timeit import default_timer

try:
	from tabulate import tabulate
except:
	print("Module tabulate not installed.")
	print("Please install it first. To do this run the following command:")
	print("\tpython -m pip install tabulate")
	exit()

# --- Compar4 methods ----------------------------------------------

def compare_by_hash_map(files):
	map_ = fsuniquesearcher.FsUniqueItemsMap(files)

	files_groups = map_.get_file_groups_by_map()

	return files_groups

def compare_by_hash_lists(files):
	fsuniquesearcher.set_compare_method("hash")
	map_ = fsuniquesearcher.FsUniqueItemsMap(files)

	files_groups = map_.get_file_groups_by_lists()

	return files_groups

def compare_by_bytes_lists(files):
	fsuniquesearcher.set_compare_method("bytes")
	map_ = fsuniquesearcher.FsUniqueItemsMap(files)

	files_groups = map_.get_file_groups_by_lists()

	return files_groups

# --- Comparing interface ------------------------------------------

class CompareResult:
	def __init__(self, method, groups, time):
		self._method = method
		self._groups = groups
		self._time = time

	def get_method(self):
		return str(self._method)

	def get_groups(self):
		return self._groups

	def get_time(self):
		return self._time


class CompareMethod:
	def __init__(self, name, func):
		self._name = name
		self._func = func

	def get_name(self):
		return self._name

	def run(self, files):
		begin_time = default_timer()
		groups = self._func(files)
		end_time = default_timer()

		return CompareResult(self, groups, end_time - begin_time)

	def __str__(self):
		return self.get_name()


def get_compare_methods():
	return (
				CompareMethod("Hash map" , compare_by_hash_map),
		   		CompareMethod("Hash lists", compare_by_hash_lists),
		   		CompareMethod("Bytes lists", compare_by_bytes_lists),
		   )

# --- UI -----------------------------------------------------------

def get_table(methods_result):
	return [ ( m_result.get_method(), m_result.get_time(), len(m_result.get_groups()) ) for m_result in methods_result ]

def get_results_cmp_table(methods_result):
	m_results = methods_result[:]

	for m_res in m_results:
		groups = m_res.get_groups()

		for i in range(len(groups)):
			groups[i] = [ item.get_path() for item in groups[i] ]
			groups[i].sort()

		groups.sort()

	grid = [ [ "" ] + [ m_res.get_method() for m_res in m_results ] ]

	for i, m_res1 in enumerate(m_results):
		cmp_row = [ "-" ] * (i + 1)
		cmp_row += [ m_res1.get_groups() == m.get_groups() for m in m_results[i + 1:] ]

		grid.append([ m_res1.get_method() ] + cmp_row)

	return grid

# --- Main code ----------------------------------------------------

if __name__ == "__main__":
	if len(argv) < 2:
		print("Usage: python main.py [directiories...]")
		print("Example:\tpython test.py ~/Desktop ~/Downloads")
		exit()

	files = [ ]
	for path in argv[1:]:
		_files = fsuniquesearcher.get_fs_items(path)
		files += [ item for item in _files if not (item in files) ]

	methods = get_compare_methods()
	methods_result = [ ]
	for method in methods:
		print("Comparing by ", method, "...", sep="")
		methods_result.append(method.run(files))
		print("\nDone.\n")

	grid_time_body = get_table(methods_result)
	grid_time_body.sort(key=lambda x: x[1])

	grid_cmp = get_results_cmp_table(methods_result)

	print()
	print(tabulate(grid_cmp, tablefmt="fancy_grid"))
	print(tabulate(grid_time_body, headers=[ "Method", "Time", "Groups list size" ], tablefmt="fancy_grid"))



