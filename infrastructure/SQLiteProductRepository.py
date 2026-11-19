#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.ProductRepository import ProductRepository
from typing import List

class SQLiteProductRepository(ProductRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToProduct(self, row):
		from domain.Product import Product
		p = Product()
		p._productId = row['productId']
		p._name = row['name']
		p._category = row['category']
		p._description = row['description']
		p._published = bool(row['published'])
		return p

	def findById(self, productId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM Product WHERE productId = ?', (productId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToProduct(row)

	def findSearchable(self) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'SELECT * FROM Product WHERE published = 1'
			).fetchall()
		return [self._rowToProduct(r) for r in rows]

	def findByIds(self, ids: list) -> list:
		if not ids:
			return []
		placeholders = ','.join('?' * len(ids))
		with self._tm.transaction() as conn:
			rows = conn.execute(
				f'SELECT * FROM Product WHERE productId IN ({placeholders})', ids
			).fetchall()
		return [self._rowToProduct(r) for r in rows]

	def save(self, product) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO Product
				   (productId, name, category, description, published)
				   VALUES (?, ?, ?, ?, ?)''',
				(product._productId, product._name, product._category,
				 product._description, 1 if product._published else 0)
			)
