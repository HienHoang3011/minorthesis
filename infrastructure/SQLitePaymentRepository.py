#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.PaymentRepository import PaymentRepository
from typing import List

class SQLitePaymentRepository(PaymentRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToPayment(self, row):
		from domain.PaymentTransaction import PaymentTransaction
		p = PaymentTransaction()
		p._paymentId = row['paymentId']
		p._providerTransactionId = row['providerTransactionId']
		p._paymentMethod = row['paymentMethod']
		p._amountCents = row['amountCents']
		p._currency = row['currency']
		p._status = row['status']
		p._receivedAt = row['receivedAt']
		return p

	def findById(self, paymentId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM PaymentTransaction WHERE paymentId = ?', (paymentId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToPayment(row)

	def findByReservation(self, reservationId: int) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'SELECT * FROM PaymentTransaction WHERE reservationId = ?',
				(reservationId,)
			).fetchall()
		return [self._rowToPayment(r) for r in rows]

	def save(self, payment) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO PaymentTransaction
				   (paymentId, providerTransactionId, paymentMethod, amountCents,
				    currency, status, receivedAt, reservationId, orderId)
				   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				(payment._paymentId, payment._providerTransactionId,
				 payment._paymentMethod, payment._amountCents,
				 payment._currency, payment._status, payment._receivedAt,
				 payment._reservation._reservationId if payment._reservation else None,
				 payment._order._orderId if payment._order else None)
			)
