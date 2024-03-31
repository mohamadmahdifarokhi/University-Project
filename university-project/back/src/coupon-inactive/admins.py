# from ..core.admins import BaseAdmin
# from .models import Coupon
#
#
# class CouponAdmin(BaseAdmin, model=Coupon):
#     category = "Coupon"
#     name = "Coupon"
#     name_plural = "Coupons"
#     column_list = [Coupon.id, Coupon.name, Coupon.discount_price, Coupon.discount_percentage,
#                    Coupon.started, Coupon.ended] + BaseAdmin.column_list
#     column_searchable_list = [Coupon.id, Coupon.name]
#     column_sortable_list = [Coupon.name, Coupon.discount_price, Coupon.discount_percentage,
#                             Coupon.started, Coupon.ended] + BaseAdmin.column_sortable_list
