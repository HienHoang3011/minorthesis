#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.CustomerOrder import CustomerOrder
from domain.ProductVariant import ProductVariant
from domain.InventoryBatch import InventoryBatch
from typing import List

class OrderLine(object):
	def __init__(self):
		self._orderLineId : Integer = None
		self._skuSnapshot : String = None
		self._nameSnapshot : String = None
		self._quantity : Integer = None
		self._unitPriceCents : Integer = None
		self._order : CustomerOrder = None
		"""# @AssociationMultiplicity 1"""
		self._variant : ProductVariant = None
		"""# @AssociationMultiplicity 1"""
		self._batch : InventoryBatch = None
		"""# @AssociationMultiplicity 1"""

