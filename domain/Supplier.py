#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class Supplier(object):
	def __init__(self):
		self._supplierId : Integer = None
		self._supplierName : String = None
		self._contactName : String = None
		self._phone : String = None
		self._email : String = None
		self._batches = []
		"""# @AssociationMultiplicity 0..*"""

