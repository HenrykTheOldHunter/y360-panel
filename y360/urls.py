from django.urls import re_path
from . import views

from .admin import admin_view
from django.contrib import admin
admin.site.admin_view = admin_view

urlpatterns = [
    re_path(r'^logout-wire/$', views.logout_wire, name='logout-wire'),
    re_path(r'^logout-confirm/$', views.logout_confirm, name='logout-confirm'),

    re_path(r'^staff/$', views.staff, name='staff'),
    re_path(r'^department/$', views.department, name='department'),
    re_path(r'^groups/$', views.groups, name='groups'),
    re_path(r'^modal/(\d+)/$', views.modal_staff, name='modal'),
    re_path(r'^change-password/(\d+)/$', views.modal_change_password, name='change-password'),
    re_path(r'^drop-2fa/(\d+)/$', views.modal_drop_2fa, name='drop-2fa'),
    re_path(r'^change-password-data/(\d+)/$', views.modal_change_password_data, name='change-password-data'),
    re_path(r'^drop-2fa-data/(\d+)/$', views.modal_drop_2fa_data, name='drop-2fa-data'),
    re_path(r'^enable/(\d+)/$', views.modal_enable, name='enable'),
    re_path(r'^enable-data/(\d+)/$', views.modal_enable_data, name='enable-data'),
    re_path(r'^add-staff/$', views.modal_add_staff, name='add-staff'),
    re_path(r'^add-staff-data/$', views.modal_add_staff_data, name='add-staff-data'),
    re_path(r'^department-create/(\d+)/$', views.departments_create, name='department-create'),
    re_path(r'^add-department/(\d+)/$', views.modal_add_department, name='add-department'),
    re_path(r'^add-department-data/(\d+)/$', views.modal_add_department_data, name='add-department-data'),
    re_path(r'^add-staff-department/(\d+)/$', views.modal_add_staff_department, name='add-staff-department'),
    re_path(r'^add-staff-department-data/(\d+)/$', views.modal_add_staff_department_data, name='add-staff-department-data'),
    re_path(r'^change-department/(\d+)/$', views.modal_change_department, name='change-department'),
    re_path(r'^change-department-data/(\d+)/$', views.modal_change_department_data, name='change-department-data'),
    re_path(r'^delete-department/(\d+)/$', views.modal_delete_department, name='delete-department'),
    re_path(r'^delete-department-data/(\d+)/$', views.modal_delete_department_data, name='delete-department-data'),
    re_path(r'^delete-department-staff/(\d+)/$', views.modal_delete_department_staff, name='delete-department-staff'),
    re_path(r'^delete-department-staff-data/(\d+)/$', views.modal_delete_department_staff_data, name='delete-department-staff-data'),
    re_path(r'^group-create/(\d+)/$', views.groups_create, name='group-create'),
    re_path(r'^add-group/(\d+)/$', views.modal_add_group, name='add-group'),
    re_path(r'^add-group-data/(\d+)/$', views.modal_add_group_data, name='add-group-data'),
    re_path(r'^add-staff-group/(\d+)/$', views.modal_add_staff_group, name='add-staff-group'),
    re_path(r'^add-staff-group-data/(\d+)/$', views.modal_add_staff_group_data, name='add-staff-group-data'),
    re_path(r'^change-group/(\d+)/$', views.modal_change_group, name='change-group'),
    re_path(r'^change-group-data/(\d+)/$', views.modal_change_group_data, name='change-group-data'),
    re_path(r'^delete-group/(\d+)/$', views.modal_delete_group, name='delete-group'),
    re_path(r'^delete-group-data/(\d+)/$', views.modal_delete_group_data, name='delete-group-data'),
    re_path(r'^delete-group-staff/(\d+)/$', views.modal_delete_group_staff, name='delete-group-staff'),
    re_path(r'^delete-group-staff-data/(\d+)/$', views.modal_delete_group_staff_data, name='delete-group-staff-data'),
    re_path(r'^department-lookup/$', views.department_lookup, name='department-lookup'),
    re_path(r'^department-staff-lookup/$', views.department_staff_lookup, name='department-staff-lookup'),
    re_path(r'^group-lookup/$', views.group_lookup, name='group-lookup'),
    re_path(r'^group-staff-lookup/$', views.group_staff_lookup, name='group-staff-lookup'),
    re_path(r'^close-unit/(\d+)/$', views.close_unit, name='close_unit'),
    
    
    #ver2
    re_path(r'^paste/(\d+)/$', views.modal_paste, name='paste'),
    re_path(r'^paste-show-department/(\d+)/$', views.modal_paste_show_department, name='paste-show-department'),
    re_path(r'^paste-show-group/(\d+)/$', views.modal_paste_show_group, name='paste-show-group'),
    re_path(r'^paste-department/(\d+)/$', views.modal_paste_department, name='paste-department'),
    re_path(r'^paste-group/(\d+)/$', views.modal_paste_group, name='paste-group'),

]
