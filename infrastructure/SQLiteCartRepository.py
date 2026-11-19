#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.CartRepository import CartRepository
from typing import List

class SQLiteCartRepository(CartRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToCart(self, row):
		from domain.Cart import Cart
		c = Cart()
		c._cartId = row['cartId']
		c._sessionKey = row['sessionKey']
		c._createdAt = row['createdAt']
		c._updatedAt = row['updatedAt']
		return c

	def findByCustomer(self, customerId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM Cart WHERE customerId = ? LIMIT 1', (customerId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToCart(row)

	def findBySession(self, sessionKey: str):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM Cart WHERE sessionKey = ? LIMIT 1', (sessionKey,)
			).fetchone()
		if row is None:
			return None
		return self._rowToCart(row)

	def save(self, cart) -> None:
		import datetime
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO Cart
				   (cartId, sessionKey, createdAt, updatedAt, customerId)
				   VALUES (?, ?, ?, ?, ?)''',
				(cart._cartId, cart._sessionKey, cart._createdAt,
				 datetime.datetime.utcnow().isoformat(),
				 cart._owner._customerId if cart._owner else None)
			)
