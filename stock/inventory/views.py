from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, F, Q, Count, Case, When
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Product, Order, OrderItem, Transaction
from .forms import ProductForm, OrderForm, OrderItemFormSet, OrderStatusForm
import csv
import json


def product_list(request):
    products = Product.objects.all().order_by('name')
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(reference__icontains=search)
        )
    
    context = {
        'products': products,
        'search': search,
    }
    return render(request, 'inventory/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recent_transactions = Transaction.objects.filter(product=product)[:10]
    
    # Données pour le graphique d'évolution du stock
    stock_history = get_stock_evolution(product)
    
    context = {
        'product': product,
        'recent_transactions': recent_transactions,
        'stock_history': json.dumps(stock_history),
    }
    return render(request, 'inventory/product_detail.html', context)


def get_stock_evolution(product):
    """Calcule l'évolution du stock au fil du temps basée sur les transactions"""
    transactions = Transaction.objects.filter(product=product).order_by('timestamp')
    
    stock_evolution = []
    current_stock = 0
    
    if transactions.exists():
        # Calculer l'évolution basée sur chaque transaction
        for transaction in transactions:
            if transaction.transaction_type == 'IN':
                current_stock += transaction.quantity
            elif transaction.transaction_type == 'OUT':
                current_stock -= transaction.quantity
            elif transaction.transaction_type == 'ADJUSTMENT':
                current_stock += transaction.quantity
            
            stock_evolution.append({
                'date': transaction.timestamp.strftime('%Y-%m-%d'),
                'stock': current_stock
            })
    else:
        # Aucune transaction, juste le stock actuel
        stock_evolution.append({
            'date': product.created_at.strftime('%Y-%m-%d'),
            'stock': product.quantity
        })
    
    return stock_evolution


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produit "{product.name}" créé avec succès.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Ajouter un produit'})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produit "{product.name}" modifié avec succès.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Modifier le produit'})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Produit "{product_name}" supprimé avec succès.')
        return redirect('product_list')
    
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    order_type = request.GET.get('type')
    status = request.GET.get('status')
    
    if order_type:
        orders = orders.filter(order_type=order_type)
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'order_types': Order.ORDER_TYPES,
        'status_choices': Order.STATUS_CHOICES,
        'selected_type': order_type,
        'selected_status': status,
    }
    return render(request, 'inventory/order_list.html', context)


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'inventory/order_detail.html', context)


def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Statut de la commande "{order.order_number}" mis à jour avec succès.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    
    context = {
        'form': form,
        'order': order,
        'title': f'Modifier le statut - {order.order_number}'
    }
    return render(request, 'inventory/order_status_form.html', context)


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            
            # Traiter les transactions pour chaque article
            for item in order.orderitem_set.all():
                transaction_type = 'IN' if order.order_type == 'IN' else 'OUT'
                quantity = item.quantity if order.order_type == 'IN' else -item.quantity
                
                Transaction.objects.create(
                    product=item.product,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    unit_price=item.unit_price,
                    order_item=item,
                    notes=f"Commande {order.order_number}"
                )
            
            messages.success(request, f'Commande "{order.order_number}" créée avec succès.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Créer une commande',
        'products': Product.objects.all().order_by('name'),
    }
    return render(request, 'inventory/order_form.html', context)


def dashboard(request):
    # Statistiques générales
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_stock_level')).count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # Commandes récentes
    recent_orders = Order.objects.order_by('-order_date')[:5]
    
    # Produits les plus vendus (30 derniers jours)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    top_selling_products = Product.objects.annotate(
        sales_count=Count('transaction', filter=Q(
            transaction__transaction_type='OUT',
            transaction__timestamp__gte=thirty_days_ago
        ))
    ).order_by('-sales_count')[:5]
    
    # Transactions récentes
    recent_transactions = Transaction.objects.select_related('product').order_by('-timestamp')[:10]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_stock_value': total_stock_value,
        'recent_orders': recent_orders,
        'top_selling_products': top_selling_products,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'inventory/dashboard.html', context)


def stock_report(request):
    products = Product.objects.all().order_by('name')
    
    # Filtres
    low_stock_only = request.GET.get('low_stock')
    if low_stock_only:
        products = products.filter(quantity__lte=F('min_stock_level'))
    
    # Calcul des statistiques de stock
    all_products = Product.objects.all()
    out_of_stock = all_products.filter(quantity=0).count()
    low_stock = all_products.filter(quantity__lte=F('min_stock_level'), quantity__gt=0).count()
    ok_stock = all_products.filter(quantity__gt=F('min_stock_level')).count()
    
    context = {
        'products': products,
        'low_stock_only': low_stock_only,
        'out_of_stock_count': out_of_stock,
        'low_stock_count': low_stock,
        'ok_stock_count': ok_stock,
    }
    return render(request, 'inventory/stock_report.html', context)


def sales_report(request):
    # Gestion des filtres
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    product_id = request.GET.get('product')
    
    # Dates par défaut (30 derniers jours)
    today = timezone.now().date()
    if date_from_str:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
    else:
        date_from = today - timedelta(days=30)
    
    if date_to_str:
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
    else:
        date_to = today
    
    # Convertir en datetime avec timezone
    date_from_dt = timezone.make_aware(datetime.combine(date_from, datetime.min.time()))
    date_to_dt = timezone.make_aware(datetime.combine(date_to, datetime.max.time()))
    
    # Requête de base pour les transactions de vente
    sales_transactions = Transaction.objects.filter(
        transaction_type='OUT',
        timestamp__gte=date_from_dt,
        timestamp__lte=date_to_dt
    ).select_related('product', 'order_item__order')
    
    # Filtre par produit si spécifié
    if product_id:
        sales_transactions = sales_transactions.filter(product_id=product_id)
    
    # Calculer les statistiques directement depuis les transactions
    stats = {
        'total_transactions': sales_transactions.count(),
        'total_quantity': 0,
        'total_value': 0,
        'products_sold': set(),
    }
    
    # Grouper par produit pour le classement
    product_sales = {}
    
    for transaction in sales_transactions:
        quantity_sold = abs(transaction.quantity)  # Convertir en positif
        value = quantity_sold * (transaction.unit_price or 0)
        
        stats['total_quantity'] += quantity_sold
        stats['total_value'] += value
        stats['products_sold'].add(transaction.product.id)
        
        # Grouper par produit
        if transaction.product.id not in product_sales:
            product_sales[transaction.product.id] = {
                'product': transaction.product,
                'quantity': 0,
                'value': 0,
                'transactions': []
            }
        
        product_sales[transaction.product.id]['quantity'] += quantity_sold
        product_sales[transaction.product.id]['value'] += value
        product_sales[transaction.product.id]['transactions'].append(transaction)
    
    # Calculer le total et la quantité absolue pour toutes les transactions
    for transaction in sales_transactions:
        transaction.quantity_abs = abs(transaction.quantity)
        transaction.total_calculated = transaction.quantity_abs * (transaction.unit_price or 0)
    
    # Ajouter le prix moyen et le pourcentage
    for product_data in product_sales.values():
        if product_data['quantity'] > 0:
            product_data['avg_price'] = product_data['value'] / product_data['quantity']
        else:
            product_data['avg_price'] = 0
    
    # Trier par quantité vendue
    top_selling_list = sorted(
        product_sales.values(), 
        key=lambda x: x['quantity'], 
        reverse=True
    )
    
    stats['unique_products'] = len(stats['products_sold'])
    
    # Période d'affichage
    days_diff = (date_to - date_from).days + 1
    if days_diff <= 1:
        period = "Aujourd'hui"
    elif days_diff <= 7:
        period = f"{days_diff} derniers jours"
    elif days_diff <= 31:
        period = f"{days_diff} derniers jours"
    else:
        period = f"Du {date_from.strftime('%d/%m/%Y')} au {date_to.strftime('%d/%m/%Y')}"
    
    # Raccourcis de dates
    date_shortcuts = {
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
        '7_days': (today - timedelta(days=7)).strftime('%Y-%m-%d'),
        '30_days': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
        '90_days': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
    }
    
    # Liste des produits pour le filtre
    products = Product.objects.all().order_by('name')
    selected_product = None
    if product_id:
        try:
            selected_product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            pass
    
    context = {
        'sales_transactions': sales_transactions,
        'top_selling': top_selling_list,
        'stats': stats,
        'period': period,
        'date_from': date_from.strftime('%Y-%m-%d'),
        'date_to': date_to.strftime('%Y-%m-%d'),
        'date_shortcuts': date_shortcuts,
        'products': products,
        'selected_product_id': int(product_id) if product_id else None,
        'selected_product': selected_product,
        'filters_applied': bool(date_from_str or date_to_str or product_id),
    }
    return render(request, 'inventory/sales_report.html', context)


def transaction_history(request):
    transactions = Transaction.objects.select_related('product', 'order_item__order').order_by('-timestamp')
    
    # Filtres
    product_id = request.GET.get('product')
    transaction_type = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if product_id:
        transactions = transactions.filter(product_id=product_id)
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if date_from:
        transactions = transactions.filter(timestamp__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(timestamp__date__lte=date_to)
    
    # Calcul des statistiques
    stats = {
        'in_count': transactions.filter(transaction_type='IN').count(),
        'out_count': transactions.filter(transaction_type='OUT').count(),
        'adjustment_count': transactions.filter(transaction_type='ADJUSTMENT').count(),
        'total_count': transactions.count(),
    }
    
    products = Product.objects.all().order_by('name')
    
    context = {
        'transactions': transactions,
        'products': products,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'stats': stats,
        'filters': {
            'product_id': product_id,
            'transaction_type': transaction_type,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    return render(request, 'inventory/transaction_history.html', context)


def export_stock_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Référence', 'Quantité', 'Prix unitaire', 'Valeur totale', 'Stock minimum'])
    
    for product in Product.objects.all():
        writer.writerow([
            product.name,
            product.reference,
            product.quantity,
            product.price,
            product.total_value,
            product.min_stock_level
        ])
    
    return response

def export_sales_csv(request):
    from datetime import datetime, timedelta
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date/Heure', 'Produit', 'Référence', 'Quantité', 'Prix unitaire', 'Total', 'Commande', 'Notes'])
    
    # Récupérer les filtres
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    product_id = request.GET.get('product')
    
    # Construire la requête
    transactions = Transaction.objects.filter(transaction_type='OUT').order_by('-timestamp')
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            transactions = transactions.filter(timestamp__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            transactions = transactions.filter(timestamp__date__lte=date_to_obj)
        except ValueError:
            pass
    
    if product_id:
        try:
            transactions = transactions.filter(product_id=int(product_id))
        except ValueError:
            pass
    
    for transaction in transactions:
        writer.writerow([
            transaction.timestamp.strftime('%d/%m/%Y %H:%M'),
            transaction.product.name,
            transaction.product.reference,
            abs(transaction.quantity),
            transaction.unit_price,
            transaction.total_value,
            transaction.order_item.order.order_number if transaction.order_item else '-',
            transaction.notes or '-'
        ])
    
    return response

def export_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions_history.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date/Heure', 'Produit', 'Référence', 'Type', 'Quantité', 'Prix unitaire', 'Valeur', 'Commande', 'Notes'])
    
    # Récupérer les filtres
    product_id = request.GET.get('product')
    transaction_type = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Construire la requête
    transactions = Transaction.objects.all().order_by('-timestamp')
    
    if product_id:
        try:
            transactions = transactions.filter(product_id=int(product_id))
        except ValueError:
            pass
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            transactions = transactions.filter(timestamp__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            from datetime import datetime
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            transactions = transactions.filter(timestamp__date__lte=date_to_obj)
        except ValueError:
            pass
    
    for transaction in transactions:
        type_display = {
            'IN': 'Entrée',
            'OUT': 'Sortie',
            'ADJUSTMENT': 'Ajustement'
        }.get(transaction.transaction_type, transaction.transaction_type)
        
        writer.writerow([
            transaction.timestamp.strftime('%d/%m/%Y %H:%M'),
            transaction.product.name,
            transaction.product.reference,
            type_display,
            transaction.quantity,
            transaction.unit_price or '-',
            transaction.total_value,
            transaction.order_item.order.order_number if transaction.order_item else '-',
            transaction.notes or '-'
        ])
    
    return response