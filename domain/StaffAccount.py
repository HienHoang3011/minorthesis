#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class StaffAccount(object):
	def __init__(self):
		self._staffId : Integer = None
		self._email : String = None
		self._passwordHash : String = None
		self._status : String = None
		self._fullName : String = None
		self._roleName : String = None
		self._publishedProducts = []
		"""# @AssociationMultiplicity 0..*"""
		self._receivedBatches = []
		"""# @AssociationMultiplicity 0..*"""
		self._inspections = []
		"""# @AssociationMultiplicity 0..*"""

