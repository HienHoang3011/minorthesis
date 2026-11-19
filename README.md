# Northfield Plant Shop — Minor Thesis Project

Hệ thống thương mại điện tử bán cây cảnh và phụ kiện, được thiết kế theo kiến trúc 4 tầng (Presentation → Application → Infrastructure → Domain) và sinh khung mã từ mô hình UML bằng Visual Paradigm Instant Generator.

## Cấu trúc thư mục

```
minorthesis/
├── domain/                     # Các lớp miền (20 lớp)
│   ├── Product.py
│   ├── PlantProduct.py
│   ├── AccessoryProduct.py
│   ├── ProductVariant.py
│   ├── ProductImage.py
│   ├── Customer.py
│   ├── Cart.py
│   ├── CartItem.py
│   ├── CustomerOrder.py
│   ├── OrderLine.py
│   ├── StockReservation.py
│   ├── ReservationItem.py
│   ├── InventoryBatch.py
│   ├── InspectionRecord.py
│   ├── Shipment.py
│   ├── ShipmentEvent.py
│   ├── PaymentTransaction.py
│   ├── CareGuide.py
│   ├── Supplier.py
│   └── StaffAccount.py
├── application/
│   └── service/                # Giao diện kho lưu trữ & ca sử dụng
│       ├── ProductRepository.py
│       ├── CartRepository.py
│       ├── OrderRepository.py
│       ├── InventoryRepository.py
│       ├── ReservationRepository.py
│       ├── PaymentRepository.py
│       ├── CareGuideRepository.py
│       ├── KeywordSearch.py
│       ├── ImageSearch.py
│       ├── SpeechTranscriber.py
│       ├── PaymentGateway.py
│       ├── SearchRequest.py
│       ├── SearchResult.py
│       ├── CareAnswer.py
│       ├── SearchService.py
│       ├── CareChatService.py
│       ├── CheckoutService.py
│       └── InventoryService.py
├── infrastructure/             # Triển khai SQLite & adapter tùy chọn
│   ├── SQLiteTransactionManager.py
│   ├── SQLiteProductRepository.py
│   ├── SQLiteCartRepository.py
│   ├── SQLiteOrderRepository.py
│   ├── SQLiteInventoryRepository.py
│   ├── SQLiteReservationRepository.py
│   ├── SQLitePaymentRepository.py
│   ├── SQLiteCareGuideRepository.py
│   ├── KeywordAdapter.py
│   ├── LocalPaymentGateway.py
│   ├── OptionalImageAdapter.py
│   └── OptionalSpeechAdapter.py
├── presentation/
│   └── controller/             # Lớp điều khiển
│       ├── SearchController.py
│       ├── CheckoutController.py
│       └── CareController.py
├── tieuluan.ddl                # DDL gốc từ VP (tham khảo)
├── schema.sql                  # DDL sạch, dùng để khởi tạo DB
├── app.py                      # Bootstrap toàn bộ 4 tầng
└── presentation/
    └── web/
        ├── server.py           # HTTP API server (built-in http.server)
        └── index.html          # Giao diện storefront
```

## Công nghệ

- **Ngôn ngữ:** Python 3
- **Cơ sở dữ liệu:** SQLite (file local, không cần máy chủ)
- **Mô hình thiết kế:** UML class diagram → Visual Paradigm Instant Generator
- **Kiến trúc:** 4 tầng (Presentation / Application / Infrastructure / Domain)

## Chạy ứng dụng

```bash
# Smoke test toàn bộ layer wiring
python3 app.py

# Khởi động web server (tạo DB nếu chưa có)
python3 presentation/web/server.py 8000 northfield.db
# Mở http://localhost:8000 trên trình duyệt
```

API endpoints:
- `GET  /api/health`              — kiểm tra server
- `GET  /api/search?q=&limit=20` — tìm kiếm sản phẩm
- `POST /api/search/image`        — tìm kiếm bằng ảnh (body = raw bytes)
- `GET  /api/care?question=&productId=` — hỏi trợ lý chăm sóc
- `POST /api/checkout/begin`      — bắt đầu thanh toán (JSON body)
- `POST /api/checkout/confirm`    — xác nhận thanh toán (JSON body)

## Khởi động nhanh (programmatic)

```python
from infrastructure.SQLiteTransactionManager import SQLiteTransactionManager
from infrastructure.SQLiteProductRepository import SQLiteProductRepository
from infrastructure.KeywordAdapter import KeywordAdapter
from application.service.SearchService import SearchService
from presentation.controller.SearchController import SearchController

tm = SQLiteTransactionManager('shop.db')
productRepo = SQLiteProductRepository(tm)
keyword = KeywordAdapter()

products = productRepo.findSearchable()
keyword.buildIndex(products)

service = SearchService(productRepo, keyword)
ctrl = SearchController(service)
print(ctrl.search('monstera'))
```
