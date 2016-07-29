# тут надосделать ивенты вместо этой ебучей привязки к стдауту внутри независимого модуля

import os
import time
from hashlib import md5, sha256
from sys import stdout

# --- Exeption classes ---------------------------------------------

class FsItemNotFoundException(Exception):
	def __init__(self, path, type_):
		self._path = path
		self._type = type_

	def get_path(self):
		return self._path

	def get_type_(self):
		return self._type

class InvalidTypeException(Exception):
	def __init__(self, real_type, expected_type):
		self._real_type = real_type
		self._expected_type = expected_type

	def get_real_type(self):
		return self._real_type

	def get_expected_type(self):
		return self._expected_type

# --- Local members ------------------------------------------------

def stream_compare(stream1, stream2):
	BUFF_SIZE = 1024 * 4
	result = True
	while True:
		buff1 = stream1.read(BUFF_SIZE)
		buff2 = stream2.read(BUFF_SIZE)

		if not buff1 or not buff2:
			break

		if buff1 != buff2:
			result = False
			break

	return result

def _md5_sum(fname):
	hash_md5 = md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def _sha256_sum(fname):
	fhash = sha256()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			fhash.update(chunk)
	return fhash.hexdigest()

def _safety_enumerate_forward(subscriptable, begin=0):
	i = begin
	while i < len(subscriptable):
		yield i, subscriptable[i]
		i += 1

# --- Fs Classes ---------------------------------------------------

class FsItem:
	def __init__(self, path, type="n"):
		self._path = path

	def get_path(self):
		return self._path

	def get_name(self):
		head, tail = os.path.split(self.get_path())
		return tail

	def get_mtime(self):
		if self._mdate is None:
			self._mdate = os.path.getmtime(self._path)

		return self._mdate

	def __str__(self):
		return self.get_name()

class FsFile(FsItem):
	def __init__(self, path):
		path = str(path)
		if not os.path.isfile(path):
			raise FsItemNotFoundException(path, "f")

		FsItem.__init__(self, path);

		self._hash = None
		self._size = None
		self._mdate = None

	def get_hash(self):
		if self._hash is None:
			self._hash = _md5_sum(self._path) + _sha256_sum(self._path)

		return self._hash

	def get_size(self):
		if not self._size:
			self._size = os.path.getsize(self._path)

		return self._size

	def __str__(self):
		return FsItem.__str__(self)

# --- Public members -----------------------------------------

def set_compare_method(by_hash=0):
	if by_hash:
		FsFile.__eq__ = lambda self, obj: obj.get_hash() == self.get_hash()
	else:
		FsFile.__eq__ = lambda self, obj: stream_compare(open(obj.get_path(), "rb"), open(self.get_path(), "rb"))

def get_fs_items(dir_path, deep=-1):
	dir_path = str(dir_path)
	if not os.path.isdir(dir_path):
		raise FsItemNotFoundException(dir_path, "d")

	items = os.listdir(dir_path)

	result = [ ]
	for item in items:
		item = os.path.join(dir_path, item)

		if os.path.isfile(item):
			result.append(FsFile(item))
		elif deep != 0:
			result += get_fs_items(item, deep - 1)

	return result

# --- Analyzing Classes --------------------------------------------

class FsUniqueItemsMap:
	def __init__(self, files_list):
		self._files = files_list
		self._group_list = None

	def get_file_groups_by_lists(self):
		if self._group_list is None: # really i dont like big 'if' blocks
			size_map = { }
			for i, item in enumerate(self._files):
				if isinstance(item, str):
					item = FsFile(item)

				if not isinstance(item, FsFile):
					raise InvalidTypeException(type(item), FsFile)

				f_size = item.get_size()
				if f_size in size_map:
					size_map[f_size].append(item)
				else:
					size_map[f_size] = [ item ]

				stdout.write("{:} of {:} processed...\r".format(i, len(self._files)))
				stdout.flush()
			stdout.write('\n')

			self._group_list = [ ]
			for i, (i_size, items) in enumerate(size_map.items()):
				if len(items) > 1:
					for j, item1 in _safety_enumerate_forward(items):
						_items = [ item1 ]
						for k, item2 in _safety_enumerate_forward(items, j + 1):
							if item1 == item2:
								_items.append(item2)
								del items[k]

						if len(_items) > 1:
							self._group_list.append(_items)


					stdout.write("{:} of {:} compared...\r".format(i, len(size_map)))
					stdout.flush()

		return self._group_list

	def get_file_groups_by_map(self):
		if self._group_list is None: # really i dont like big 'if' blocks
			size_map = { }
			for i, item in enumerate(self._files):
				if isinstance(item, str):
					item = FsFile(item)

				if not isinstance(item, FsFile):
					raise InvalidTypeException(type(item), FsFile)

				f_size = item.get_size()
				if f_size in size_map:
					size_map[f_size].append(item)
				else:
					size_map[f_size] = [ item ]

				stdout.write("{:} of {:} processed...\r".format(i, len(self._files)))
				stdout.flush()
			stdout.write('\n')

			hash_map = { } # not full map
			for i, (i_size, items) in enumerate(size_map.items()):
				if len(items) > 1:
					for item in items:
						_hash = item.get_hash()
						if _hash in hash_map:
							hash_map[_hash].append(item)
						else:
							hash_map[_hash] = [ item ]

				stdout.write("{:} of {:} hash calculated...\r".format(i, len(size_map)))
				stdout.flush()
			stdout.write('\n')

			self._group_list = [ ]
			for i_hash, items in hash_map.items():
				if len(items) > 1:
					self._group_list.append(items)

		return self._group_list
