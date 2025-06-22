from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du produit")
    reference = models.CharField(max_length=100, unique=True, verbose_name="Référence")
    description = models.TextField(blank=True, verbose_name="Description")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Prix unitaire"
    )
    min_stock_level = models.PositiveIntegerField(default=10, verbose_name="Niveau de stock minimum")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.reference})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level

    @property
    def total_value(self):
        return self.quantity * self.price


class Order(models.Model):
    ORDER_TYPES = [
        ('IN', 'Entrée (Achat)'),
        ('OUT', 'Sortie (Vente)'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('DELIVERED', 'Livrée'),
        ('CANCELLED', 'Annulée'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de commande")
    order_type = models.CharField(max_length=3, choices=ORDER_TYPES, verbose_name="Type de commande")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Date de commande")
    supplier_customer = models.CharField(max_length=255, blank=True, verbose_name="Fournisseur/Client")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.order_number} - {self.get_order_type_display()}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Prix unitaire"
    )

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
        unique_together = ['order', 'product']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Entrée'),
        ('OUT', 'Sortie'),
        ('ADJUSTMENT', 'Ajustement'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Type de transaction")
    quantity = models.IntegerField(verbose_name="Quantité")
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name="Prix unitaire"
    )
    order_item = models.ForeignKey(
        OrderItem, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Article de commande"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Date/Heure")

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} ({self.quantity})"

    @property
    def total_value(self):
        if self.unit_price:
            return abs(self.quantity) * self.unit_price
        return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Mettre à jour le stock du produit
        if self.transaction_type == 'IN':
            self.product.quantity += self.quantity
        elif self.transaction_type == 'OUT':
            self.product.quantity -= self.quantity
        elif self.transaction_type == 'ADJUSTMENT':
            self.product.quantity += self.quantity
        
        self.product.save()