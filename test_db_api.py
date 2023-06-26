import calendar

from PHPSupport_DB import setup

setup()

import db_api

print(db_api.is_subscription_active('TemWithFrog'))
print(db_api.is_contractor_verified('Vyzlastyle'))
print(db_api.create_order('TemWithFrog', "Это новое описание запроса", "Реквизиты для сайта admin, admin", 111, 222))
print(db_api.get_active_client_orders('TemWithFrog'))
print(db_api.get_order_info(12))
print(db_api.add_message(12, 'Некое сообщение 12...'))
print(db_api.get_order(12))
print(db_api.close_order_by_client(12))
print(db_api.close_order_by_contractor(12))
print(db_api.get_order_rate())
print(db_api.get_current_month_closed_orders('kaser137'))
print(db_api.get_current_month_salary('kaser137'))
print("take order: ", db_api.take_order('kaser137', 12, 55, 'Ну, когда-нибудь сделаю...'))
print(db_api.get_available_orders())
print(db_api.get_contractor_order(12, 'kaser137'))
print(db_api.get_access_info(12))
