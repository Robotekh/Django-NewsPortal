# from datetime import datetime
#
# from django.db import models
#
# director = 'DI'
# admin = 'AD'
# cook = 'CO'
# cashier = 'CA'
# cleaner = 'CL'
#
# POSITIONS = [
#     (director, 'Директор'),
#     (admin, 'Администратор'),
#     (cook, 'Повар'),
#     (cashier, 'Кассир'),
#     (cleaner, 'Уборщик')
# ]
#
# class Staff(models.Model):
#     full_name = models.CharField(max_length=255)
#     position = models.CharField(max_length=2,
#                                 choices=POSITIONS,
#                                 default=cashier)
#     labor_contract = models.IntegerField()
#
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.FloatField(default=0.0)
#     # composition = models.TextField(default="Состав не указан")
#
#     def __str__(self):
#         return self.name + "/" + str(self.price)
#
#
# class Order(models.Model):
#     time_in = models.DateTimeField(auto_now_add=True)
#     time_out = models.DateTimeField(null=True)
#     cost = models.FloatField(default=0.0)
#     pickup = models.BooleanField(default=False)
#     complete = models.BooleanField(default=False)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='orders')
#     products = models.ManyToManyField(Product, through='ProductOrder')
#
#     def finish_order(self):
#         self.time_out = datetime.now()
#         self.complete = True
#         self.save()
#
#     def get_duration(self):
#         if self.complete:  # если завершён, возвращаем разность объектов
#             return (self.time_out - self.time_in).total_seconds()
#         else:  # если ещё нет, то сколько длится выполнение
#             return (datetime.now() - self.time_in).total_seconds()
#
#
# class ProductOrder(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     _amount = models.IntegerField(default=1, db_column='amount')
#
#     def product_sum(self):
#         return self.product.price * self.amount
#
#     @property
#     def amount(self):
#         return self._amount
#
#     @amount.setter
#     def amount(self, value):
#         self._amount = int(value) if value >= 0 else 0
#         self.save()
#
#         #cashier1 = Staff.objects.create(full_name="Иванов Иван Иванович", position=cashier, labor_contract=1754)

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name + "/" + str(self.price)


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    products = models.ManyToManyField(Product, through='ProductOrder')


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)