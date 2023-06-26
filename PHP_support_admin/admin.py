import datetime

from django.contrib import admin
from PHP_support_admin.models import Order, Question, Contractor, Client, Rate, OrderStat
import db_api

admin.site.register(Order)
admin.site.register(Question)
admin.site.register(Rate)


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['tg_account', 'current_month_finished_orders_count', 'current_month_salary']

    def current_month_finished_orders_count(self, obj):
        today = datetime.date.today()
        the_first_day_in_cur_month = datetime.date(today.year, today.month, 1)
        finished_orders_quantity = obj.orders.filter(is_finished_by_client=True,
                                                     date_closed__gte=the_first_day_in_cur_month,
                                                     date_closed__lte=today,
                                                     ).count()
        return finished_orders_quantity

    def current_month_salary(self, obj):
        return db_api.get_order_rate() * self.current_month_finished_orders_count(obj)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['tg_account', 'total_opened_orders']

    @admin.display(ordering='-total_opened_orders')
    def total_opened_orders(self, obj):
        return obj.orders.all().count()


@admin.register(OrderStat)
class OrderStatAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'month_order_quantity']
    list_filter = ['year', 'month']
    ordering = ('-year', '-month')
