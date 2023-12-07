from django.contrib import admin
from secondapp.models import Student, Contact_us, Category, register_table, add_product,Cart,Order,Wallet

# Register your models here.
admin.site.site_header="My Website Second Project"
class StudentAdmin(admin.ModelAdmin):

    #fields = ["roll_no","name","email"]
    list_display = ["id","name","roll_no","email","fee","gender","address","is_registered"]
    search_fields = ["roll_no","name","email"]
    list_filter = ["name","gender"]
    list_editable = ["email","address"]
class ContactusAdmin(admin.ModelAdmin):
    #fields = ["contact_no","name"]
    list_display = ["name","contact_no","added_on"]
    search_fields = ["name"]
    list_filter = ["added_on"]



class CategoryAdmin(admin.ModelAdmin):
    #fields = ["contact_no","name"]
    list_display = ["id","cat_name","cat_cover_pic","cat_desciption","cat_added_on"]
    search_fields = ["cat_name"]
    list_filter = ["cat_added_on"]


admin.site.register(Student,StudentAdmin)
admin.site.register(Contact_us,ContactusAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(register_table)
admin.site.register(add_product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wallet)






