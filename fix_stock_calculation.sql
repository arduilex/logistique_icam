-- Script pour recalculer correctement les stocks finaux

-- Remettre tous les stocks à zéro
UPDATE inventory_product SET quantity = 0;

-- Calculer le stock final pour chaque produit basé sur toutes les transactions
UPDATE inventory_product 
SET quantity = (
    SELECT COALESCE(
        SUM(
            CASE 
                WHEN t.transaction_type = 'IN' THEN t.quantity
                WHEN t.transaction_type = 'OUT' THEN -t.quantity
                WHEN t.transaction_type = 'ADJUSTMENT' THEN t.quantity
                ELSE 0
            END
        ), 0
    )
    FROM inventory_transaction t 
    WHERE t.product_id = inventory_product.id
);

-- Vérifier les résultats
SELECT name, quantity as stock_final FROM inventory_product ORDER BY id;