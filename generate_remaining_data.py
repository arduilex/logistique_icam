#!/usr/bin/env python3
"""Génère les données complètes pour la base de données"""

import sqlite3
import random
from datetime import datetime, timedelta

def generate_remaining_orders_and_transactions():
    """Génère les 50 commandes restantes avec leurs articles et transactions"""
    
    conn = sqlite3.connect('/home/alex/dev/icam/icamerce_dev/stock/db.sqlite3')
    cursor = conn.cursor()
    
    # Fournisseurs et clients
    suppliers = [
        'SCHNEIDER ELECTRIC', 'SIEMENS', 'FESTO', 'PARKER HANNIFIN', 'SKF',
        'SICK', 'PHOENIX CONTACT', 'LEGRIS', 'BOSCH REXROTH', 'ABB'
    ]
    
    customers = [
        'RENAULT TRUCKS', 'AIRBUS', 'SANOFI', 'MICHELIN', 'TOTAL ENERGIES',
        'ARCELORMITTAL', 'SAFRAN', 'THALES', 'PEUGEOT', 'DANONE'
    ]
    
    # Dates de commandes réparties sur 6 mois
    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 6, 30)
    
    order_id = 10  # Commencer après les 9 commandes de janvier
    achat_counter = 6
    vente_counter = 5
    
    # Générer 50 commandes supplémentaires
    for i in range(50):
        # Date aléatoire entre février et juin
        random_days = random.randint(0, (end_date - start_date).days)
        order_date = start_date + timedelta(days=random_days)
        
        # Type de commande (60% ventes, 40% achats)
        order_type = 'OUT' if random.random() < 0.6 else 'IN'
        
        if order_type == 'IN':
            order_number = f'ACH-2025-{str(achat_counter).zfill(3)}'
            supplier_customer = random.choice(suppliers)
            notes = 'Réapprovisionnement'
            achat_counter += 1
        else:
            order_number = f'VTE-2025-{str(vente_counter).zfill(3)}'
            supplier_customer = random.choice(customers)
            notes = 'Commande client'
            vente_counter += 1
        
        # Statut (pour les 5 dernières commandes, on mettra des statuts variés plus tard)
        status = 'DELIVERED'
        
        # Insérer la commande
        cursor.execute("""
            INSERT INTO inventory_order (order_number, order_type, status, supplier_customer, order_date, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_number, order_type, status, supplier_customer, 
              order_date.strftime('%Y-%m-%d %H:%M:%S'), notes,
              order_date.strftime('%Y-%m-%d %H:%M:%S'), order_date.strftime('%Y-%m-%d %H:%M:%S')))
        
        order_id += 1
        
        # Générer 2-4 articles par commande
        num_items = random.randint(2, 4)
        products = random.sample(range(1, 46), num_items)  # Sélectionner des produits aléatoires
        
        for product_id in products:
            # Récupérer le prix du produit
            cursor.execute("SELECT price FROM inventory_product WHERE id = ?", (product_id,))
            base_price = cursor.fetchone()[0]
            
            if order_type == 'IN':
                # Achat: quantité importante, prix de base
                quantity = random.randint(10, 50)
                unit_price = base_price
                transaction_quantity = quantity
            else:
                # Vente: quantité modérée, prix avec marge
                quantity = random.randint(3, 20)
                unit_price = base_price * 1.2  # Marge de 20%
                transaction_quantity = quantity
            
            # Insérer l'article de commande
            cursor.execute("""
                INSERT INTO inventory_orderitem (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (order_id - 1, product_id, quantity, unit_price))
            
            # Insérer la transaction correspondante
            cursor.execute("""
                INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product_id, order_type, transaction_quantity, unit_price,
                  f"{'Achat' if order_type == 'IN' else 'Vente'} - {order_number}",
                  order_date.strftime('%Y-%m-%d %H:%M:%S')))
    
    # Quelques ajustements d'inventaire
    adjustment_dates = [
        datetime(2025, 2, 15), datetime(2025, 3, 20), datetime(2025, 4, 10),
        datetime(2025, 5, 5), datetime(2025, 6, 1)
    ]
    
    for adj_date in adjustment_dates:
        product_id = random.randint(1, 45)
        adjustment = random.randint(-8, 12)
        
        cursor.execute("""
            INSERT INTO inventory_transaction (product_id, transaction_type, quantity, unit_price, notes, timestamp)
            VALUES (?, 'ADJUSTMENT', ?, NULL, 'Correction inventaire', ?)
        """, (product_id, adjustment, adj_date.strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    print("✅ 50 commandes supplémentaires générées avec succès")

def update_last_orders_status():
    """Met à jour les statuts des 5 dernières commandes"""
    conn = sqlite3.connect('/home/alex/dev/icam/icamerce_dev/stock/db.sqlite3')
    cursor = conn.cursor()
    
    # Récupérer les 5 dernières commandes
    cursor.execute("SELECT id FROM inventory_order ORDER BY id DESC LIMIT 5")
    last_orders = [row[0] for row in cursor.fetchall()]
    
    statuses = ['PENDING', 'CONFIRMED', 'CANCELLED', 'PENDING', 'CONFIRMED']
    
    for i, order_id in enumerate(last_orders):
        cursor.execute("UPDATE inventory_order SET status = ? WHERE id = ?", (statuses[i], order_id))
    
    conn.commit()
    conn.close()
    print("✅ Statuts des 5 dernières commandes mis à jour")

def calculate_final_stock():
    """Calcule les stocks finaux basés sur toutes les transactions"""
    conn = sqlite3.connect('/home/alex/dev/icam/icamerce_dev/stock/db.sqlite3')
    cursor = conn.cursor()
    
    # Remettre tous les stocks à zéro
    cursor.execute("UPDATE inventory_product SET quantity = 0")
    
    # Calculer le stock final pour chaque produit
    cursor.execute("""
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
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Stocks finaux calculés")

def main():
    print("🚀 Génération des données complètes...")
    
    # Générer les commandes restantes
    generate_remaining_orders_and_transactions()
    
    # Mettre à jour les statuts des dernières commandes
    update_last_orders_status()
    
    # Calculer les stocks finaux
    calculate_final_stock()
    
    # Statistiques finales
    conn = sqlite3.connect('/home/alex/dev/icam/icamerce_dev/stock/db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM inventory_product")
    nb_products = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM inventory_order")
    nb_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM inventory_orderitem")
    nb_items = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM inventory_transaction")
    nb_transactions = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 STATISTIQUES FINALES:")
    print(f"   • {nb_products} produits")
    print(f"   • {nb_orders} commandes") 
    print(f"   • {nb_items} articles de commande")
    print(f"   • {nb_transactions} transactions")
    print(f"\n🎉 Base de données complète générée avec succès !")

if __name__ == "__main__":
    main()