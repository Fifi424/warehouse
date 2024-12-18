from django.db import models

# Модель ПВЗ
class PvzLocation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    rent_paid_until = models.DateField()

    class Meta:
        verbose_name = "Список ПВЗ"
        verbose_name_plural = "Списоки ПВЗ"
    
    def __str__(self):
        return self.name

# Модель заказа
class Order(models.Model):
    pvz = models.ForeignKey(PvzLocation, related_name="orders", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)
    sender_name = models.CharField(max_length=100)
    sender_contact = models.CharField(max_length=20)
    creation_date = models.DateField()
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return self.order_number

# Модель позиций в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
    
    def __str__(self):
        return self.item_name

# Модель для выдачи заказов
class Delivery(models.Model):
    order = models.OneToOneField(Order, related_name="delivery", on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=[('Оплачен', 'Оплачен'), ('Предоплачен', 'Предоплачен'), ('Требуется', 'Требуется')])
    recipient_name = models.CharField(max_length=100)
    recipient_contact = models.CharField(max_length=20)
    acceptance_date = models.DateField()
    issued = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Выдача заказа"
        verbose_name_plural = "Выдача заказов"
    
    def __str__(self):
        return f"Delivery {self.order.order_number}"

# Модель для купленных товаров
class PurchasedItem(models.Model):
    order = models.ForeignKey(Order, related_name="purchased_items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Купленный товар"
        verbose_name_plural = "Купленные товары"

    def __str__(self):
        return f"Куплено: {self.item_name} из заказа {self.order.order_number}"

# Модель для возвращённых товаров
class ReturnedItem(models.Model):
    order = models.ForeignKey(Order, related_name="returned_items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Взвращённый товар"
        verbose_name_plural = "Возвращённые товары"

    def __str__(self):
        return f"Возвращено: {self.item_name} из заказа {self.order.order_number}"