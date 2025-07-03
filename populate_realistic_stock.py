#!/usr/bin/env python
"""Script pour créer des données avec variations de stock réalistes entre janvier et juin 2025"""

from decimal import Decimal
import random
from datetime import datetime, timedelta
from inventory.models import Product, Order, OrderItem, Transaction

def clear_database():
    """Vide la base de données"""
    print("🗑️  Nettoyage de la base de données...")
    Transaction.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    print("✅ Base de données nettoyée")

def create_products():
    """Crée une sélection de produits avec stocks initiaux"""
    print("📦 Création des produits...")
    
    products_data = [
        {"name": "Moteur électrique 3kW", "reference": "MOT-3KW-001", "price": 450.00, "initial_stock": 50, "min_stock": 10},
        {"name": "Capteur de température Pt100", "reference": "CAPT-PT100-01", "price": 125.00, "initial_stock": 80, "min_stock": 15},
        {"name": "Vérin pneumatique Ø32", "reference": "VER-32-50", "price": 68.00, "initial_stock": 120, "min_stock": 25},
        {"name": "Contacteur 25A", "reference": "CONT-25A-001", "price": 32.80, "initial_stock": 200, "min_stock": 40},
        {"name": "Roulement à billes 6204", "reference": "ROUL-6204-2RS", "price": 12.50, "initial_stock": 300, "min_stock": 50},
        {"name": "Électrovanne 5/2", "reference": "EV-5-2-G14", "price": 95.00, "initial_stock": 60, "min_stock": 12},
        {"name": "Transformateur 220V/24V", "reference": "TRANS-220-24", "price": 89.50, "initial_stock": 90, "min_stock": 20},
        {"name": "Projecteur LED 50W", "reference": "PROJ-LED-50W", "price": 89.00, "initial_stock": 75, "min_stock": 15},
        {"name": "Détecteur de proximité", "reference": "DET-PROX-IND", "price": 35.00, "initial_stock": 150, "min_stock": 30},
        {"name": "Vanne à boisseau DN25", "reference": "VAN-BOIS-25", "price": 45.00, "initial_stock": 100, "min_stock": 20},
    ]
    
    products = []
    for data in products_data:
        product = Product.objects.create(
            name=data["name"],
            reference=data["reference"],
            description=f"Description du produit {data['name']}",
            quantity=data["initial_stock"],
            price=Decimal(str(data["price"])),
            min_stock_level=data["min_stock"],
            created_at=datetime(2024, 12, 15)  # Créé en décembre 2024
        )
        products.append(product)
        print(f"  ✓ {product.name} - Stock initial: {data['initial_stock']}")
    
    print(f"✅ {len(products)} produits créés")
    return products

def generate_realistic_transactions(products):
    """Génère des transactions réalistes entre janvier et juin 2025"""
    print("📈 Génération des transactions avec variations réalistes...")
    
    # Période de janvier à juin 2025
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 6, 30)
    
    # Fournisseurs et clients
    suppliers = ["SCHNEIDER", "SIEMENS", "FESTO", "PARKER", "SKF"]
    customers = ["RENAULT", "AIRBUS", "SANOFI", "MICHELIN", "TOTAL"]
    
    # Compteurs pour les numéros de commande
    achat_counter = 1
    vente_counter = 1
    
    # Pour chaque produit, générer un historique réaliste
    for product in products:
        print(f"  📊 Génération pour {product.name}")
        
        # Stock de départ (on remet à zéro pour recalculer)
        current_stock = product.quantity
        product.quantity = 0
        product.save()
        
        # Première transaction: stock initial le 1er janvier
        Transaction.objects.create(
            product=product,
            transaction_type='IN',
            quantity=current_stock,
            unit_price=product.price,
            notes="Stock initial 2025",
            timestamp=start_date
        )
        product.quantity = current_stock
        product.save()
        
        # Générer des transactions sur 6 mois
        current_date = start_date
        
        while current_date <= end_date:
            # Probabilité d'avoir une transaction ce jour-là
            if random.random() < 0.15:  # 15% de chance par jour
                
                # Type de transaction basé sur le niveau de stock
                if product.quantity <= product.min_stock_level * 1.5:
                    # Stock faible -> plus de chances d'achat
                    transaction_type = 'IN' if random.random() < 0.8 else 'OUT'
                elif product.quantity >= product.min_stock_level * 4:
                    # Stock élevé -> plus de chances de vente
                    transaction_type = 'OUT' if random.random() < 0.7 else 'IN'
                else:
                    # Stock normal -> équilibré
                    transaction_type = random.choice(['IN', 'OUT'])
                
                if transaction_type == 'IN':
                    # Entrée de stock (achat)
                    quantity = random.randint(10, 50)
                    
                    # Créer une commande d'achat
                    order = Order.objects.create(
                        order_number=f"ACH-2025-{str(achat_counter).zfill(3)}",
                        order_type='IN',
                        status='DELIVERED',
                        supplier_customer=random.choice(suppliers),
                        order_date=current_date,
                        notes="Réapprovisionnement"
                    )
                    achat_counter += 1
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price
                    )
                    
                    Transaction.objects.create(
                        product=product,
                        transaction_type='IN',
                        quantity=quantity,
                        unit_price=product.price,
                        notes=f"Achat - {order.order_number}",
                        timestamp=current_date
                    )
                    
                    # Mettre à jour le stock
                    product.quantity += quantity
                    product.save()
                    
                elif transaction_type == 'OUT':
                    # Sortie de stock (vente) - s'assurer de ne pas descendre sous 0
                    max_quantity = min(product.quantity, random.randint(5, 30))
                    if max_quantity > 0:
                        quantity = random.randint(1, max_quantity)
                        
                        # Créer une commande de vente
                        order = Order.objects.create(
                            order_number=f"VTE-2025-{str(vente_counter).zfill(3)}",
                            order_type='OUT',
                            status='DELIVERED',
                            supplier_customer=random.choice(customers),
                            order_date=current_date,
                            notes="Vente client"
                        )
                        vente_counter += 1
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            unit_price=product.price * Decimal('1.2')  # Marge
                        )
                        
                        Transaction.objects.create(
                            product=product,
                            transaction_type='OUT',
                            quantity=quantity,  # Positif dans Transaction, la logique de soustraction est dans save()
                            unit_price=product.price * Decimal('1.2'),
                            notes=f"Vente - {order.order_number}",
                            timestamp=current_date
                        )
                        
                        # Mettre à jour le stock
                        product.quantity -= quantity
                        product.save()
            
            # Avancer d'un jour
            current_date += timedelta(days=1)
        
        print(f"    ✓ Stock final: {product.quantity}")

def add_some_adjustments(products):
    """Ajoute quelques ajustements d'inventaire"""
    print("⚖️  Ajout d'ajustements d'inventaire...")
    
    for _ in range(8):
        product = random.choice(products)
        # Ajustement entre -10 et +15, mais sans jamais faire descendre sous 0
        max_negative = -min(10, product.quantity)
        adjustment = random.randint(max_negative, 15)
        
        if adjustment != 0:
            Transaction.objects.create(
                product=product,
                transaction_type='ADJUSTMENT',
                quantity=adjustment,
                unit_price=None,
                notes="Correction inventaire",
                timestamp=datetime(2025, random.randint(2, 5), random.randint(1, 28))
            )
            
            # Mettre à jour le stock
            product.quantity += adjustment
            product.save()
            
            print(f"  ✓ Ajustement {product.name}: {adjustment:+d} (nouveau stock: {product.quantity})")

def main():
    """Fonction principale"""
    print("🏭 GÉNÉRATION DE DONNÉES RÉALISTES - JANVIER À JUIN 2025")
    print("=" * 65)
    
    # Vider la base
    clear_database()
    
    # Créer les produits
    products = create_products()
    
    # Générer les transactions réalistes
    generate_realistic_transactions(products)
    
    # Ajouter quelques ajustements
    add_some_adjustments(products)
    
    print("\n" + "=" * 65)
    print("🎉 DONNÉES RÉALISTES GÉNÉRÉES AVEC SUCCÈS !")
    print(f"📊 Statistiques finales:")
    print(f"   • {Product.objects.count()} produits")
    print(f"   • {Order.objects.count()} commandes")
    print(f"   • {OrderItem.objects.count()} articles de commande")
    print(f"   • {Transaction.objects.count()} transactions")
    
    print(f"\n📈 État des stocks:")
    for product in products:
        status = "🔴" if product.quantity == 0 else "🟡" if product.quantity <= product.min_stock_level else "🟢"
        print(f"   {status} {product.name}: {product.quantity} unités")
    
    print("\n🌐 Les graphiques d'évolution devraient maintenant montrer des variations réalistes !")

if __name__ == "__main__":
    main()