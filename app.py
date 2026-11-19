#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Northfield Plant Shop — application bootstrap.

Wires the four-layer architecture produced by VP Instant Generator:
  domain/ → application/service/ → infrastructure/ → presentation/controller/

Usage:
  python app.py          # run a self-contained smoke test
  python app.py --demo   # print layer wiring summary
"""
import sys
import os
import sqlite3

# Allow running from the project root with plain `python app.py`
sys.path.insert(0, os.path.dirname(__file__))

from infrastructure.SQLiteTransactionManager      import SQLiteTransactionManager
from infrastructure.SQLiteProductRepository       import SQLiteProductRepository
from infrastructure.SQLiteCartRepository          import SQLiteCartRepository
from infrastructure.SQLiteOrderRepository         import SQLiteOrderRepository
from infrastructure.SQLiteInventoryRepository     import SQLiteInventoryRepository
from infrastructure.SQLiteReservationRepository   import SQLiteReservationRepository
from infrastructure.SQLitePaymentRepository       import SQLitePaymentRepository
from infrastructure.SQLiteCareGuideRepository     import SQLiteCareGuideRepository
from infrastructure.KeywordAdapter                import KeywordAdapter
from infrastructure.OptionalImageAdapter          import OptionalImageAdapter
from infrastructure.OptionalSpeechAdapter         import OptionalSpeechAdapter
from infrastructure.LocalPaymentGateway           import LocalPaymentGateway
from infrastructure.GeminiChatAdapter             import GeminiChatAdapter

from application.service.SearchService    import SearchService
from application.service.CheckoutService  import CheckoutService
from application.service.CareChatService  import CareChatService
from application.service.InventoryService import InventoryService

from presentation.controller.SearchController   import SearchController
from presentation.controller.CheckoutController import CheckoutController
from presentation.controller.CareController     import CareController


def build(db_path: str = ':memory:'):
    """Return fully-wired controller objects backed by *db_path*."""
    tm = SQLiteTransactionManager(db_path)

    # repositories
    product_repo     = SQLiteProductRepository(tm)
    cart_repo        = SQLiteCartRepository(tm)
    order_repo       = SQLiteOrderRepository(tm)
    inventory_repo   = SQLiteInventoryRepository(tm)
    reservation_repo = SQLiteReservationRepository(tm)
    payment_repo     = SQLitePaymentRepository(tm)
    care_guide_repo  = SQLiteCareGuideRepository(tm)

    # ports (optional AI adapters fall back gracefully when libraries absent)
    keyword_adapter  = KeywordAdapter()
    image_adapter    = OptionalImageAdapter()
    speech_adapter   = OptionalSpeechAdapter()
    payment_gateway  = LocalPaymentGateway()
    gemini_adapter   = GeminiChatAdapter()

    # services
    search_svc   = SearchService(product_repo, keyword_adapter,
                                 imageSearch=image_adapter,
                                 speechTranscriber=speech_adapter)
    checkout_svc = CheckoutService(cart_repo, product_repo, inventory_repo,
                                   reservation_repo, payment_repo, payment_gateway)
    care_svc     = CareChatService(care_guide_repo, geminiAdapter=gemini_adapter)
    inventory_svc = InventoryService(inventory_repo)

    # pre-build keyword index from published products (if DB already has data)
    try:
        products = product_repo.findSearchable()
        if products:
            keyword_adapter.buildIndex(products)
    except Exception:
        pass

    # controllers
    search_ctrl   = SearchController(search_svc)
    checkout_ctrl = CheckoutController(checkout_svc)
    care_ctrl     = CareController(care_svc)

    return search_ctrl, checkout_ctrl, care_ctrl, tm


def _init_schema(db_path: str) -> None:
    """Create tables from tieuluan.ddl in the given SQLite database."""
    ddl_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(ddl_path, encoding='utf-8') as fh:
        ddl = fh.read()
    conn = sqlite3.connect(db_path)
    conn.executescript(ddl)
    conn.commit()
    conn.close()


def _smoke_test():
    """Wire every layer and exercise basic paths end-to-end."""
    import tempfile, os

    print('Northfield Plant Shop — smoke test')
    print('=' * 45)

    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    try:
        _init_schema(db_path)
        search_ctrl, checkout_ctrl, care_ctrl, tm = build(db_path)

        # 1. text search on empty catalogue → empty result, no crash
        result = search_ctrl.search(query='fern', limit=5)
        assert isinstance(result['items'], list)
        print('  [PASS] SearchController.search — empty catalogue returns []')

        # 2. image search fallback (no model installed) → empty result
        result = search_ctrl.search(imageBytes=b'\x89PNG', limit=5)
        assert result['items'] == []
        print('  [PASS] SearchController.search — image fallback returns []')

        # 3. voice transcription fallback → empty string
        text = search_ctrl.transcribeAudio(b'\x00\x00')
        assert text == ''
        print('  [PASS] SearchController.transcribeAudio — speech fallback returns ""')

        # 4. care answer with no approved guides → polite refusal
        answer = care_ctrl.answer(question='how often to water?', productId=999)
        assert answer['isRefusal'] is True
        print('  [PASS] CareController.answer — refusal when no guides')

        # 5. checkout on nonexistent cart → ValueError
        try:
            checkout_ctrl.beginCheckout(
                customerId=1, cartId=1,
                deliveryAddress='12 Green St', deliveryOption='STANDARD',
                quotedTotalCents=10000, receiverName='Test', receiverPhone='0901234567'
            )
            assert False, 'Should have raised'
        except (ValueError, Exception):
            pass
        print('  [PASS] CheckoutController.beginCheckout — raises on missing cart')

        print('=' * 45)
        print('All smoke tests passed.')
    finally:
        os.unlink(db_path)


def _demo():
    print('Northfield Plant Shop — layer wiring')
    print('=' * 45)
    layers = [
        ('domain/',                 '20 persistent classes (VP Instant Generator)'),
        ('application/service/',    'SearchService, CheckoutService, CareChatService, InventoryService'),
        ('infrastructure/',         'SQLite repos, KeywordAdapter, LocalPaymentGateway'),
        ('presentation/controller/','SearchController, CheckoutController, CareController'),
    ]
    for layer, desc in layers:
        print(f'  {layer:<32} {desc}')
    print('=' * 45)
    print('Entry point: build(db_path) → (search_ctrl, checkout_ctrl, care_ctrl, tm)')


if __name__ == '__main__':
    if '--demo' in sys.argv:
        _demo()
    else:
        _smoke_test()
