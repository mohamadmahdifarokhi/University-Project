# from ..core.admins import BaseAdmin
# from .models import Review
#
#
# class ReviewAdmin(BaseAdmin):
#     """
#     Admin class for managing Review model in the application.
#
#     Attributes:
#         model (Review): The model associated with this admin class.
#         category (str): The category label for the admin interface.
#         name (str): The singular name for the model in the admin interface.
#         name_plural (str): The plural name for the model in the admin interface.
#         column_list (list): List of columns to be displayed in the admin interface.
#         column_searchable_list (list): List of columns that can be searched in the admin interface.
#         column_sortable_list (list): List of columns that can be sorted in the admin interface.
#     """
#     model = Review
#     category = "Review"
#     name = "Review"
#     name_plural = "Reviews"
#     column_list = [Review.id, Review.is_reply, Review.head, Review.body, Review.rating] + BaseAdmin.column_list
#     column_searchable_list = [Review.id, Review.head, Review.rating]
#     column_sortable_list = [Review.head, Review.rating] + BaseAdmin.column_sortable_list
#
