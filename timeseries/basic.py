#!/usr/bin/python3.5

import itertools
import reprlib
import numpy as np

def isNumericList(seq):
	'''
	This function checks if the sequence parsed as argument is numeric.
	'''
	for x in seq:
		try:
			float(x)
			return True
		except:
			return False

class TimeSeries:
	"""This TimeSeries class stores a single, ordered set of numerical data as a Python list."""
	def __init__(self, values, times=None):
		"""
		The constructor of the class takes for argumnent an ordered set of numerical data.

		Parameters
		----------

		values: Numerical Sequence, compulsory
		times: Ordered Numerical Sequence, optional

		Attributes
		----------
		
		self._times: list
		self._values: list
		self.timeseries: list of tuples (time, value)

		Notes
		-----

		- If no times argument is passed, then times will be initialised by their index: 1 to len(values)

		- Errors will be raised if values or times have non numerical entries or if the times are not in ascending order
		Examples:
		---------

		>>> t1 = TimeSeries([])
		>>> t1.timeseries
		[]
		>>> t2 = TimeSeries([1, 2, 3, 4, 5])
		>>> t2.timeseries
		[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
		>>> t3 = TimeSeries([1, 2, 3], [0, 0.25, 0.5])
		>>> t3.timeseries
		[(0, 1), (0.25, 2), (0.5, 3)]
		"""

		if len(values) == 0:
			self._times = []
			self._values = []
			self.timeseries = []
		else:
			assert isNumericList(values), "Values sequence must be only contain numerical entries"
			self._values = [v for v in values]
			if times:
				assert isNumericList(times), "Time sequence must be only contain numerical entries"
				assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
				assert len(times) == len(values), "Time and Value sequences must have the same lengths"
				self._times = [t for t in times]
			else:
				self._times = range(0,len(self._values))
			self.timeseries = list(zip(self._times, self._values))
		

	def __len__(self):
		""" 
		Returns the length of the TimeSeries object, which corresponds to the length of the timeseries attribute
		"""
		return len(self.timeseries)

	def __iter__(self):
		"""
		Returns an Iterator over values
		"""
		return iter(self._values)

	def itertimes(self):
		"""
		Returns an Iterator over times
		"""
		return iter(self._times)

	def iteritems(self):
		"""
		Returns an Iterator over values, time pair
		"""
		return iter(self.timeseries)

	def __getitem__(self, i):
		""" 
		Returns the ith value of the TimeSeries object
		
		Parameter
		---------

		i: int

		Notes
		-----

		- If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
		This is due to the fact that the underlying data structure is a Python list.
		"""

		return self._values[i]

	def __setitem__(self, i, value):
		""" 
		Sets the value of the ith item TimeSeries object to the value `value`

		Notes
		-----

		- !!!! The setitem method does not change the time associated with the ith item !!!!

		- If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
		This is due to the fact that the underlying data structure is a Python list.
		"""
		self._values[i] = value
		self.timeseries[i] = (self._times[i], value)

	def __repr__(self):
		'''
		This function returns the formal string representation of a TimeSeries object. We define the formal string
		representations by:

		Type(len=XX, timeseries=XX) 

		Notes
		-----

		- If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
		'''
		class_name = type(self).__name__
		length = len(self.timeseries)
		if length <= 5:
			return '{}(len = {}; timeseries = {})'.format(class_name, length, self.timeseries)
		else:
			components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
			components = components[:components.find(']')]
			return '{}(timeseries = {}, ...]; len = {})'.format(class_name, length, components)

	def __str__(self):
		'''
		This function returns the informal string representation of a TimeSeries object which only correponds to the
		string representation of the `timeseries` attribute.

		Notes
		-----

		- If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
		'''

		length = len(self.timeseries)
		if length <= 5:
			return str(self.timeseries)
		else:
			components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
			components = components[:components.find(']')]
			return '{}, ...]'.format(components)

	### Newly added Part 4
	def __contains__(self, value):
		return (value in self._values)

	def values(self):
		return np.array(self._values)

	def itervalues(self):
		return iter(self.values())

	def times(self):
		return np.array(self._times)

	def items(self):
		return self.timeseries

	def __abs__(self):
		return math.sqrt(sum(x * x for x in self.values()))

	def __bool__(self):
		return bool(abs(self))

	def __neg__(self):
		return TimeSeries([-x for x in self._values], [x for x in self._times])

	def __pos__(self):
		return TimeSeries(self._values, self._times)

	@staticmethod
	def _check_match_helper(self , rhs):
		if (not self.hastime) or (not rhs.hastime):
			raise NotImplemented
		if not self._times==rhs._times:
			raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')

	def __add__(self, rhs):
		if isinstance(rhs, TimeSeries):
			TimeSeries._check_match_helper(self, rhs)
			pairs = zip(self._values, rhs._values)
			return TimeSeries([a + b for a, b in pairs], [x for x in self._times])
		else:
			raise TypeError(str(rhs)+' must be a TimeSeries instance')

	def __sub__(self, rhs):
		if isinstance(rhs, TimeSeries):
			TimeSeries._check_match_helper(self, rhs)
			pairs = zip(self._values, rhs._values)
			return TimeSeries([a - b for a, b in pairs], [x for x in self._times])
		else:
			raise TypeError(str(rhs)+' must be a TimeSeries instance')

	def __mul__(self, rhs):
		if isinstance(rhs, TimeSeries):
			TimeSeries._check_match_helper(self, rhs)
			pairs = zip(self._values, rhs._values)
			return TimeSeries([a * b for a, b in pairs], [x for x in self._times])
		else:
			raise TypeError(str(rhs)+' must be a TimeSeries instance')

	def __eq__(self, rhs):
		if isinstance(rhs, TimeSeries):
			TimeSeries._check_match_helper(self, rhs)
			pairs = zip(self._values, rhs._values)
			return all([a==b for a, b in pairs])
		else:
			raise TypeError(str(rhs)+' must be a TimeSeries instance')


class ArrayTimeSeries(TimeSeries):
	def __init__(self, times, values):
		assert isNumericList(values), "Values sequence must be only contain numerical entries"
		self._values = np.array(values)
		if times:
			assert isNumericList(times), "Time sequence must be only contain numerical entries"
			assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
			self._times = np.array([t for t in times])
		else:
			self._times = np.arange(0,len(self._values))
		self.timeseries = np.array(list(zip(self._times, self._values)))

	def interpolate(self, times):
		assert len(self._times) >= 1, "require at least one time-value pair for interpolation"
		assert isNumericList(times), "Time sequence must be only contain numerical entries"
		interpolated = []
		for t in times:
			if t <= self._times[0]:
				interpolated.append(self._times[0])
			elif t >= self._times[-1]:
				interpolated.append(self._times[-1])
			else:
				prev_index = np.sum(self._times < t) - 1
				lin_slope = ((self._values[prev_index + 1] - self._values[prev_index])/
					     (self._times[prev_index + 1] - self._times[prev_index]))
				interpolated_val = self._values[prev_index] + (t - self._times[prev_index]) * lin_slope
				interpolated.append(interpolated_val)
		return interpolated
