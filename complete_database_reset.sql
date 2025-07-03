-- Script SQL complet pour 45 produits, 60 commandes avec articles et transactions
-- Période : janvier à juin 2025

-- === NETTOYAGE COMPLET ===
DELETE FROM inventory_transaction;
DELETE FROM inventory_orderitem;
DELETE FROM inventory_order;
DELETE FROM inventory_product;
DELETE FROM sqlite_sequence WHERE name IN ('inventory_product', 'inventory_order', 'inventory_orderitem', 'inventory_transaction');

-- === CRÉATION DE 45 PRODUITS ===
INSERT INTO inventory_product (name, reference, description, quantity, price, min_stock_level, created_at, updated_at) VALUES
-- Équipements électriques (10 produits)
('Moteur électrique 3kW', 'MOT-3KW-001', 'Moteur triphasé 3000 tr/min', 0, 450.00, 10, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Moteur électrique 5.5kW', 'MOT-5K5-001', 'Moteur triphasé 1500 tr/min', 0, 680.00, 8, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Transformateur 220V/24V', 'TRANS-220-24', 'Transformateur de sécurité 100VA', 0, 89.50, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Transformateur 380V/110V', 'TRANS-380-110', 'Transformateur de sécurité 250VA', 0, 145.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Contacteur 25A', 'CONT-25A-001', 'Contacteur triphasé 25A bobine 24V', 0, 32.80, 40, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Contacteur 40A', 'CONT-40A-001', 'Contacteur triphasé 40A bobine 230V', 0, 48.50, 30, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Variateur de fréquence 2.2kW', 'VAR-2K2-001', 'Variateur vectoriel IP20', 0, 520.00, 5, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Variateur de fréquence 5.5kW', 'VAR-5K5-001', 'Variateur vectoriel IP20', 0, 780.00, 3, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Relais thermique 16-25A', 'REL-TH-16-25', 'Protection surcharge moteur', 0, 45.60, 25, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Relais thermique 32-50A', 'REL-TH-32-50', 'Protection surcharge moteur', 0, 62.80, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),

-- Capteurs et instrumentation (10 produits)
('Capteur température Pt100', 'CAPT-PT100-01', 'Sonde Pt100 3 fils, -50°C à +200°C', 0, 125.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Capteur température thermocouple K', 'CAPT-TC-K-01', 'Thermocouple type K 0-1000°C', 0, 89.00, 12, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Capteur de pression 0-10 bar', 'CAPT-P-10B', 'Transmetteur 4-20mA', 0, 156.00, 8, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Capteur de pression 0-25 bar', 'CAPT-P-25B', 'Transmetteur 4-20mA', 0, 178.00, 6, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Débitmètre électromagnétique DN50', 'DEB-MAG-50', 'Débitmètre haute précision', 0, 1250.00, 2, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Débitmètre vortex DN25', 'DEB-VOR-25', 'Débitmètre pour gaz et liquides', 0, 890.00, 3, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Manomètre glycérine 0-16 bar', 'MANO-GLY-16', 'Cadran 100mm avec amortisseur', 0, 28.50, 30, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Manomètre digital 0-25 bar', 'MANO-DIG-25', 'Affichage LCD avec alarmes', 0, 165.00, 10, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Thermomètre à cadran', 'THERMO-CAD-01', '0-120°C, tige 100mm', 0, 18.90, 25, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Thermomètre digital', 'THERMO-DIG-01', 'Sonde déportée -50/+300°C', 0, 45.80, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),

-- Pneumatique (8 produits)
('Vérin pneumatique Ø32 course 50mm', 'VER-32-50', 'Vérin double effet ISO 6432', 0, 68.00, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Vérin pneumatique Ø63 course 100mm', 'VER-63-100', 'Vérin double effet ISO 15552', 0, 125.00, 12, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Électrovanne 5/2 G1/4', 'EV-5-2-G14', 'Électrovanne bistable 24VDC', 0, 95.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Électrovanne 3/2 G1/8', 'EV-3-2-G18', 'Électrovanne monostable 24VDC', 0, 65.00, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Régulateur de pression G1/4', 'REG-P-G14', '0-10 bar avec manomètre', 0, 42.50, 18, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Régulateur de pression G1/2', 'REG-P-G12', '0-16 bar avec manomètre', 0, 58.00, 12, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Filtre à air G1/2', 'FILT-AIR-G12', 'Filtre coalesceur 5µm', 0, 35.80, 25, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Raccord rapide DN6', 'RACC-RAP-6', 'Raccord pneumatique laiton', 0, 8.50, 100, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),

-- Hydraulique (5 produits)
('Pompe hydraulique 2.2kW', 'POMP-HYD-2K2', 'Pompe à engrenages externe', 0, 890.00, 3, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Distributeur hydraulique 4/3', 'DIST-4-3-001', 'Centre fermé NG6', 0, 245.00, 6, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Accumulateur hydraulique 1L', 'ACCU-HYD-1L', 'À membrane 210 bar', 0, 156.00, 8, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Filtre hydraulique retour', 'FILT-HYD-RET', 'Élément 10µm G1/2', 0, 78.50, 12, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Flexible hydraulique DN12', 'FLEX-HYD-12', '2 tresses métalliques 350 bar', 0, 45.00, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),

-- Mécanique (7 produits)
('Roulement à billes 6204 2RS', 'ROUL-6204-2RS', 'Roulement étanche Ø20x47x14', 0, 12.50, 80, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Roulement à rouleaux 22210', 'ROUL-22210', 'Roulement conique Ø50x90x23', 0, 28.90, 40, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Courroie trapézoïdale SPA 1250', 'COUR-SPA-1250', 'Courroie section SPA', 0, 15.80, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Courroie synchrone 8M-1200', 'COUR-8M-1200', 'Courroie dentée largeur 20mm', 0, 24.50, 15, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Réducteur à vis sans fin i=30', 'RED-VS-30', 'Réducteur couple 150Nm', 0, 320.00, 4, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Joint torique NBR 20x3', 'JOINT-OR-20-3', 'Joint NBR 70 shores', 0, 2.50, 200, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Graisse haute température', 'GRAI-HT-001', 'Cartouche 400g -20°C/+150°C', 0, 24.90, 25, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),

-- Automatisme et sécurité (5 produits)
('Automate programmable 16E/12S', 'AUTO-16-12', 'CPU compacte Ethernet', 0, 650.00, 3, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Détecteur de proximité inductif', 'DET-PROX-IND', 'M18 PNP NO 2 fils', 0, 35.00, 50, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Fin de course IP67', 'FDC-IP67-001', 'Corps métallique 2NO+2NF', 0, 28.00, 30, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Arrêt d\urgence Ø40 rouge', 'AU-40-ROUGE', 'Bouton coup de poing 1NC', 0, 18.50, 40, '2024-12-15 10:00:00', '2025-06-30 16:30:00'),
('Projecteur LED 50W IP65', 'PROJ-LED-50W', '6500K 5000 lumens', 0, 89.00, 20, '2024-12-15 10:00:00', '2025-06-30 16:30:00');

-- === STOCKS INITIAUX (1er JANVIER 2025) ===
INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(1, 'IN', 50, 450.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(2, 'IN', 35, 680.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(3, 'IN', 120, 89.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(4, 'IN', 80, 145.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(5, 'IN', 200, 32.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(6, 'IN', 150, 48.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(7, 'IN', 25, 520.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(8, 'IN', 15, 780.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(9, 'IN', 100, 45.60, 'Stock initial 2025', '2025-01-01 08:00:00'),
(10, 'IN', 80, 62.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(11, 'IN', 75, 125.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(12, 'IN', 60, 89.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(13, 'IN', 40, 156.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(14, 'IN', 30, 178.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(15, 'IN', 8, 1250.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(16, 'IN', 12, 890.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(17, 'IN', 150, 28.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(18, 'IN', 50, 165.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(19, 'IN', 100, 18.90, 'Stock initial 2025', '2025-01-01 08:00:00'),
(20, 'IN', 75, 45.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(21, 'IN', 80, 68.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(22, 'IN', 48, 125.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(23, 'IN', 75, 95.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(24, 'IN', 100, 65.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(25, 'IN', 90, 42.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(26, 'IN', 60, 58.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(27, 'IN', 125, 35.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(28, 'IN', 500, 8.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(29, 'IN', 15, 890.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(30, 'IN', 30, 245.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(31, 'IN', 40, 156.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(32, 'IN', 60, 78.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(33, 'IN', 75, 45.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(34, 'IN', 400, 12.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(35, 'IN', 200, 28.90, 'Stock initial 2025', '2025-01-01 08:00:00'),
(36, 'IN', 100, 15.80, 'Stock initial 2025', '2025-01-01 08:00:00'),
(37, 'IN', 75, 24.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(38, 'IN', 20, 320.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(39, 'IN', 800, 2.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(40, 'IN', 125, 24.90, 'Stock initial 2025', '2025-01-01 08:00:00'),
(41, 'IN', 15, 650.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(42, 'IN', 250, 35.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(43, 'IN', 150, 28.00, 'Stock initial 2025', '2025-01-01 08:00:00'),
(44, 'IN', 200, 18.50, 'Stock initial 2025', '2025-01-01 08:00:00'),
(45, 'IN', 100, 89.00, 'Stock initial 2025', '2025-01-01 08:00:00');

-- === COMMANDES ET TRANSACTIONS JANVIER 2025 ===

-- Commande ACH-2025-001 (3 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-001', 'IN', 'DELIVERED', 'SCHNEIDER ELECTRIC', '2025-01-03 09:30:00', 'Réapprovisionnement équipements électriques', '2025-01-03 09:30:00', '2025-01-03 09:30:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 20, 450.00),
(1, 5, 50, 32.80),
(1, 9, 30, 45.60);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(1, 'IN', 20, 450.00, 'Achat - ACH-2025-001', '2025-01-03 09:30:00'),
(5, 'IN', 50, 32.80, 'Achat - ACH-2025-001', '2025-01-03 09:30:00'),
(9, 'IN', 30, 45.60, 'Achat - ACH-2025-001', '2025-01-03 09:30:00');

-- Commande VTE-2025-001 (5 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-001', 'OUT', 'DELIVERED', 'RENAULT TRUCKS', '2025-01-05 14:15:00', 'Commande client', '2025-01-05 14:15:00', '2025-01-05 14:15:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(2, 1, 8, 540.00),
(2, 21, 15, 81.60),
(2, 34, 25, 15.00);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(1, 'OUT', 8, 540.00, 'Vente - VTE-2025-001', '2025-01-05 14:15:00'),
(21, 'OUT', 15, 81.60, 'Vente - VTE-2025-001', '2025-01-05 14:15:00'),
(34, 'OUT', 25, 15.00, 'Vente - VTE-2025-001', '2025-01-05 14:15:00');

-- Commande ACH-2025-002 (8 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-002', 'IN', 'DELIVERED', 'SIEMENS', '2025-01-08 11:45:00', 'Capteurs et instrumentation', '2025-01-08 11:45:00', '2025-01-08 11:45:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(3, 11, 25, 125.00),
(3, 13, 15, 156.00),
(3, 18, 20, 165.00);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(11, 'IN', 25, 125.00, 'Achat - ACH-2025-002', '2025-01-08 11:45:00'),
(13, 'IN', 15, 156.00, 'Achat - ACH-2025-002', '2025-01-08 11:45:00'),
(18, 'IN', 20, 165.00, 'Achat - ACH-2025-002', '2025-01-08 11:45:00');

-- Commande VTE-2025-002 (10 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-002', 'OUT', 'DELIVERED', 'AIRBUS', '2025-01-10 16:20:00', 'Commande client', '2025-01-10 16:20:00', '2025-01-10 16:20:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(4, 11, 12, 150.00),
(4, 42, 30, 42.00),
(4, 45, 8, 106.80);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(11, 'OUT', 12, 150.00, 'Vente - VTE-2025-002', '2025-01-10 16:20:00'),
(42, 'OUT', 30, 42.00, 'Vente - VTE-2025-002', '2025-01-10 16:20:00'),
(45, 'OUT', 8, 106.80, 'Vente - VTE-2025-002', '2025-01-10 16:20:00');

-- Commande ACH-2025-003 (15 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-003', 'IN', 'DELIVERED', 'FESTO', '2025-01-15 10:00:00', 'Équipements pneumatiques', '2025-01-15 10:00:00', '2025-01-15 10:00:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(5, 21, 30, 68.00),
(5, 23, 25, 95.00),
(5, 25, 40, 42.50);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(21, 'IN', 30, 68.00, 'Achat - ACH-2025-003', '2025-01-15 10:00:00'),
(23, 'IN', 25, 95.00, 'Achat - ACH-2025-003', '2025-01-15 10:00:00'),
(25, 'IN', 40, 42.50, 'Achat - ACH-2025-003', '2025-01-15 10:00:00');

-- Commande VTE-2025-003 (18 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-003', 'OUT', 'DELIVERED', 'MICHELIN', '2025-01-18 13:45:00', 'Commande client', '2025-01-18 13:45:00', '2025-01-18 13:45:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(6, 5, 40, 39.36),
(6, 17, 25, 34.20),
(6, 28, 80, 10.20);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(5, 'OUT', 40, 39.36, 'Vente - VTE-2025-003', '2025-01-18 13:45:00'),
(17, 'OUT', 25, 34.20, 'Vente - VTE-2025-003', '2025-01-18 13:45:00'),
(28, 'OUT', 80, 10.20, 'Vente - VTE-2025-003', '2025-01-18 13:45:00');

-- Commande ACH-2025-004 (22 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-004', 'IN', 'DELIVERED', 'PARKER HANNIFIN', '2025-01-22 15:30:00', 'Équipements hydrauliques', '2025-01-22 15:30:00', '2025-01-22 15:30:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(7, 29, 5, 890.00),
(7, 30, 10, 245.00),
(7, 32, 15, 78.50);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(29, 'IN', 5, 890.00, 'Achat - ACH-2025-004', '2025-01-22 15:30:00'),
(30, 'IN', 10, 245.00, 'Achat - ACH-2025-004', '2025-01-22 15:30:00'),
(32, 'IN', 15, 78.50, 'Achat - ACH-2025-004', '2025-01-22 15:30:00');

-- Commande VTE-2025-004 (25 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('VTE-2025-004', 'OUT', 'DELIVERED', 'SANOFI', '2025-01-25 12:15:00', 'Commande client', '2025-01-25 12:15:00', '2025-01-25 12:15:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(8, 3, 20, 107.40),
(8, 19, 15, 22.68),
(8, 40, 10, 29.88);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(3, 'OUT', 20, 107.40, 'Vente - VTE-2025-004', '2025-01-25 12:15:00'),
(19, 'OUT', 15, 22.68, 'Vente - VTE-2025-004', '2025-01-25 12:15:00'),
(40, 'OUT', 10, 29.88, 'Vente - VTE-2025-004', '2025-01-25 12:15:00');

-- Commande ACH-2025-005 (28 janvier)
INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at) VALUES
('ACH-2025-005', 'IN', 'DELIVERED', 'SKF', '2025-01-28 09:45:00', 'Roulements et mécanique', '2025-01-28 09:45:00', '2025-01-28 09:45:00');

INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price) VALUES
(9, 34, 100, 12.50),
(9, 35, 50, 28.90),
(9, 36, 30, 15.80);

INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp) VALUES
(34, 'IN', 100, 12.50, 'Achat - ACH-2025-005', '2025-01-28 09:45:00'),
(35, 'IN', 50, 28.90, 'Achat - ACH-2025-005', '2025-01-28 09:45:00'),
(36, 'IN', 30, 15.80, 'Achat - ACH-2025-005', '2025-01-28 09:45:00');