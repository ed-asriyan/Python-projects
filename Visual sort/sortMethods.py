# --- Sort functions -----------------------------------------------

# --- простыми вставками -------------------------------------------

def insertionSort(l):
	for i in range(1, len(l)):
		j = i - 1 
		key = l[i]

		while (l[j] > key) and (j >= 0):
			l[j+1] = l[j]
			j -= 1
		l[j + 1] = key

	return l

# --- простыми вставками с бинарным поиском ------------------------

def insertionBinarySort(seq):
	return seq
	for i in range(1, len(seq)):
		key = seq[i]
		low, up = 0, i
		while up > low:
			middle = (low + up) // 2
			if seq[middle] < key:
				low = middle + 1				
			else:
				up = middle
		seq[:] = seq[:low] + [key] + seq[low:i] + seq[i + 1:]

	return seq

# --- простым выбором ----------------------------------------------

def selectionSort(mylist):
	for k in range(len(mylist) - 1):
		m = k
		i = k + 1
		while i < len(mylist):
			if mylist[i] < mylist[m]:
				m = i
			i += 1
		t = mylist[k]
		mylist[k] = mylist[m]
		mylist[m] = t

	return mylist

# --- слиянием -----------------------------------------------------

def merge(a, left, mid, right):
	"""
	Merge fuction
	"""
	#Copy array
	copy_list = [ ]
	i, j = left, mid + 1
	ind = left
	
	while ind < right+1:
		
		#if left array finish merging, copy from right side
		if i > mid:
			copy_list.append(a[j])
			j +=1
		#if right array finish merging, copy from left side
		elif j > right:
			copy_list.append(a[i])
			i +=1
		#Check if right array value is less than left one
		elif a[j] < a[i]:
			copy_list.append(a[j])
			j +=1
		else:
			copy_list.append(a[i])
			i +=1
		ind +=1
		
	ind=0
	for x in (range(left,right+1)):
		a[x] = copy_list[ind]
		ind += 1
		
def mergeSort(list_, left=0, right=None):
	if right is None:
		right = len(list_)

	factor = 2
	temp_mid = 0
	#Main loop to iterate over the array by 2^n.
	while 1:
		index = 0
		left = 0
		right = len(list_) - (len(list_) % factor) - 1
		mid = (factor // 2) - 1
		
		#Auxiliary array to merge subdivisions
		while index < right:
			temp_left = index
			temp_right = temp_left + factor -1
			mid2 = (temp_right +temp_left) // 2
			merge (list_, temp_left, mid2, temp_right)
			index = (index + factor)
		
		#Chek if there is something to merge from the remaining
		#Sub-array created by the factor
		if len(list_) % factor and temp_mid !=0:
			#merge sub array to later be merged to the final array
			merge(list_, right +1, temp_mid, len(list_)-1)
			#Update the pivot
			mid = right
		#Increase the factor
		factor = factor * 2
		temp_mid = right
		 
		#Final merge, merge subarrays created by the subdivision
		#of the factor to the main array.
		if factor > len(list_) :
			mid = right
			right = len(list_)-1
			merge(list_, 0, mid, right)
			break

# --- пузырьком ----------------------------------------------------

def bubbleSort(alist):
	for passnum in range(len(alist)-1,0,-1):
		for i in range(passnum):
			if alist[i] > alist[i+1]:
				alist[i], alist[i + 1] = alist[i + 1], alist[i]

	return alist

# --- шейкер -------------------------------------------------------

def cocktailSort(A):
	for k in range(len(A)-1, 0, -1):
		swapped = False
		for i in range(k, 0, -1):
			if A[i]<A[i-1]:
				A[i], A[i-1] = A[i-1], A[i]
				swapped = True

		for i in range(k):
			if A[i] > A[i+1]:
				A[i], A[i+1] = A[i+1], A[i]
				swapped = True
		
		if not swapped:
			break

	return A

# --- шелл ---------------------------------------------------------

def shellSort(array):
	 #"Shell sort using Shell's (original) gap sequence: n/2, n/4, ..., 1."
	gap = len(array) // 2
	# loop over the gaps
	while gap > 0:
		# do the insertion sort
		for i in range(gap, len(array)):
			val = array[i]
			j = i
			while j >= gap and array[j - gap] > val:
				array[j] = array[j - gap]
				j -= gap
			array[j] = val
		gap //= 2

	return array

# --- быстрая ------------------------------------------------------

from random import choice

def quickSort(alist):
	 quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
	 if first<last:

		 splitpoint = partition(alist,first,last)

		 quickSortHelper(alist,first,splitpoint-1)
		 quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
	 pivotvalue = alist[first]

	 leftmark = first+1
	 rightmark = last

	 done = False
	 while not done:

		 while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
			 leftmark = leftmark + 1

		 while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
			 rightmark = rightmark -1

		 if rightmark < leftmark:
			 done = True
		 else:
			 temp = alist[leftmark]
			 alist[leftmark] = alist[rightmark]
			 alist[rightmark] = temp

	 temp = alist[first]
	 alist[first] = alist[rightmark]
	 alist[rightmark] = temp


	 return rightmark

# --- Гномья -------------------------------------------------------

def gnomSort(a):
	i,j,size = 0,1,len(a)-1
	while i<size:
		if a[j]<a[i]:
			a[j],a[i] = a[i],a[j]
			if i!=0:
				i-=1
				j-=1
		else:
			i+=1
			j+=1
	return a

# Circle sort ------------------------------------------------------

def circle_sort_backend(A, L, R):
		n = R-L
		if n < 2:
				return 0
		swaps = 0
		m = n//2
		for i in range(m):
				if A[R-(i+1)] < A[L+i]:
						(A[R-(i+1)], A[L+i],) = (A[L+i], A[R-(i+1)],)
						swaps += 1
		if (n & 1) and (A[L+m] < A[L+m-1]):
				(A[L+m-1], A[L+m],) = (A[L+m], A[L+m-1],)
				swaps += 1
		return swaps + circle_sort_backend(A, L, L+m) + circle_sort_backend(A, L+m, R)
 
def circleSort(L):
		swaps = 0
		s = 1
		while s:
				s = circle_sort_backend(L, 0, len(L))
				swaps += s
		return swaps

# --- Heap ---------------------------------------------------------

def heapSort(lst):
	''' Heapsort. Note: this function sorts in-place (it mutates the list). '''
 
	# in pseudo-code, heapify only called once, so inline it here
	for start in range((len(lst)-2)//2, -1, -1):
		siftdown(lst, start, len(lst)-1)
 
	for end in range(len(lst)-1, 0, -1):
		lst[end], lst[0] = lst[0], lst[end]
		siftdown(lst, 0, end - 1)
	return lst
 
def siftdown(lst, start, end):
	root = start
	while True:
		child = root * 2 + 1
		if child > end: break
		if child + 1 <= end and lst[child] < lst[child + 1]:
			child += 1
		if lst[root] < lst[child]:
			lst[root], lst[child] = lst[child], lst[root]
			root = child
		else:
			break

# --- Stooge -------------------------------------------------------

def stoogeSort(L, i=0, j=None):
	if j is None:
		j = len(L) - 1
	if L[j] < L[i]:
		L[i], L[j] = L[j], L[i]
	if j - i > 1:
		t = (j - i + 1) // 3
		stoogeSort(L, i	, j-t)
		stoogeSort(L, i+t, j	)
		stoogeSort(L, i	, j-t)
	return L

# --- Counting -----------------------------------------------------

def countingSort(array):
		maxval = max(array)
		n = len(array)
		m = maxval + 1
		count = [0] * m							 # init with zeros
		for a in array:
				count[a] += 1						 # count occurences
		i = 0
		for a in range(m):						# emit
				for c in range(count[a]): # - emit 'count[a]' copies of 'a'
						array[i] = a
						i += 1
		return array

# --- Comb ---------------------------------------------------------

def combSort(input):
		gap = len(input)
		swaps = True
		while gap > 1 or swaps:
				gap = max(1, int(gap / 1.25))	# minimum gap is 1
				swaps = False
				for i in range(len(input) - gap):
						j = i+gap
						if input[i] > input[j]:
								input[i], input[j] = input[j], input[i]
								swaps = True

# --- Bogo ---------------------------------------------------------

from random import shuffle

def issorted(array):
		return not any(
				array[i] > array[i+1]
				for i in range(len(array)-1)
		)

def bogoSort(array):
		while not issorted(array):
				shuffle(array)

		return array

# --- Random -------------------------------------------------------

from random import randint

def checkSortedList(l, increase=True):
	if l is None:
		return None

	for i in range(len(l) - 1):
		diff = l[i + 1] - l[i]
		if diff and (diff < 0) == increase:
			return False
	return True

def randomSort(s):
	maxIndex = len(s) - 1
	while True:
		i, j = randint(0, maxIndex), randint(0, maxIndex)
		s[i], s[j] = s[j], s[i]
		if checkSortedList(s):
			break

# --- tim ----------------------------------------------------------

# thanks to Sofia (https://vk.com/soofiki) for code
def timSort(a):
	key = False

	saveLength = len(a)
	flag = 0
	while saveLength >= 64:
		flag |= saveLength & 1
		saveLength >>= 1
	minSize = saveLength + flag

	# Create the sub-arrays:
	subarrays = [ ]
	amountSubarr = len(a) // minSize

	countSubarr = 0
	j = 0
	if amountSubarr == 1:
			subarrays = a
			key = False
	else:
		key = True
		while countSubarr <= amountSubarr:
			subarrays.append([ j, j + minSize, minSize ])
			j += minSize
			countSubarr += 1

	# Insertion Sort for sub-arrays:
	if len(subarrays) == 10:
		for i in range(1, len(subarrays)):
			new_elem = subarrays[i]
			j = i - 1
			while j >= 0 and subarrays[j] > new_elem:
				subarrays[j + 1] = a[j]
				j -= 1
			subarrays[j + 1] = new_elem
	else:
		for p in range(len(subarrays)):
			for i in range(1, subarrays[2]):
				new_elem = a[subarrays[p][0] + i]# subarrays[p][i]
				j = i - 1
				while j >= 0 and a[subarrays[p][0] + j] > new_elem:
					a[subarrays[p][0] + j + 1] = a[subarrays[p][0] + j]
					j -= 1
				a[subarrays[p][0] + j + 1]= new_elem

		# Delete the array with length = 0:
		for j in range(len(subarrays)):
			if len(subarrays[j]) == 0:
				del subarrays[j]
	# Galloping Mode:
	sortingArray = [ ]
	if key == True:
		for j in range(len(subarrays) - 1):
			if len(subarrays[j]) <= len(subarrays[j + 1]):
				minSubarray = subarrays[j]
				bigSubarray = subarrays[j + 1]
				c = 0
				p = 0
				while c != minSubarray[2] and p != bigSubarray[2]:
					if minSubarray[c] < bigSubarray[p]:
						sortingArray.append(a[minSubarray[c][0]])
						if c < len(minSubarray):
							c += 1

					elif bigSubarray[p] < minSubarray[c]:
						sortingArray.append(bigSubarray[p])
						if p < len(bigSubarray):
							p += 1

					elif bigSubarray[p] == minSubarray[c]:
						if p < len(bigSubarray) and c < len(minSubarray):
							sortingArray.append(bigSubarray[p])
							sortingArray.append(minSubarray[c])
							p += 1
							c += 1

					if c == len(minSubarray):
						for d in range(p + 1, len(bigSubarray)):
							sortingArray.append(bigSubarray[d])

					if p == len(bigSubarray):
						for d in range(c + 1, len(minSubarray)):
							sortingArray.append(minSubarray[d])

# --- radix --------------------------------------------------------

def radixSort( aList ):
	RADIX = 10
	maxLength = False
	tmp , placement = -1, 1

	while not maxLength:
		maxLength = True
		# declare and initialize buckets
		buckets = [ list() for _ in range( RADIX ) ]

		# split aList between lists
		for	i in range(len(aList)):
			tmp = aList[i] // placement
			buckets[tmp % RADIX].append( aList[i] )
			if maxLength and tmp > 0:
				maxLength = False

		# empty lists into aList array
		a = 0
		for b in range( RADIX ):
			buck = buckets[b]
			for i in buck:
				aList[a] = i
				a += 1

		# move to next digit
		placement *= RADIX

SORT_METHODS = ( insertionSort, selectionSort,\
				 mergeSort, bubbleSort, cocktailSort,\
				 shellSort, quickSort, gnomSort,\
				 circleSort, heapSort, stoogeSort,\
				 countingSort, combSort, randomSort,\
				 bogoSort, radixSort, timSort )
