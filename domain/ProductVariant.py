#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Product import Product
from typing import List

class ProductVariant(object):
	def isSaleable(self) -> bool:
		return self._saleStatus == 'active'

	def __init__(self):
		self._variantId : Integer = None
		self._sku : String = None
		self._sizeLabel : String = None
		self._optionLabel : String = None
		self._priceCents : Integer = None
		self._saleStatus : String = None
		self._product : Product = None
		"""# @AssociationMultiplicity 1"""
		self._images = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""
		self._batches = []
		"""# @AssociationMultiplicity 0..*"""
		self._cartItems = []
		"""# @AssociationMultiplicity 0..*"""
		self._orderLines = []
		"""# @AssociationMultiplicity 0..*"""

