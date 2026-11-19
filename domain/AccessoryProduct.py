#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Product import Product
from typing import List

class AccessoryProduct(Product):
	def specifications(self) -> str:
		lines = []
		if self._accessoryType:
			lines.append(f'Loại phụ kiện: {self._accessoryType}')
		if self._material:
			lines.append(f'Chất liệu: {self._material}')
		if self._usageInstructions:
			lines.append(f'Hướng dẫn sử dụng: {self._usageInstructions}')
		return '\n'.join(lines)

	def searchDocument(self) -> str:
		parts = [p for p in [self._name, self._description, self._category,
		                      self._accessoryType, self._material] if p]
		return ' '.join(parts)

	def __init__(self):
		self._productId : Integer = None
		self._accessoryType : String = None
		self._material : String = None
		self._usageInstructions : String = None

