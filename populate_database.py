#!/usr/bin/env python
"""Script pour remplir la base de données avec des produits industriels"""

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

# Données de produits industriels
INDUSTRIAL_PRODUCTS = [
    # Équipements électriques
    {"name": "Moteur électrique 3kW", "reference": "MOT-3KW-001", "price": 450.00, "quantity": 15, "min_stock": 5, "description": "Moteur triphasé 3000 tr/min"},
    {"name": "Transformateur 220V/24V", "reference": "TRANS-220-24", "price": 89.50, "quantity": 25, "min_stock": 10, "description": "Transformateur de sécurité 100VA"},
    {"name": "Contacteur 25A", "reference": "CONT-25A-001", "price": 32.80, "quantity": 50, "min_stock": 15, "description": "Contacteur triphasé 25A bobine 24V"},
    {"name": "Variateur de fréquence 5.5kW", "reference": "VAR-5K5-001", "price": 780.00, "quantity": 8, "min_stock": 3, "description": "Variateur vectoriel IP20"},
    {"name": "Relais thermique 16-25A", "reference": "REL-TH-16-25", "price": 45.60, "quantity": 30, "min_stock": 12, "description": "Protection surcharge moteur"},
    
    # Capteurs et instrumentation
    {"name": "Capteur de température Pt100", "reference": "CAPT-PT100-01", "price": 125.00, "quantity": 20, "min_stock": 8, "description": "Sonde Pt100 3 fils, -50°C à +200°C"},
    {"name": "Capteur de pression 0-10 bar", "reference": "CAPT-P-10B", "price": 89.00, "quantity": 12, "min_stock": 5, "description": "Transmetteur 4-20mA"},
    {"name": "Débitmètre électromagnétique DN50", "reference": "DEB-MAG-50", "price": 1250.00, "quantity": 4, "min_stock": 2, "description": "Débitmètre haute précision"},
    {"name": "Manomètre glycérine 0-16 bar", "reference": "MANO-GLY-16", "price": 28.50, "quantity": 45, "min_stock": 20, "description": "Cadran 100mm avec amortisseur"},
    {"name": "Thermomètre à cadran", "reference": "THERMO-CAD-01", "price": 18.90, "quantity": 35, "min_stock": 15, "description": "0-120°C, tige 100mm"},
    
    # Pneumatique
    {"name": "Vérin pneumatique Ø32 course 50mm", "reference": "VER-32-50", "price": 68.00, "quantity": 18, "min_stock": 8, "description": "Vérin double effet ISO 6432"},
    {"name": "Électrovanne 5/2 G1/4", "reference": "EV-5-2-G14", "price": 95.00, "quantity": 22, "min_stock": 10, "description": "Électrovanne bistable 24VDC"},
    {"name": "Régulateur de pression G1/4", "reference": "REG-P-G14", "price": 42.50, "quantity": 30, "min_stock": 12, "description": "0-10 bar avec manomètre"},
    {"name": "Filtre à air G1/2", "reference": "FILT-AIR-G12", "price": 35.80, "quantity": 25, "min_stock": 10, "description": "Filtre coalesceur 5µm"},
    {"name": "Raccord rapide DN6", "reference": "RACC-RAP-6", "price": 8.50, "quantity": 100, "min_stock": 50, "description": "Raccord pneumatique laiton"},
    
    # Hydraulique
    {"name": "Pompe hydraulique 2.2kW", "reference": "POMP-HYD-2K2", "price": 890.00, "quantity": 6, "min_stock": 2, "description": "Pompe à engrenages externe"},
    {"name": "Distributeur hydraulique 4/3", "reference": "DIST-4-3-001", "price": 245.00, "quantity": 8, "min_stock": 3, "description": "Centre fermé NG6"},
    {"name": "Accumulateur hydraulique 1L", "reference": "ACCU-HYD-1L", "price": 156.00, "quantity": 10, "min_stock": 4, "description": "À membrane 210 bar"},
    {"name": "Filtre hydraulique retour", "reference": "FILT-HYD-RET", "price": 78.50, "quantity": 15, "min_stock": 6, "description": "Élément 10µm G1/2"},
    
    # Mécanique
    {"name": "Roulement à billes 6204 2RS", "reference": "ROUL-6204-2RS", "price": 12.50, "quantity": 80, "min_stock": 30, "description": "Roulement étanche Ø20x47x14"},
    {"name": "Courroie trapézoïdale SPA 1250", "reference": "COUR-SPA-1250", "price": 15.80, "quantity": 25, "min_stock": 10, "description": "Courroie section SPA"},
    {"name": "Réducteur à vis sans fin i=30", "reference": "RED-VS-30", "price": 320.00, "quantity": 5, "min_stock": 2, "description": "Réducteur couple 150Nm"},
    {"name": "Joint torique NBR 20x3", "reference": "JOINT-OR-20-3", "price": 2.50, "quantity": 200, "min_stock": 100, "description": "Joint NBR 70 shores"},
    {"name": "Graisse haute température", "reference": "GRAI-HT-001", "price": 24.90, "quantity": 40, "min_stock": 15, "description": "Cartouche 400g -20°C/+150°C"},
    
    # Vannes et robinetterie
    {"name": "Vanne à boisseau sphérique DN25", "reference": "VAN-BOIS-25", "price": 45.00, "quantity": 20, "min_stock": 8, "description": "Inox 316 PN40 filetage BSP"},
    {"name": "Électrovanne eau DN20 NC", "reference": "EV-EAU-20-NC", "price": 125.00, "quantity": 12, "min_stock": 5, "description": "230VAC normalement fermée"},
    {"name": "Clapet anti-retour DN32", "reference": "CLAP-AR-32", "price": 38.50, "quantity": 15, "min_stock": 6, "description": "Clapet à ressort laiton"},
    {"name": "Vanne de régulation pneumatique", "reference": "VAN-REG-PNEU", "price": 480.00, "quantity": 4, "min_stock": 2, "description": "DN25 actuateur 3-15 PSI"},
    
    # Automatisme
    {"name": "Automate programmable 16E/12S", "reference": "AUTO-16-12", "price": 650.00, "quantity": 6, "min_stock": 2, "description": "CPU compacte Ethernet"},
    {"name": "Module d'extension 8 entrées", "reference": "MOD-8E-001", "price": 145.00, "quantity": 10, "min_stock": 4, "description": "Entrées TOR 24VDC"},
    {"name": "IHM tactile 7 pouces", "reference": "IHM-7P-001", "price": 420.00, "quantity": 8, "min_stock": 3, "description": "Écran couleur Ethernet"},
    {"name": "Détecteur de proximité inductif", "reference": "DET-PROX-IND", "price": 35.00, "quantity": 50, "min_stock": 20, "description": "M18 PNP NO 2 fils"},
    {"name": "Fin de course IP67", "reference": "FDC-IP67-001", "price": 28.00, "quantity": 35, "min_stock": 15, "description": "Corps métallique 2NO+2NF"},
    
    # Éclairage industriel
    {"name": "Projecteur LED 50W IP65", "reference": "PROJ-LED-50W", "price": 89.00, "quantity": 25, "min_stock": 10, "description": "6500K 5000 lumens"},
    {"name": "Réglette LED étanche 36W", "reference": "REG-LED-36W", "price": 45.00, "quantity": 30, "min_stock": 12, "description": "120cm IP65 4000K"},
    {"name": "Lampe de signalisation LED", "reference": "LAMP-SIG-LED", "price": 32.50, "quantity": 40, "min_stock": 15, "description": "Rouge/Vert 24VDC Ø22"},
    
    # Sécurité
    {"name": "Arrêt d'urgence Ø40 rouge", "reference": "AU-40-ROUGE", "price": 18.50, "quantity": 60, "min_stock": 25, "description": "Bouton coup de poing 1NC"},
    {"name": "Bouton poussoir vert Ø22", "reference": "BP-22-VERT", "price": 12.80, "quantity": 80, "min_stock": 30, "description": "Contact 1NO affleurant"},
    {"name": "Sélecteur 3 positions Ø22", "reference": "SEL-3P-22", "price": 22.90, "quantity": 25, "min_stock": 10, "description": "0-1-2 maintenu 2NO"},
    {"name": "Voyant lumineux rouge Ø22", "reference": "VOY-22-ROUGE", "price": 15.60, "quantity": 45, "min_stock": 20, "description": "LED 24VDC lisse"},
    
    # Outils et consommables
    {"name": "Huile hydraulique HVI 46", "reference": "HUILE-HVI-46", "price": 68.00, "quantity": 30, "min_stock": 12, "description": "Bidon 20L anti-usure"},
    {"name": "Nettoyant contact électrique", "reference": "NETT-CONT-EL", "price": 14.50, "quantity": 50, "min_stock": 20, "description": "Aérosol 400ml dégraissant"},
    {"name": "Pâte d'étanchéité filetages", "reference": "PATE-ETAN-FIL", "price": 8.90, "quantity": 60, "min_stock": 25, "description": "Tube 50g haute température"},
    {"name": "Fil électrique H07V-K 2.5mm²", "reference": "FIL-H07VK-2.5", "price": 1.25, "quantity": 500, "min_stock": 200, "description": "Prix au mètre - Rouge"},
    {"name": "Gaine thermorétractable Ø6mm", "reference": "GAIN-THER-6", "price": 0.85, "quantity": 300, "min_stock": 150, "description": "Prix au mètre - Noire"},
]

def clear_database():
    """Vide la base de données"""
    print("🗑️  Nettoyage de la base de données...")
    Transaction.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    print("✅ Base de données nettoyée")

def create_products():
    """Crée les produits industriels"""
    print("📦 Création des produits...")
    products = []
    
    for product_data in INDUSTRIAL_PRODUCTS:
        product = Product.objects.create(
            name=product_data["name"],
            reference=product_data["reference"],
            description=product_data["description"],
            quantity=product_data["quantity"],
            price=Decimal(str(product_data["price"])),
            min_stock_level=product_data["min_stock"]
        )
        products.append(product)
        print(f"  ✓ {product.name} ({product.reference})")
    
    print(f"✅ {len(products)} produits créés")
    return products

def create_sample_orders(products):
    """Crée des commandes d'exemple"""
    print("📋 Création de commandes d'exemple...")
    
    # Quelques fournisseurs fictifs
    suppliers = [
        "SCHNEIDER ELECTRIC",
        "SIEMENS",
        "FESTO",
        "PARKER HANNIFIN",
        "SKF",
        "SICK",
        "PHOENIX CONTACT",
        "LEGRIS",
    ]
    
    clients = [
        "RENAULT TRUCKS",
        "AIRBUS",
        "SANOFI",
        "MICHELIN",
        "TOTAL ENERGIES",
        "ARCELORMITTAL",
        "SAFRAN",
        "THALES",
    ]
    
    # Créer des commandes d'achat (IN)
    for i in range(5):
        order = Order.objects.create(
            order_number=f"ACH-2024-{str(i+1).zfill(3)}",
            order_type='IN',
            status=random.choice(['DELIVERED', 'CONFIRMED']),
            supplier_customer=random.choice(suppliers),
            order_date=datetime.now() - timedelta(days=random.randint(1, 30)),
            notes="Commande d'approvisionnement"
        )
        
        # Ajouter 2-5 produits par commande
        selected_products = random.sample(products, random.randint(2, 5))
        for product in selected_products:
            quantity = random.randint(5, 20)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
            
            # Créer la transaction correspondante
            Transaction.objects.create(
                product=product,
                transaction_type='IN',
                quantity=quantity,
                unit_price=product.price,
                notes=f"Achat - {order.order_number}",
                timestamp=order.order_date
            )
        
        print(f"  ✓ Commande d'achat {order.order_number}")
    
    # Créer des commandes de vente (OUT)
    for i in range(8):
        order = Order.objects.create(
            order_number=f"VTE-2024-{str(i+1).zfill(3)}",
            order_type='OUT',
            status=random.choice(['DELIVERED', 'CONFIRMED', 'PENDING']),
            supplier_customer=random.choice(clients),
            order_date=datetime.now() - timedelta(days=random.randint(1, 15)),
            notes="Commande client"
        )
        
        # Ajouter 1-3 produits par commande
        selected_products = random.sample(products, random.randint(1, 3))
        for product in selected_products:
            # Quantité limitée par le stock disponible
            max_qty = min(product.quantity, 10)
            if max_qty > 0:
                quantity = random.randint(1, max_qty)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price * Decimal('1.2')  # Marge de 20%
                )
                
                # Créer la transaction correspondante (sortie)
                Transaction.objects.create(
                    product=product,
                    transaction_type='OUT',
                    quantity=-quantity,  # Négatif pour sortie
                    unit_price=product.price * Decimal('1.2'),
                    notes=f"Vente - {order.order_number}",
                    timestamp=order.order_date
                )
        
        print(f"  ✓ Commande de vente {order.order_number}")
    
    print("✅ Commandes d'exemple créées")

def create_inventory_adjustments(products):
    """Crée quelques ajustements d'inventaire"""
    print("⚖️  Création d'ajustements d'inventaire...")
    
    # Sélectionner quelques produits pour ajustement
    for product in random.sample(products, 5):
        adjustment = random.randint(-5, 10)
        Transaction.objects.create(
            product=product,
            transaction_type='ADJUSTMENT',
            quantity=adjustment,
            unit_price=None,
            notes="Ajustement d'inventaire",
            timestamp=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        print(f"  ✓ Ajustement {product.name}: {adjustment:+d}")
    
    print("✅ Ajustements créés")

def main():
    """Fonction principale"""
    print("🏭 PEUPLEMENT DE LA BASE DE DONNÉES - PRODUITS INDUSTRIELS")
    print("=" * 60)
    
    # Vider la base
    clear_database()
    
    # Créer les produits
    products = create_products()
    
    # Créer des commandes d'exemple
    create_sample_orders(products)
    
    # Créer des ajustements
    create_inventory_adjustments(products)
    
    print("\n" + "=" * 60)
    print("🎉 BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS !")
    print(f"📊 Statistiques:")
    print(f"   • {Product.objects.count()} produits")
    print(f"   • {Order.objects.count()} commandes")
    print(f"   • {OrderItem.objects.count()} articles de commande")
    print(f"   • {Transaction.objects.count()} transactions")
    print("\n🌐 Vous pouvez maintenant tester l'application !")

if __name__ == "__main__":
    main()