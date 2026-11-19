#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.CareGuideRepository import CareGuideRepository

class SQLiteCareGuideRepository(CareGuideRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToGuide(self, row):
		from domain.CareGuide import CareGuide
		g = CareGuide()
		g._guideId = row['guideId']
		g._categoryScope = row['categoryScope']
		g._title = row['title']
		g._content = row['content']
		g._sourceTitle = row['sourceTitle']
		g._approved = bool(row['approved'])
		g._revisionDate = row['revisionDate']
		return g

	def findByPlant(self, plantProductId: int) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'''SELECT * FROM CareGuide
				   WHERE plantProductId = ? AND approved = 1''',
				(plantProductId,)
			).fetchall()
		return [self._rowToGuide(r) for r in rows]

	def findByCategory(self, categoryScope: str) -> list:
		with self._tm.transaction() as conn:
			rows = conn.execute(
				'SELECT * FROM CareGuide WHERE categoryScope = ? AND approved = 1',
				(categoryScope,)
			).fetchall()
		return [self._rowToGuide(r) for r in rows]

	def findById(self, guideId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM CareGuide WHERE guideId = ?', (guideId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToGuide(row)
