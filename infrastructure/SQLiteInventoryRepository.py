#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.InventoryRepository import InventoryRepository
from typing import List

class SQLiteInventoryRepository(InventoryRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToBatch(self, row):
		from domain.InventoryBatch import InventoryBatch
		b = InventoryBatch()
		b._batchId = row['batchId']
		b._supplierBatchRef = row['supplierBatchRef']
		b._arrivalDate = row['arrivalDate']
		b._receivedQty = row['receivedQty']
		b._supplierDocumentQty = row['supplierDocumentQty']
		b._readyQty = row['readyQty']
		b._reservedQty = row['reservedQty']
		b._allocatedQty = row['allocatedQty']
		b._underCareQty = row['underCareQty']
		b._removedQty = row['removedQty']
		b._dispatchedQty = row['dispatchedQty']
		b._postedAt = row['postedAt']
		return b

	def findBatch(self, batchId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM InventoryBatch WHERE batchId = ?', (batchId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToBatch(row)

	def findByVariant(self, variantId: int) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'SELECT * FROM InventoryBatch WHERE variantId = ? ORDER BY arrivalDate DESC',
				(variantId,)
			).fetchall()
		return [self._rowToBatch(r) for r in rows]

	def saveBatch(self, batch) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO InventoryBatch
				   (batchId, supplierBatchRef, arrivalDate, receivedQty,
				    supplierDocumentQty, readyQty, reservedQty, allocatedQty,
				    underCareQty, removedQty, dispatchedQty, postedAt,
				    receiverStaffId, supplierId, variantId)
				   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				(batch._batchId, batch._supplierBatchRef, batch._arrivalDate,
				 batch._receivedQty, batch._supplierDocumentQty,
				 batch._readyQty or 0, batch._reservedQty or 0,
				 batch._allocatedQty or 0, batch._underCareQty or 0,
				 batch._removedQty or 0, batch._dispatchedQty or 0,
				 batch._postedAt,
				 batch._receiver._staffId if batch._receiver else None,
				 batch._supplier._supplierId if batch._supplier else None,
				 batch._variant._variantId if batch._variant else None)
			)

	def saveInspection(self, record) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO InspectionRecord
				   (inspectionId, recordType, recordedAt, conditionSummary,
				    careNote, readyQty, underCareQty, removedQty,
				    reinspectionDate, inspectorStaffId, batchId)
				   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				(record._inspectionId, record._recordType, record._recordedAt,
				 record._conditionSummary, record._careNote,
				 record._readyQty or 0, record._underCareQty or 0,
				 record._removedQty or 0, record._reinspectionDate,
				 record._inspector._staffId if record._inspector else None,
				 record._batch._batchId if record._batch else None)
			)
