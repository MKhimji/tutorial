from django.contrib import admin
from accounts.models import UserProfile

# Register your models here.



##This class is only to help modify the functionality of the admin interface, i.e. sorting


##Purpose of creating this class is to add columns to admin UserProfile page
##It is a class which inherits from a a model which is ModelAdmin

##admin.ModelAdmin , admin comes from import above, ModelAdmin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone', 'website')

## for each row in user_info column we need to be able to populate each row
## each row will be populated by the object parameter
## since we need to pass in different values for each row(every user will have a different descriptiom, city, phone
##we need to return a variable

##for example say it was
##
##def user_info(self, obj):
##        return 'String'

##Since each row is populated by an object and that object is returning a string every element in that row will be a string


##Description is a field

    def user_info(self, obj):
        return obj.description
        user_info.short_description = 'Info'
##get query set is a method which we've inherited from i.e mode.ModelAdmin
##so this method is basically overriding the get_queryset in model.ModelAdmin class
##but we are going to still use the original method from mode.ModelAdmin but just customize the output
##The super method is just saying what ive written above so its accessing
##the method from mode.ModelAdmin

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
##up to the point we've applied the method exactly as it is specified in
##model.ModelAdmin
##Now we can customize the response
##Filter by phone in descending (minus sign), if cant filter other users
##because fields are the same for example phone number then can put in second argument

        queryset = queryset.order_by('-phone', 'user')
        return queryset




##registers userprofile model in django admin and userprofileadmin class

admin.site.register(UserProfile, UserProfileAdmin)