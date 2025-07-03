#!/usr/bin/env python
"""Script pour ajouter 100 commandes entre 2023 et 2025 avec des données réalistes"""

import os
import sys
import django
from decimal import Decimal
import random
from datetime import datetime, timedelta

# Configuration Django
sys.path.append('/home/alex/dev/claude-code/stock')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')
django.setup()

from inventory.models import Product, Order, OrderItem, Transaction
from django.utils import timezone

def generate_random_date(start_year=2023, end_year=2025):
    """Génère une date aléatoire entre start_year et end_year"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    
    random_date = start_date + timedelta(days=random_days)
    return timezone.make_aware(random_date)

def create_advanced_sales_data():
    """Crée 100 commandes avec des données réalistes sur 3 ans"""
    
    print("🏭 Création de 100 commandes avancées (2023-2025)")
    print("=" * 60)
    
    # Récupérer tous les produits
    products = list(Product.objects.all())
    if not products:
        print("❌ Aucun produit trouvé ! Veuillez d'abord peupler la base avec des produits.")
        return
    
    print(f"📦 {len(products)} produits disponibles")
    
    # Listes de fournisseurs et clients réalistes
    suppliers = [
        "SCHNEIDER ELECTRIC FRANCE",
        "SIEMENS INDUSTRY",
        "FESTO PNEUMATIC",
        "PARKER HANNIFIN CORP",
        "SKF ROULEMENTS",
        "SICK SENSORS",
        "PHOENIX CONTACT",
        "LEGRIS AUTOMATION",
        "ABB FRANCE",
        "OMRON ELECTRONICS",
        "MITSUBISHI ELECTRIC",
        "ROCKWELL AUTOMATION",
        "EATON MOELLER",
        "BOSCH REXROTH",
        "VICKERS HYDRAULICS"
    ]
    
    clients = [
        "RENAULT TRUCKS",
        "AIRBUS HELICOPTERS",
        "SANOFI AVENTIS",
        "MICHELIN TYRES",
        "TOTAL ENERGIES",
        "ARCELORMITTAL",
        "SAFRAN AIRCRAFT",
        "THALES DEFENSE",
        "PSA PEUGEOT CITROËN",
        "ALSTOM TRANSPORT",
        "DASSAULT AVIATION",
        "VALEO AUTOMOTIVE",
        "SCHNEIDER AUTOMATION",
        "VALLOUREC TUBES",
        "AIR LIQUIDE",
        "BOUYGUES CONSTRUCTION",
        "VINCI ENERGIES",
        "SPIE BATIGNOLLES",
        "EIFFAGE METAL",
        "TECHNIP ENERGIES"
    ]
    
    # Nettoyer les anciennes données de test
    print("🗑️  Nettoyage des anciennes commandes de test...")
    Order.objects.filter(order_number__startswith='TEST-').delete()
    Transaction.objects.filter(notes__contains='Test automatique').delete()
    
    # Compteurs
    orders_created = 0
    total_items = 0
    total_transactions = 0
    
    # Créer 60 commandes d'achat et 40 commandes de vente
    for i in range(100):
        # 60% d'achats, 40% de ventes
        is_purchase = i < 60
        order_type = 'IN' if is_purchase else 'OUT'
        
        # Générer une date aléatoire
        order_date = generate_random_date()
        
        # Numéro de commande avec préfixe TEST pour identification
        if is_purchase:
            order_number = f"TEST-ACH-{order_date.year}-{str(i+1).zfill(3)}"
            company = random.choice(suppliers)
        else:
            order_number = f"TEST-VTE-{order_date.year}-{str(i+1).zfill(3)}"
            company = random.choice(clients)
        
        # Statut selon la date (plus ancien = plus de chance d'être livré)
        days_ago = (timezone.now() - order_date).days
        if days_ago > 365:  # Plus d'un an
            status = 'DELIVERED'
        elif days_ago > 30:  # Plus d'un mois
            status = random.choice(['DELIVERED', 'DELIVERED', 'CONFIRMED'])
        else:  # Récent
            status = random.choice(['DELIVERED', 'CONFIRMED', 'PENDING'])
        
        # Créer la commande
        order = Order.objects.create(
            order_number=order_number,
            order_type=order_type,
            status=status,
            supplier_customer=company,
            order_date=order_date,
            notes=f"Commande de test automatique - {order_date.year}"
        )
        
        # Ajouter 1 à 4 produits par commande
        nb_products = random.randint(1, 4)
        selected_products = random.sample(products, min(nb_products, len(products)))
        
        order_items_created = 0
        
        for product in selected_products:
            # Quantité selon le type de produit
            if 'Roulement' in product.name or 'Joint' in product.name:
                # Petites pièces : quantités importantes
                quantity = random.randint(10, 100)
            elif 'Moteur' in product.name or 'Pompe' in product.name or 'Automate' in product.name:
                # Équipements lourds : petites quantités
                quantity = random.randint(1, 5)
            else:
                # Autres : quantités moyennes
                quantity = random.randint(2, 20)
            
            # Prix avec variation aléatoire (-10% à +15%)
            price_variation = random.uniform(0.9, 1.15)
            if is_purchase:
                # Prix d'achat
                unit_price = product.price * Decimal(str(price_variation))
            else:
                # Prix de vente avec marge (20% à 40%)
                margin = random.uniform(1.2, 1.4)
                unit_price = product.price * Decimal(str(price_variation * margin))
            
            # Créer l'article de commande
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price
            )
            
            order_items_created += 1
            
            # Créer la transaction si la commande est livrée
            if status == 'DELIVERED':
                transaction_quantity = quantity if is_purchase else -quantity
                transaction_type = 'IN' if is_purchase else 'OUT'
                
                # Date de transaction légèrement après la commande
                transaction_date = order_date + timedelta(days=random.randint(1, 15))
                
                Transaction.objects.create(
                    product=product,
                    transaction_type=transaction_type,
                    quantity=transaction_quantity,
                    unit_price=unit_price,
                    order_item=order_item,
                    notes=f"Test automatique - {order.order_number}",
                    timestamp=transaction_date
                )
                
                total_transactions += 1
        
        orders_created += 1
        total_items += order_items_created
        
        # Affichage du progrès
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/100 commandes créées...")
    
    print("\n" + "=" * 60)
    print("🎉 DONNÉES AVANCÉES CRÉÉES AVEC SUCCÈS !")
    print(f"📊 Statistiques finales:")
    print(f"   • {orders_created} nouvelles commandes")
    print(f"   • {total_items} articles de commande")
    print(f"   • {total_transactions} nouvelles transactions")
    
    # Statistiques par année
    print(f"\n📅 Répartition par année:")
    for year in [2023, 2024, 2025]:
        count = Order.objects.filter(
            order_number__startswith='TEST-',
            order_date__year=year
        ).count()
        print(f"   • {year}: {count} commandes")
    
    # Statistiques par type
    purchases = Order.objects.filter(order_number__startswith='TEST-ACH-').count()
    sales = Order.objects.filter(order_number__startswith='TEST-VTE-').count()
    print(f"\n💼 Répartition par type:")
    print(f"   • Achats: {purchases} commandes")
    print(f"   • Ventes: {sales} commandes")
    
    print(f"\n🌐 Vous pouvez maintenant tester les rapports avec des données réalistes !")
    print(f"   • Utilisez les filtres de date pour analyser par période")
    print(f"   • Testez les rapports 2023, 2024, 2025")
    print(f"   • Analysez l'évolution des ventes dans le temps")

if __name__ == "__main__":
    create_advanced_sales_data()