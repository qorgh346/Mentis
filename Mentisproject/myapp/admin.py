from django.contrib import admin
from django.db.models.base import Model
from .models import *

# Register your models here.

# 유저 DB
@admin.register(User_info)
class User_infoAdmin(admin.ModelAdmin):
    list_display = ('user_id','user_name','user_certification_check')


# 멘티 DB
@admin.register(Menti_info)
class Menti_infoAdmin(admin.ModelAdmin):
    list_display = ('user_info_id', 'contents')

# 칼럼 DB
@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at')

# 캐시 DB
@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('payer', 'user_id', 'cash_charge', 'cash_at', 'success_true_false')

# 결제 DB
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'payment_at', 'sum')
