#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.StaffAccount import StaffAccount
from domain.Supplier import Supplier
from domain.ProductVariant import ProductVariant
from typing import List

class InventoryBatch(object):
	def availableToReserve(self) -> int:
		return self._readyQty or 0

	def __init__(self):
		self._batchId : Integer = None
		self._supplierBatchRef : String = None
		self._arrivalDate : String = None
		self._receivedQty : Integer = None
		self._supplierDocumentQty : Integer = None
		self._readyQty : Integer = None
		self._reservedQty : Integer = None
		self._allocatedQty : Integer = None
		self._underCareQty : Integer = None
		self._removedQty : Integer = None
		self._dispatchedQty : Integer = None
		self._postedAt : String = None
		self._receiver : StaffAccount = None
		"""# @AssociationMultiplicity 1"""
		self._supplier : Supplier = None
		"""# @AssociationMultiplicity 1"""
		self._variant : ProductVariant = None
		"""# @AssociationMultiplicity 1"""
		self._inspections = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""
		self._holds = []
		"""# @AssociationMultiplicity 0..*"""
		self._allocatedLines = []
		"""# @AssociationMultiplicity 0..*"""

