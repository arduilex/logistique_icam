-- Script SQL pour réinitialiser la base de données avec des données réalistes
-- Variations de stock entre janvier et juin 2025

-- Vider les tables existantes
DELETE FROM inventory_transaction;
DELETE FROM inventory_orderitem;
DELETE FROM inventory_order;
DELETE FROM inventory_product;

-- Réinitialiser les séquences
DELETE FROM sqlite_sequence WHERE name IN ('inventory_product', 'inventory_order', 'inventory_orderitem', 'inventory_transaction');

-- Créer des produits avec stocks initiaux
INSERT INTO inventory_product (name, reference, description, quantity, price, min_stock_level, created_at, updated_at) VALUES
('Moteur électrique 3kW', 'MOT-3KW-001', 'Moteur triphasé industriel', 45, 450.00, 10, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Capteur température Pt100', 'CAPT-PT100-01', 'Sonde de température industrielle', 62, 125.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Vérin pneumatique Ø32', 'VER-32-50', 'Vérin double effet 50mm course', 88, 68.00, 25, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Contacteur 25A', 'CONT-25A-001', 'Contacteur triphasé 25A', 156, 32.80, 40, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Roulement à billes 6204', 'ROUL-6204-2RS', 'Roulement étanche 20x47x14', 234, 12.50, 50, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Électrovanne 5/2', 'EV-5-2-G14', 'Électrovanne pneumatique bistable', 38, 95.00, 12, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Transformateur 220V/24V', 'TRANS-220-24', 'Transformateur de sécurité 100VA', 71, 89.50, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Projecteur LED 50W', 'PROJ-LED-50W', 'Éclairage industriel IP65', 52, 89.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Détecteur de proximité', 'DET-PROX-IND', 'Détecteur inductif M18 PNP', 103, 35.00, 30, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Vanne à boisseau DN25', 'VAN-BOIS-25', 'Vanne sphérique inox 316', 67, 45.00, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00');

-- Créer des commandes et transactions avec variations réalistes

-- === JANVIER 2025 ===

-- Stock initial (1er janvier)
INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(1, 'IN', 50, 450.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(2, 'IN', 80, 125.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(3, 'IN', 120, 68.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(4, 'IN', 200, 32.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(5, 'IN', 300, 12.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(6, 'IN', 60, 95.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(7, 'IN', 90, 89.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(8, 'IN', 75, 89.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(9, 'IN', 150, 35.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(10, 'IN', 100, 45.00, 'Stock initial 2025', '2025-01-01 08:00:00');

-- Janvier - Quelques ventes et achats
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-001', 'OUT', 'DELIVERED', 'RENAULT TRUCKS', '2025-01-05 10:30:00', 'Vente client', '2025-01-05 10:30:00', '2025-01-05 10:30:00'),
('ACH-2025-001', 'IN', 'DELIVERED', 'SCHNEIDER', '2025-01-12 14:15:00', 'Réapprovisionnement', '2025-01-12 14:15:00', '2025-01-12 14:15:00'),
('VTE-2025-002', 'OUT', 'DELIVERED', 'AIRBUS', '2025-01-18 09:45:00', 'Vente client', '2025-01-18 09:45:00', '2025-01-18 09:45:00'),
('VTE-2025-003', 'OUT', 'DELIVERED', 'MICHELIN', '2025-01-25 16:20:00', 'Vente client', '2025-01-25 16:20:00', '2025-01-25 16:20:00');

-- Transactions janvier
INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Vente du 5 janvier
(1, 'OUT', 5, 540.00, 'Vente - VTE-2025-001', '2025-01-05 10:30:00'),
(3, 'OUT', 12, 81.60, 'Vente - VTE-2025-001', '2025-01-05 10:30:00'),
-- Achat du 12 janvier
(1, 'IN', 20, 450.00, 'Achat - ACH-2025-001', '2025-01-12 14:15:00'),
(6, 'IN', 15, 95.00, 'Achat - ACH-2025-001', '2025-01-12 14:15:00'),
-- Vente du 18 janvier
(2, 'OUT', 8, 150.00, 'Vente - VTE-2025-002', '2025-01-18 09:45:00'),
(9, 'OUT', 25, 42.00, 'Vente - VTE-2025-002', '2025-01-18 09:45:00'),
-- Vente du 25 janvier
(4, 'OUT', 30, 39.36, 'Vente - VTE-2025-003', '2025-01-25 16:20:00'),
(5, 'OUT', 45, 15.00, 'Vente - VTE-2025-003', '2025-01-25 16:20:00');

-- === FÉVRIER 2025 ===

INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-002', 'IN', 'DELIVERED', 'SIEMENS', '2025-02-03 11:00:00', 'Réapprovisionnement', '2025-02-03 11:00:00', '2025-02-03 11:00:00'),
('VTE-2025-004', 'OUT', 'DELIVERED', 'SANOFI', '2025-02-08 13:30:00', 'Vente client', '2025-02-08 13:30:00', '2025-02-08 13:30:00'),
('VTE-2025-005', 'OUT', 'DELIVERED', 'TOTAL', '2025-02-15 10:15:00', 'Vente client', '2025-02-15 10:15:00', '2025-02-15 10:15:00'),
('ACH-2025-003', 'IN', 'DELIVERED', 'FESTO', '2025-02-22 15:45:00', 'Réapprovisionnement', '2025-02-22 15:45:00', '2025-02-22 15:45:00');

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Achat du 3 février
(2, 'IN', 25, 125.00, 'Achat - ACH-2025-002', '2025-02-03 11:00:00'),
(7, 'IN', 18, 89.50, 'Achat - ACH-2025-002', '2025-02-03 11:00:00'),
-- Vente du 8 février
(8, 'OUT', 15, 106.80, 'Vente - VTE-2025-004', '2025-02-08 13:30:00'),
(10, 'OUT', 22, 54.00, 'Vente - VTE-2025-004', '2025-02-08 13:30:00'),
-- Vente du 15 février
(3, 'OUT', 18, 81.60, 'Vente - VTE-2025-005', '2025-02-15 10:15:00'),
(4, 'OUT', 35, 39.36, 'Vente - VTE-2025-005', '2025-02-15 10:15:00'),
-- Achat du 22 février
(3, 'IN', 30, 68.00, 'Achat - ACH-2025-003', '2025-02-22 15:45:00'),
(6, 'IN', 12, 95.00, 'Achat - ACH-2025-003', '2025-02-22 15:45:00');

-- === MARS 2025 ===

INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-006', 'OUT', 'DELIVERED', 'RENAULT', '2025-03-05 09:20:00', 'Vente client', '2025-03-05 09:20:00', '2025-03-05 09:20:00'),
('VTE-2025-007', 'OUT', 'DELIVERED', 'AIRBUS', '2025-03-12 14:40:00', 'Vente client', '2025-03-12 14:40:00', '2025-03-12 14:40:00'),
('ACH-2025-004', 'IN', 'DELIVERED', 'PARKER', '2025-03-18 11:25:00', 'Réapprovisionnement', '2025-03-18 11:25:00', '2025-03-18 11:25:00'),
('VTE-2025-008', 'OUT', 'DELIVERED', 'MICHELIN', '2025-03-25 16:00:00', 'Vente client', '2025-03-25 16:00:00', '2025-03-25 16:00:00');

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Vente du 5 mars
(5, 'OUT', 55, 15.00, 'Vente - VTE-2025-006', '2025-03-05 09:20:00'),
(9, 'OUT', 30, 42.00, 'Vente - VTE-2025-006', '2025-03-05 09:20:00'),
-- Vente du 12 mars
(1, 'OUT', 8, 540.00, 'Vente - VTE-2025-007', '2025-03-12 14:40:00'),
(7, 'OUT', 12, 107.40, 'Vente - VTE-2025-007', '2025-03-12 14:40:00'),
-- Achat du 18 mars
(5, 'IN', 80, 12.50, 'Achat - ACH-2025-004', '2025-03-18 11:25:00'),
(9, 'IN', 45, 35.00, 'Achat - ACH-2025-004', '2025-03-18 11:25:00'),
-- Vente du 25 mars
(2, 'OUT', 20, 150.00, 'Vente - VTE-2025-008', '2025-03-25 16:00:00'),
(6, 'OUT', 18, 114.00, 'Vente - VTE-2025-008', '2025-03-25 16:00:00');

-- === AVRIL 2025 ===

INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-005', 'IN', 'DELIVERED', 'SKF', '2025-04-02 10:15:00', 'Réapprovisionnement', '2025-04-02 10:15:00', '2025-04-02 10:15:00'),
('VTE-2025-009', 'OUT', 'DELIVERED', 'SANOFI', '2025-04-08 15:20:00', 'Vente client', '2025-04-08 15:20:00', '2025-04-08 15:20:00'),
('VTE-2025-010', 'OUT', 'DELIVERED', 'TOTAL', '2025-04-15 12:45:00', 'Vente client', '2025-04-15 12:45:00', '2025-04-15 12:45:00'),
('ACH-2025-006', 'IN', 'DELIVERED', 'SCHNEIDER', '2025-04-22 09:30:00', 'Réapprovisionnement', '2025-04-22 09:30:00', '2025-04-22 09:30:00');

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Achat du 2 avril
(8, 'IN', 28, 89.00, 'Achat - ACH-2025-005', '2025-04-02 10:15:00'),
(10, 'IN', 35, 45.00, 'Achat - ACH-2025-005', '2025-04-02 10:15:00'),
-- Vente du 8 avril
(4, 'OUT', 28, 39.36, 'Vente - VTE-2025-009', '2025-04-08 15:20:00'),
(8, 'OUT', 20, 106.80, 'Vente - VTE-2025-009', '2025-04-08 15:20:00'),
-- Vente du 15 avril
(3, 'OUT', 25, 81.60, 'Vente - VTE-2025-010', '2025-04-15 12:45:00'),
(10, 'OUT', 18, 54.00, 'Vente - VTE-2025-010', '2025-04-15 12:45:00'),
-- Achat du 22 avril
(1, 'IN', 15, 450.00, 'Achat - ACH-2025-006', '2025-04-22 09:30:00'),
(2, 'IN', 22, 125.00, 'Achat - ACH-2025-006', '2025-04-22 09:30:00');

-- === MAI 2025 ===

INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-011', 'OUT', 'DELIVERED', 'AIRBUS', '2025-05-03 11:30:00', 'Vente client', '2025-05-03 11:30:00', '2025-05-03 11:30:00'),
('VTE-2025-012', 'OUT', 'DELIVERED', 'RENAULT', '2025-05-10 14:15:00', 'Vente client', '2025-05-10 14:15:00', '2025-05-10 14:15:00'),
('ACH-2025-007', 'IN', 'DELIVERED', 'SIEMENS', '2025-05-17 16:00:00', 'Réapprovisionnement', '2025-05-17 16:00:00', '2025-05-17 16:00:00'),
('VTE-2025-013', 'OUT', 'DELIVERED', 'MICHELIN', '2025-05-24 10:45:00', 'Vente client', '2025-05-24 10:45:00', '2025-05-24 10:45:00');

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Vente du 3 mai
(7, 'OUT', 15, 107.40, 'Vente - VTE-2025-011', '2025-05-03 11:30:00'),
(9, 'OUT', 32, 42.00, 'Vente - VTE-2025-011', '2025-05-03 11:30:00'),
-- Vente du 10 mai
(1, 'OUT', 6, 540.00, 'Vente - VTE-2025-012', '2025-05-10 14:15:00'),
(5, 'OUT', 40, 15.00, 'Vente - VTE-2025-012', '2025-05-10 14:15:00'),
-- Achat du 17 mai
(6, 'IN', 25, 95.00, 'Achat - ACH-2025-007', '2025-05-17 16:00:00'),
(7, 'IN', 20, 89.50, 'Achat - ACH-2025-007', '2025-05-17 16:00:00'),
-- Vente du 24 mai
(2, 'OUT', 15, 150.00, 'Vente - VTE-2025-013', '2025-05-24 10:45:00'),
(3, 'OUT', 22, 81.60, 'Vente - VTE-2025-013', '2025-05-24 10:45:00');

-- === JUIN 2025 ===

INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-008', 'IN', 'DELIVERED', 'FESTO', '2025-06-05 13:20:00', 'Réapprovisionnement', '2025-06-05 13:20:00', '2025-06-05 13:20:00'),
('VTE-2025-014', 'OUT', 'DELIVERED', 'SANOFI', '2025-06-12 09:50:00', 'Vente client', '2025-06-12 09:50:00', '2025-06-12 09:50:00'),
('VTE-2025-015', 'OUT', 'DELIVERED', 'TOTAL', '2025-06-18 15:30:00', 'Vente client', '2025-06-18 15:30:00', '2025-06-18 15:30:00'),
('ACH-2025-009', 'IN', 'DELIVERED', 'PARKER', '2025-06-25 11:15:00', 'Réapprovisionnement', '2025-06-25 11:15:00', '2025-06-25 11:15:00');

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
-- Achat du 5 juin
(3, 'IN', 20, 68.00, 'Achat - ACH-2025-008', '2025-06-05 13:20:00'),
(4, 'IN', 40, 32.80, 'Achat - ACH-2025-008', '2025-06-05 13:20:00'),
-- Vente du 12 juin
(8, 'OUT', 18, 106.80, 'Vente - VTE-2025-014', '2025-06-12 09:50:00'),
(10, 'OUT', 25, 54.00, 'Vente - VTE-2025-014', '2025-06-12 09:50:00'),
-- Vente du 18 juin
(4, 'OUT', 32, 39.36, 'Vente - VTE-2025-015', '2025-06-18 15:30:00'),
(9, 'OUT', 28, 42.00, 'Vente - VTE-2025-015', '2025-06-18 15:30:00'),
-- Achat du 25 juin
(1, 'IN', 12, 450.00, 'Achat - ACH-2025-009', '2025-06-25 11:15:00'),
(8, 'IN', 15, 89.00, 'Achat - ACH-2025-009', '2025-06-25 11:15:00');

-- Quelques ajustements d'inventaire
INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(2, 'ADJUSTMENT', -3, NULL, 'Correction inventaire', '2025-02-15 17:00:00'),
(5, 'ADJUSTMENT', 8, NULL, 'Correction inventaire', '2025-03-20 16:30:00'),
(7, 'ADJUSTMENT', -2, NULL, 'Correction inventaire', '2025-04-10 14:45:00'),
(9, 'ADJUSTMENT', 5, NULL, 'Correction inventaire', '2025-05-05 10:20:00'),
(10, 'ADJUSTMENT', -4, NULL, 'Correction inventaire', '2025-06-01 15:15:00');