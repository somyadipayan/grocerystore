from workers import celery
from celery.schedules import crontab
from models import *
from datetime import datetime, timedelta
from mailer import send_email
from flask import render_template


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(crontab(minute=10, hour=0), daily.s(), name="daily")
    #sender.add_periodic_task(30, daily.s(), name="daily")
    sender.add_periodic_task(30, monthly.s(), name="monthly")

   

@celery.task
def add_together(x,y):
    return x+y

@celery.task
def daily():
    subject = "DAILY REMINDER"
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    inactive_users = User.query.filter(User.last_logged_in < twenty_four_hours_ago).all()
    print(len(inactive_users))
    for user in inactive_users:
        print(f"Trying to send daily  reminder to {user.name}, {user.email}")
        send_email(subject=subject, to=user.email, html_body=render_template('daily.html', user=user))
        print(f"sent daily reminder to {user.name}")
    return "successs"

@celery.task
def monthly():
    subject = "MONTHLY REMINDER"
    users = User.query.filter_by(role = "user").all()
    for user in users:
        one_month_ago = datetime.now() - timedelta(days=30)
        user_orders = Order.query.filter_by(user_id=user.id).filter(Order.order_date > one_month_ago).all()
        order_details = []
        total_amount = 0
        for order in user_orders:
            order_items = OrderItem.query.filter_by(order_id=order.id).all()
            total_amount += order.total_amount
            product_names = [item.product.name for item in order_items]
            order_details.append({
                'order_date': order.order_date.strftime("%d-%m-%Y %H:%M"),
                'product_names': ", ".join(product_names),
                "total_order_value": order.total_amount
            })
        html = render_template('monthly.html', user=user, order_details=order_details, total_amount_spent=total_amount)
        send_email(subject=subject, to=user.email, html_body=html)
    return "successs sending monthly reminder"