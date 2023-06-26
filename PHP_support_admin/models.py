import calendar
import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    tg_account = models.CharField('telegram account for communication', max_length=200, unique=True)
    subscription_start_date = models.DateField(verbose_name='date of starting subscription', null=True, blank=True)
    subscription_end_date = models.DateField(verbose_name='date of ending subscription (inclusive)', null=True,
                                             blank=True)

    def __str__(self):
        return self.tg_account

    def is_subscription_active(self) -> bool:
        now = datetime.date.today()
        return self.subscription_start_date <= now <= self.subscription_end_date


class Contractor(models.Model):
    tg_account = models.CharField('telegram account of Contractor', max_length=200, unique=True)
    is_verified = models.BooleanField("permission to get orders is granted?", default=False)

    def __str__(self):
        return self.tg_account


@receiver(post_save, sender=Contractor)
def contractor_disconnected(sender, instance, **kwargs):
    """ Подрядчик разочаровал → хочу закрыть ему доступ к заказам → закрыл, его заказы ушли в состояние первичной
    заявки, если на нём такие были"""
    if not instance.is_verified:
        Order.objects.filter(contractor=instance).update(contractor=None)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='client', related_name='orders',
                               null=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, verbose_name='contractor',
                                   related_name='orders', null=True, blank=True)
    # question = models.ManyToManyField(Question, verbose_name='question', related_name='order', blank=True)
    request = models.TextField('description of the request from client')
    access_info = models.CharField('web site access information', max_length=400)
    estimation = models.CharField(verbose_name='estimation date of completing job from contractor', max_length=200,
                                  blank=True)
    is_finished_by_contractor = models.BooleanField("is order finished from contractor's point of view", default=False)
    is_finished_by_client = models.BooleanField("is order finished from client's point of view", default=False)
    date_opened = models.DateField(verbose_name='date of opening the order by client', null=True, blank=True)
    date_closed = models.DateField(verbose_name='date of closing the order by client', null=True, blank=True)

    client_chat_id = models.IntegerField(verbose_name='chat id to send messages to client', null=True, blank=True)
    contractor_chat_id = models.IntegerField(verbose_name='chat id to send messages to contractor',
                                             null=True, blank=True)

    def __str__(self):
        if self.client:
            return f'{self.client.tg_account}_{self.id}'
        else:
            return f'No_client_{self.id}'


class Question(models.Model):
    question = models.TextField('question about the task from contractor')
    answer = models.TextField('answer about the task from client', blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='question about the order',
                              related_name='questions', null=True, blank=True)

    def __str__(self):
        return f'{self.order}: {self.question[:30]}...'


class Rate(models.Model):
    order_rate = models.PositiveIntegerField(verbose_name="salary (rub) to contractor for 1 order")
    # valid_date = models.DateField(verbose_name="The date of starting ")


class OrderStat(models.Model):
    year = models.PositiveIntegerField(null=True, blank=True)
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    month_order_quantity = models.PositiveIntegerField(null=True, blank=True)


@receiver(post_save, sender=Order)
def order_changed(sender, instance, **kwargs):
    """ Добавился заказ + добавляем в статистику """
    year = instance.date_opened.year
    month = instance.date_opened.month
    the_first_day_in_cur_month = datetime.date(year, month, 1)
    the_first_day_in_next_month = datetime.date(year, month, 1)
    quantity = Order.objects.filter(date_opened__gte=the_first_day_in_cur_month,
                                    date_opened__lte=datetime.date(year, month, calendar.monthrange(year, month)[1])
                                    ).count()
    order_stat, created = OrderStat.objects.update_or_create(year=year, month=month)
    OrderStat.objects.filter(year=order_stat.year, month=order_stat.month).update(month_order_quantity=quantity)
