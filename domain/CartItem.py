#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Cart import Cart
from domain.ProductVariant import ProductVariant
from typing import List

class CartItem(object):
	def __init__(self):
		self._cartItemId : Integer = None
		self._quantity : Integer = None
		self._cart : Cart = None
		"""# @AssociationMultiplicity 1"""
		self._variant : ProductVariant = None
		"""# @AssociationMultiplicity 1"""

