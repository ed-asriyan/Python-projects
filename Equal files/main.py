# в этом файле какой-то пиздец с кодом, нужен рефакторинг

from sys import argv
from math import log
from os import remove
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

def size_to_str(size):
	size = int(size)

	power = int(log(abs(size), 1024) if size else 0)
	s = {
		0: "",
		1: "K",
		2: "M",
		3: "G",
		4: "T"
	}[power]

	return "{:.3f} {:}B".format(size / (1024 ** power), s)

def print_table(head, body):
	print(tabulate(body, headers=head, tablefmt="fancy_grid"))
	print('\n')

def get_file_info_row(file=None):
	if file is None:
		return [ "File Name", "File Size", "Modification Date" ]

	path = file.get_path().split('/')
	name = "/".join(path)
	while len(name) > 80 and len(path) > 1:
		if path[0] == "...":
			del path[0]
		path[0] = "..."

		name = "/".join(path)

	if len(name) > 80:
		name = "..." + name[-77:]

	return [ name, size_to_str(file.get_size()), str(time.ctime(file.get_mtime())) ]

if __name__ == '__main__':
	fsuniquesearcher.set_compare_method("bytes")

	if len(argv) < 2:
		print("Usage: python main.py [directiories...]")
		print("Example:\tpython main.py ~/Desktop ~/Downloads")
		exit()

	files = [ ]
	for path in argv[1:]:
		_files = fsuniquesearcher.get_fs_items(path)
		files += [ item for item in _files if not (item in files) ]

	files_size = sum([ file.get_size() for file in files ])
	files_count = len(files)

	map_ = fsuniquesearcher.FsUniqueItemsMap(files)

	start_time = default_timer()
	files_groups = map_.get_file_groups_by_lists()
	work_time =  default_timer() - start_time


	files_remove = [ ]
	for files in files_groups:
		files.sort(key=lambda x: x.get_mtime())
		files_remove += files[1:]
	files_remove_size = sum([ file.get_size() for file in files_remove ])
	files_remove_count = len(files_remove)

	table_samples = [ ]
	for files in files_groups:
		for file in files:
			table_samples.append(get_file_info_row(file) + [ len(files) ])
		table_samples.append([ "", "", "" ])

	table_remove = [ get_file_info_row(file) for file in files_remove ]

	table_total = [ [ "Files total:", files_count,           "Size total:" , size_to_str(files_size) ],
					[ "Remaining files:", files_count - files_remove_count,        "Remaining size:", size_to_str(files_size - files_remove_size) ],
					[ "Files to remove:", files_remove_count, "Removal size:", size_to_str(files_remove_size) ]
				  ]


	print("Groups of identical files:")
	print_table(get_file_info_row() + [ "Group Size" ], table_samples)

	print("Files which can be removed:")
	print_table(get_file_info_row(), table_remove)

	print_table([ ], table_total)

	print("Execution time:", work_time, end="\n\n")

	if files_remove_size:
		print("Choose an action")
		print("- delete dublicates (del)")
		print("- save groups of equal files (saveeq)")
		print("- save dubliates (savedub)")
		print("- quit (q)")

		ch = input(": ")

		if ch == "del":
			for file in files_remove:
				path = file.get_path()
				remove(file.get_path())
				print("Removed", path)

		if ch == "saveeq":
			with open("eq_files.txt", "w") as f:
				for files in files_groups:
					for file in files:
						f.write(file.get_path() + "\n")
					f.write("\n")

		if ch == "savedub":
			with open("dub_files.txt", w) as f:
				for file in files_remove_size:
					f.write(file.get_path() + "\n")
