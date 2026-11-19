#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Seed the Northfield Plant Shop database with sample data."""
import os, sys, sqlite3, datetime
sys.path.insert(0, os.path.dirname(__file__))

DB = os.path.join(os.path.dirname(__file__), 'northfield.db')

def run():
    if os.path.exists(DB):
        os.remove(DB)

    schema = os.path.join(os.path.dirname(__file__), 'schema.sql')
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = OFF')
    with open(schema) as f:
        conn.executescript(f.read())
    conn.execute('PRAGMA foreign_keys = ON')

    now = datetime.datetime.utcnow().isoformat()

    # Staff
    conn.execute("INSERT INTO StaffAccount(email,passwordHash,status,fullName,roleName) VALUES(?,?,?,?,?)",
        ('manager@northfield.vn','$2b$hash','active','Nguyen Van A','MANAGER'))
    conn.execute("INSERT INTO StaffAccount(email,passwordHash,status,fullName,roleName) VALUES(?,?,?,?,?)",
        ('warehouse@northfield.vn','$2b$hash','active','Tran Thi B','WAREHOUSE'))
    conn.execute("INSERT INTO StaffAccount(email,passwordHash,status,fullName,roleName) VALUES(?,?,?,?,?)",
        ('admin@northfield.vn','$2b$hash','active','Le Van C','ADMIN'))

    # Supplier
    conn.execute("INSERT INTO Supplier(supplierName,contactName,phone,email) VALUES(?,?,?,?)",
        ('Green Nursery Co.','Pham Minh D','0901234567','green@nursery.vn'))

    # Products — PlantProduct
    plants = [
        ('Monstera Deliciosa','PLANT','Cây cảnh nhiệt đới dễ trồng, lá to đẹp.',1),
        ('Fiddle Leaf Fig','PLANT','Cây sung violin, lá bóng bẩy ấn tượng.',1),
        ('Snake Plant','PLANT','Cây lưỡi hổ chịu bóng tốt, không cần tưới nhiều.',1),
        ('Pothos Golden','PLANT','Cây trầu bà vàng leo thả, dễ sống mọi điều kiện.',1),
        ('Peace Lily','PLANT','Cây huệ trắng lọc không khí, hoa trắng thanh nhã.',1),
        ('Rubber Plant','PLANT','Cây cao su lá to bóng, thích hợp góc phòng.',1),
    ]
    plant_specs = [
        ('MEDIUM','weekly','EASY',120),
        ('HIGH','weekly','MODERATE',200),
        ('LOW','monthly','EASY',80),
        ('LOW','twice weekly','EASY',60),
        ('LOW','weekly','EASY',70),
        ('MEDIUM','weekly','EASY',180),
    ]
    for (name,cat,desc,pub),(lr,wf,cl,ht) in zip(plants, plant_specs):
        conn.execute("INSERT INTO Product(name,category,description,published,publisherStaffId) VALUES(?,?,?,?,1)",
            (name,cat,desc,pub))
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute("INSERT INTO PlantProduct(productId,lightRequirement,wateringFrequency,careLevel,expectedHeightCm) VALUES(?,?,?,?,?)",
            (pid,lr,wf,cl,ht))

    # Products — AccessoryProduct
    accessories = [
        ('Ceramic Pot 15cm','POT','Chậu gốm màu trắng mịn, đường kính 15cm.',1),
        ('Moisture Meter','TOOL','Đồng hồ đo độ ẩm đất chính xác.',1),
    ]
    acc_specs = [
        ('Ceramic','Ceramic with drainage hole','Place plant directly'),
        ('Plastic','ABS plastic','Insert probe 5cm into soil'),
    ]
    for (name,cat,desc,pub),(at,mat,ui) in zip(accessories, acc_specs):
        conn.execute("INSERT INTO Product(name,category,description,published,publisherStaffId) VALUES(?,?,?,?,1)",
            (name,cat,desc,pub))
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute("INSERT INTO AccessoryProduct(productId,accessoryType,material,usageInstructions) VALUES(?,?,?,?)",
            (pid,at,mat,ui))

    # Variants & initial stock
    variants_data = [
        (1,'NF-MON-S','Small','Plastic Nursery Pot',89000,'active'),
        (1,'NF-MON-M','Medium','Ceramic Pot',149000,'active'),
        (2,'NF-FLF-M','Medium','Terracotta Pot',199000,'active'),
        (3,'NF-SNK-S','Small','Plastic Pot',69000,'active'),
        (3,'NF-SNK-M','Medium','Woven Basket',119000,'active'),
        (4,'NF-POT-S','Small','Hanging Pot',59000,'active'),
        (5,'NF-PLI-M','Medium','White Ceramic',129000,'active'),
        (6,'NF-RUB-M','Medium','Terracotta',169000,'active'),
        (7,'NF-CER-15','Medium','Ceramic',95000,'active'),
        (8,'NF-MST-01','Small','Tool',79000,'active'),
    ]
    for pid,sku,size,opt,price,status in variants_data:
        conn.execute("INSERT INTO ProductVariant(productId,sku,sizeLabel,optionLabel,priceCents,saleStatus) VALUES(?,?,?,?,?,?)",
            (pid,sku,size,opt,price,status))

    # Look up real IDs
    sup_id   = conn.execute('SELECT supplierId FROM Supplier LIMIT 1').fetchone()[0]
    staff_id = conn.execute('SELECT staffId FROM StaffAccount LIMIT 1').fetchone()[0]
    all_vids = [r[0] for r in conn.execute('SELECT variantId FROM ProductVariant ORDER BY variantId').fetchall()]

    # Inventory batches (ready stock) — one batch per variant
    batch_specs = [
        ('GN-2024-001','2024-10-01',20,20,15,2,3),
        ('GN-2024-002','2024-10-01',15,15,12,1,2),
        ('GN-2024-003','2024-10-05',10,10,8,1,1),
        ('GN-2024-004','2024-10-05',25,25,22,2,1),
        ('GN-2024-005','2024-10-05',18,18,15,2,1),
        ('GN-2024-006','2024-10-10',30,30,28,1,1),
        ('GN-2024-007','2024-10-10',12,12,10,1,1),
        ('GN-2024-008','2024-10-10',20,20,18,1,1),
        ('GN-2024-009','2024-10-15',50,50,45,3,2),
        ('GN-2024-010','2024-10-15',30,30,28,1,1),
    ]
    for vid, (ref,arr,recv,doc,ready,care,removed) in zip(all_vids, batch_specs):
        conn.execute("""INSERT INTO InventoryBatch
            (variantId,supplierId,receiverStaffId,supplierBatchRef,arrivalDate,
             receivedQty,supplierDocumentQty,readyQty,underCareQty,removedQty,
             reservedQty,allocatedQty,dispatchedQty,postedAt)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (vid,sup_id,staff_id,ref,arr,recv,doc,ready,care,removed,0,0,0,now))

    # Look up real plant product IDs
    monstera_id = conn.execute("SELECT productId FROM PlantProduct LIMIT 1").fetchone()[0]
    snake_id    = conn.execute("SELECT productId FROM PlantProduct LIMIT 1 OFFSET 2").fetchone()
    snake_id    = snake_id[0] if snake_id else monstera_id

    # Care guides
    guides = [
        (monstera_id,None,'Ánh sáng Monstera','Monstera thích ánh sáng gián tiếp trung bình. Tránh ánh nắng trực tiếp vì có thể làm cháy lá. Đặt cạnh cửa sổ hướng đông hoặc bắc là lý tưởng.','Northfield Care Library',1,'2024-09-01'),
        (monstera_id,None,'Tưới nước Monstera','Tưới khi lớp đất trên cùng khô 3-5cm, thường 1 lần/tuần. Giảm tưới vào mùa đông. Đảm bảo chậu có lỗ thoát nước tốt.','Northfield Care Library',1,'2024-09-01'),
        (snake_id,None,'Chăm sóc Lưỡi Hổ','Snake plant là cây cực kỳ chịu hạn. Tưới 1 lần/tháng vào mùa hè, 1 lần/6 tuần vào mùa đông. Tuyệt đối không để đất ngập nước.','Northfield Care Library',1,'2024-09-01'),
        (None,'PLANT','Đất trồng cây cảnh','Hầu hết cây cảnh phù hợp với hỗn hợp đất thoát nước tốt: 60% đất vườn + 20% perlite + 20% than bùn.','Northfield Care Library',1,'2024-09-15'),
        (None,'PLANT','Phân bón cơ bản','Bón phân hòa tan NPK 20-20-20 pha loãng 1/4 nồng độ, 1 lần/tháng vào mùa tăng trưởng (tháng 3-9). Không bón vào mùa đông.','Northfield Care Library',1,'2024-09-15'),
    ]
    for plantId,catScope,title,content,source,approved,rev in guides:
        conn.execute("INSERT INTO CareGuide(plantProductId,categoryScope,title,content,sourceTitle,approved,revisionDate) VALUES(?,?,?,?,?,?,?)",
            (plantId,catScope,title,content,source,approved,rev))

    # Customer
    conn.execute("INSERT INTO Customer(email,passwordHash,status,fullName,phone,defaultAddress,lightLevel,spaceCm,careEffort) VALUES(?,?,?,?,?,?,?,?,?)",
        ('hien@example.com','$2b$hash','active','Hoang Chi Hien','0912345678','12 Nguyen Hue, Q1, TP.HCM','MEDIUM',30,'EASY'))

    conn.commit()
    conn.close()
    print(f'Database seeded: {DB}')
    print('  - 8 products (6 plants + 2 accessories)')
    print('  - 10 variants with ready stock')
    print('  - 5 approved care guides')
    print('  - 1 customer')

if __name__ == '__main__':
    run()
