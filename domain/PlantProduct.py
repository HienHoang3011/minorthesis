#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Product import Product
from typing import List

class PlantProduct(Product):
	def specifications(self) -> str:
		lines = []
		if self._lightRequirement:
			lines.append(f'Ánh sáng: {self._lightRequirement}')
		if self._wateringFrequency:
			lines.append(f'Tưới nước: {self._wateringFrequency}')
		if self._careLevel:
			lines.append(f'Mức độ chăm sóc: {self._careLevel}')
		if self._expectedHeightCm:
			lines.append(f'Chiều cao dự kiến: {self._expectedHeightCm} cm')
		return '\n'.join(lines)

	def searchDocument(self) -> str:
		parts = [p for p in [self._name, self._description, self._category,
		                      self._lightRequirement, self._wateringFrequency,
		                      self._careLevel] if p]
		return ' '.join(parts)

	def __init__(self):
		self._productId : Integer = None
		self._lightRequirement : String = None
		self._wateringFrequency : String = None
		self._careLevel : String = None
		self._expectedHeightCm : Integer = None
		self._guides = []
		"""# @AssociationMultiplicity 0..*"""

