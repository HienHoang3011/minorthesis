#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from domain.StaffAccount import StaffAccount
from typing import List

class Product(object, metaclass=ABCMeta):
	def isSearchable(self) -> bool:
		return bool(self._published)

	def __init__(self):
		self._productId : Integer = None
		self._name : String = None
		self._category : String = None
		self._description : String = None
		self._published : Boolean = None
		self._publisher : StaffAccount = None
		"""# @AssociationMultiplicity 0..1"""
		self._variants = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""

