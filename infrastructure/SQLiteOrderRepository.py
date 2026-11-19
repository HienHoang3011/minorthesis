#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.OrderRepository import OrderRepository
from typing import List

class SQLiteOrderRepository(OrderRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToOrder(self, row):
		from domain.CustomerOrder import CustomerOrder
		o = CustomerOrder()
		o._orderId = row['orderId']
		o._orderRef = row['orderRef']
		o._receiverName = row['receiverName']
		o._receiverPhone = row['receiverPhone']
		o._deliveryAddress = row['deliveryAddress']
		o._deliveryOption = row['deliveryOption']
		o._shippingFeeCents = row['shippingFeeCents']
		o._status = row['status']
		o._totalCents = row['totalCents']
		o._currency = row['currency']
		o._createdAt = row['createdAt']
		o._paidAt = row['paidAt']
		o._cancellationReason = row['cancellationReason']
		return o

	def findById(self, orderId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM CustomerOrder WHERE orderId = ?', (orderId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToOrder(row)

	def findByCustomer(self, customerId: int) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'SELECT * FROM CustomerOrder WHERE customerId = ? ORDER BY createdAt DESC',
				(customerId,)
			).fetchall()
		return [self._rowToOrder(r) for r in rows]

	def save(self, order) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO CustomerOrder
				   (orderId, orderRef, receiverName, receiverPhone, deliveryAddress,
				    deliveryOption, shippingFeeCents, status, totalCents, currency,
				    createdAt, paidAt, cancellationReason,
				    customerId, reservationId)
				   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				(order._orderId, order._orderRef, order._receiverName,
				 order._receiverPhone, order._deliveryAddress,
				 order._deliveryOption, order._shippingFeeCents or 0,
				 order._status, order._totalCents, order._currency or 'VND',
				 order._createdAt, order._paidAt, order._cancellationReason,
				 order._customer._customerId if order._customer else None,
				 order._reservation._reservationId if order._reservation else None)
			)
