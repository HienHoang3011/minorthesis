#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.ProductVariant import ProductVariant
from typing import List

class ProductImage(object):
	def __init__(self):
		self._imageId : Integer = None
		self._imageUrl : String = None
		self._sortOrder : Integer = None
		self._approved : Boolean = None
		self._variant : ProductVariant = None
		"""# @AssociationMultiplicity 1"""

