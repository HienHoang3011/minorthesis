#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.StaffAccount import StaffAccount
from domain.InventoryBatch import InventoryBatch
from typing import List

class InspectionRecord(object):
	def __init__(self):
		self._inspectionId : Integer = None
		self._recordType : String = None
		self._recordedAt : String = None
		self._conditionSummary : String = None
		self._careNote : String = None
		self._readyQty : Integer = None
		self._underCareQty : Integer = None
		self._removedQty : Integer = None
		self._reinspectionDate : String = None
		self._inspector : StaffAccount = None
		"""# @AssociationMultiplicity 1"""
		self._batch : InventoryBatch = None
		"""# @AssociationMultiplicity 1"""

