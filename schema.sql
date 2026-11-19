-- Northfield Plant Shop — clean DDL derived from tieuluan.ddl
-- Column names match VP domain class attribute names (without ___ prefix).
-- Duplicate VP-generated association columns removed; FK paths kept.

PRAGMA foreign_keys = ON;

CREATE TABLE StaffAccount (
    staffId       INTEGER PRIMARY KEY AUTOINCREMENT,
    email         VARCHAR(255) NOT NULL UNIQUE,
    passwordHash  VARCHAR(255) NOT NULL,
    status        VARCHAR(50)  NOT NULL DEFAULT 'active',
    fullName      VARCHAR(255) NOT NULL,
    roleName      VARCHAR(50)  NOT NULL
);

CREATE TABLE Product (
    productId        INTEGER PRIMARY KEY AUTOINCREMENT,
    name             VARCHAR(255) NOT NULL,
    category         VARCHAR(255) NOT NULL,
    description      TEXT         NOT NULL DEFAULT '',
    published        INTEGER      NOT NULL DEFAULT 0,
    publisherStaffId INTEGER,
    FOREIGN KEY (publisherStaffId) REFERENCES StaffAccount(staffId)
);

CREATE TABLE PlantProduct (
    productId          INTEGER PRIMARY KEY,
    lightRequirement   VARCHAR(50)  NOT NULL DEFAULT '',
    wateringFrequency  VARCHAR(100) NOT NULL DEFAULT '',
    careLevel          VARCHAR(50)  NOT NULL DEFAULT '',
    expectedHeightCm   INTEGER,
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

CREATE TABLE AccessoryProduct (
    productId          INTEGER PRIMARY KEY,
    accessoryType      VARCHAR(100) NOT NULL DEFAULT '',
    material           VARCHAR(100) NOT NULL DEFAULT '',
    usageInstructions  TEXT         NOT NULL DEFAULT '',
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

CREATE TABLE ProductVariant (
    variantId   INTEGER PRIMARY KEY AUTOINCREMENT,
    productId   INTEGER NOT NULL,
    sku         VARCHAR(100) NOT NULL UNIQUE,
    sizeLabel   VARCHAR(50)  NOT NULL DEFAULT '',
    optionLabel VARCHAR(100) NOT NULL DEFAULT '',
    priceCents  INTEGER      NOT NULL DEFAULT 0,
    saleStatus  VARCHAR(50)  NOT NULL DEFAULT 'active',
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

CREATE TABLE ProductImage (
    imageId   INTEGER PRIMARY KEY AUTOINCREMENT,
    variantId INTEGER NOT NULL,
    imageUrl  VARCHAR(500) NOT NULL,
    sortOrder INTEGER      NOT NULL DEFAULT 0,
    approved  INTEGER      NOT NULL DEFAULT 0,
    FOREIGN KEY (variantId) REFERENCES ProductVariant(variantId)
);

CREATE TABLE CareGuide (
    guideId        INTEGER PRIMARY KEY AUTOINCREMENT,
    plantProductId INTEGER,
    categoryScope  VARCHAR(255),
    title          VARCHAR(255) NOT NULL,
    content        TEXT         NOT NULL,
    sourceTitle    VARCHAR(255) NOT NULL DEFAULT '',
    approved       INTEGER      NOT NULL DEFAULT 0,
    revisionDate   VARCHAR(50)  NOT NULL DEFAULT '',
    FOREIGN KEY (plantProductId) REFERENCES PlantProduct(productId)
);

CREATE TABLE Customer (
    customerId      INTEGER PRIMARY KEY AUTOINCREMENT,
    email           VARCHAR(255) NOT NULL UNIQUE,
    passwordHash    VARCHAR(255) NOT NULL,
    status          VARCHAR(50)  NOT NULL DEFAULT 'active',
    fullName        VARCHAR(255) NOT NULL DEFAULT '',
    phone           VARCHAR(50)  NOT NULL DEFAULT '',
    defaultAddress  TEXT         NOT NULL DEFAULT '',
    lightLevel      VARCHAR(50),
    spaceCm         INTEGER,
    careEffort      VARCHAR(50)
);

CREATE TABLE Cart (
    cartId      INTEGER PRIMARY KEY AUTOINCREMENT,
    customerId  INTEGER,
    sessionKey  VARCHAR(255) UNIQUE,
    createdAt   VARCHAR(50) NOT NULL DEFAULT '',
    updatedAt   VARCHAR(50) NOT NULL DEFAULT '',
    FOREIGN KEY (customerId) REFERENCES Customer(customerId)
);

CREATE TABLE CartItem (
    cartItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    cartId     INTEGER NOT NULL,
    variantId  INTEGER NOT NULL,
    quantity   INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (cartId)    REFERENCES Cart(cartId),
    FOREIGN KEY (variantId) REFERENCES ProductVariant(variantId)
);

CREATE TABLE Supplier (
    supplierId   INTEGER PRIMARY KEY AUTOINCREMENT,
    supplierName VARCHAR(255) NOT NULL,
    contactName  VARCHAR(255) NOT NULL DEFAULT '',
    phone        VARCHAR(50)  NOT NULL DEFAULT '',
    email        VARCHAR(255) NOT NULL DEFAULT ''
);

CREATE TABLE InventoryBatch (
    batchId            INTEGER PRIMARY KEY AUTOINCREMENT,
    variantId          INTEGER NOT NULL,
    supplierId         INTEGER NOT NULL,
    receiverStaffId    INTEGER NOT NULL,
    supplierBatchRef   VARCHAR(255) NOT NULL,
    arrivalDate        VARCHAR(50)  NOT NULL,
    receivedQty        INTEGER NOT NULL DEFAULT 0,
    supplierDocumentQty INTEGER,
    readyQty           INTEGER NOT NULL DEFAULT 0,
    reservedQty        INTEGER NOT NULL DEFAULT 0,
    allocatedQty       INTEGER NOT NULL DEFAULT 0,
    underCareQty       INTEGER NOT NULL DEFAULT 0,
    removedQty         INTEGER NOT NULL DEFAULT 0,
    dispatchedQty      INTEGER NOT NULL DEFAULT 0,
    postedAt           VARCHAR(50),
    FOREIGN KEY (variantId)       REFERENCES ProductVariant(variantId),
    FOREIGN KEY (supplierId)      REFERENCES Supplier(supplierId),
    FOREIGN KEY (receiverStaffId) REFERENCES StaffAccount(staffId)
);

CREATE TABLE InspectionRecord (
    inspectionId     INTEGER PRIMARY KEY AUTOINCREMENT,
    batchId          INTEGER NOT NULL,
    inspectorStaffId INTEGER NOT NULL,
    recordType       VARCHAR(50)  NOT NULL,
    recordedAt       VARCHAR(50)  NOT NULL,
    conditionSummary TEXT         NOT NULL DEFAULT '',
    careNote         TEXT,
    readyQty         INTEGER NOT NULL DEFAULT 0,
    underCareQty     INTEGER NOT NULL DEFAULT 0,
    removedQty       INTEGER NOT NULL DEFAULT 0,
    reinspectionDate VARCHAR(50),
    FOREIGN KEY (batchId)          REFERENCES InventoryBatch(batchId),
    FOREIGN KEY (inspectorStaffId) REFERENCES StaffAccount(staffId)
);

CREATE TABLE StockReservation (
    reservationId   INTEGER PRIMARY KEY AUTOINCREMENT,
    customerId      INTEGER NOT NULL,
    cartId          INTEGER NOT NULL,
    checkoutRef     VARCHAR(255) NOT NULL UNIQUE,
    receiverName    VARCHAR(255) NOT NULL DEFAULT '',
    receiverPhone   VARCHAR(50)  NOT NULL DEFAULT '',
    deliveryAddress TEXT         NOT NULL DEFAULT '',
    deliveryOption  VARCHAR(50)  NOT NULL DEFAULT 'standard',
    shippingFeeCents INTEGER     NOT NULL DEFAULT 0,
    totalCents      INTEGER      NOT NULL DEFAULT 0,
    currency        VARCHAR(10)  NOT NULL DEFAULT 'VND',
    status          VARCHAR(50)  NOT NULL DEFAULT 'pending',
    createdAt       VARCHAR(50)  NOT NULL DEFAULT '',
    expiresAt       VARCHAR(50)  NOT NULL DEFAULT '',
    FOREIGN KEY (customerId) REFERENCES Customer(customerId),
    FOREIGN KEY (cartId)     REFERENCES Cart(cartId)
);

CREATE TABLE ReservationItem (
    reservationItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    reservationId     INTEGER NOT NULL,
    batchId           INTEGER NOT NULL,
    quantity          INTEGER NOT NULL DEFAULT 1,
    unitPriceCents    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (reservationId) REFERENCES StockReservation(reservationId),
    FOREIGN KEY (batchId)       REFERENCES InventoryBatch(batchId)
);

CREATE TABLE CustomerOrder (
    orderId             INTEGER PRIMARY KEY AUTOINCREMENT,
    customerId          INTEGER NOT NULL,
    reservationId       INTEGER NOT NULL,
    orderRef            VARCHAR(255) NOT NULL UNIQUE,
    receiverName        VARCHAR(255) NOT NULL DEFAULT '',
    receiverPhone       VARCHAR(50)  NOT NULL DEFAULT '',
    deliveryAddress     TEXT         NOT NULL DEFAULT '',
    deliveryOption      VARCHAR(50)  NOT NULL DEFAULT 'standard',
    shippingFeeCents    INTEGER      NOT NULL DEFAULT 0,
    status              VARCHAR(50)  NOT NULL DEFAULT 'placed',
    totalCents          INTEGER      NOT NULL DEFAULT 0,
    currency            VARCHAR(10)  NOT NULL DEFAULT 'VND',
    createdAt           VARCHAR(50)  NOT NULL DEFAULT '',
    paidAt              VARCHAR(50),
    cancellationReason  TEXT,
    FOREIGN KEY (customerId)    REFERENCES Customer(customerId),
    FOREIGN KEY (reservationId) REFERENCES StockReservation(reservationId)
);

CREATE TABLE OrderLine (
    orderLineId   INTEGER PRIMARY KEY AUTOINCREMENT,
    orderId       INTEGER NOT NULL,
    variantId     INTEGER NOT NULL,
    batchId       INTEGER NOT NULL,
    skuSnapshot   VARCHAR(100) NOT NULL DEFAULT '',
    nameSnapshot  VARCHAR(255) NOT NULL DEFAULT '',
    quantity      INTEGER      NOT NULL DEFAULT 1,
    unitPriceCents INTEGER     NOT NULL DEFAULT 0,
    FOREIGN KEY (orderId)   REFERENCES CustomerOrder(orderId),
    FOREIGN KEY (variantId) REFERENCES ProductVariant(variantId),
    FOREIGN KEY (batchId)   REFERENCES InventoryBatch(batchId)
);

CREATE TABLE PaymentTransaction (
    paymentId             INTEGER PRIMARY KEY AUTOINCREMENT,
    reservationId         INTEGER NOT NULL,
    orderId               INTEGER,
    providerTransactionId VARCHAR(255),
    paymentMethod         VARCHAR(50)  NOT NULL DEFAULT 'online',
    amountCents           INTEGER      NOT NULL DEFAULT 0,
    currency              VARCHAR(10)  NOT NULL DEFAULT 'VND',
    status                VARCHAR(50)  NOT NULL DEFAULT 'pending',
    receivedAt            VARCHAR(50),
    FOREIGN KEY (reservationId) REFERENCES StockReservation(reservationId),
    FOREIGN KEY (orderId)       REFERENCES CustomerOrder(orderId)
);

CREATE TABLE Shipment (
    shipmentId                  INTEGER PRIMARY KEY AUTOINCREMENT,
    orderId                     INTEGER NOT NULL,
    trackingRef                 VARCHAR(255),
    carrierName                 VARCHAR(255),
    handlingInstructions        TEXT    NOT NULL DEFAULT '',
    dispatchChecklistCompleted  INTEGER NOT NULL DEFAULT 0,
    dispatchCheckNote           TEXT,
    status                      VARCHAR(50) NOT NULL DEFAULT 'pending',
    dispatchedAt                VARCHAR(50),
    FOREIGN KEY (orderId) REFERENCES CustomerOrder(orderId)
);

CREATE TABLE ShipmentEvent (
    eventId          INTEGER PRIMARY KEY AUTOINCREMENT,
    shipmentId       INTEGER NOT NULL,
    providerEventRef VARCHAR(255) NOT NULL DEFAULT '',
    eventStatus      VARCHAR(50)  NOT NULL,
    occurredAt       VARCHAR(50)  NOT NULL,
    FOREIGN KEY (shipmentId) REFERENCES Shipment(shipmentId)
);
