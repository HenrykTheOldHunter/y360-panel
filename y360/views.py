from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .api import Yapi
from .models import *
from .decorators import *
import re
import json

avatarSrc = "https://avatars.mds.yandex.net/get-yapic/{}/islands-middle"
error_messages = {
            "password.equals_previous":"Ошибка! Пароль совпадает с предыдущим!",
            "password.short":"Ошибка! Пароль слишком короткий!",
            "password.weak":"Ошибка! Пароль слишком слабый!",
            "password.prohibitedsymbols":"Ошибка! Пароль содержит недопустимые символы!",
            "password.likelogin":"Ошибка! Пароль и логин совпадают!",
            "login.prohibitedsymbols":"Ошибка! Логин содержит недопустимые символы!",
            "some_user_has_this_login":"Ошибка! Пользователь с таким логином уже существует!",
            "invalid_name": "Ошибка! Некорректное имя или название.",
            "name_too_short": "Ошибка! Имя или название слишком короткое!",
}
y = Yapi()

@apply_permissions
def logout_wire(request):
    logout(request)
    return HttpResponseRedirect('/')

def logout_confirm(request):
    return render(
	request,
	'logout_confirm.html',
	context={},
    )
#Staff
@login_required
def staff(request):
    global y
    global avatarSrc
    info = []
    querySet = Staff.objects.values_list("id", "email", "name", "img").order_by("name")
    for user in list(querySet):
        img = avatarFormat(user[3])
        info.append([user[0], user[1], user[2], avatarSrc.format(img)])
    return render(
        request,
        'staff.html',
        context={'count':Staff.objects.all().count(),'info':info},
    )
@apply_permissions
@login_required
def modal_staff(request, id):
    global avatarSrc
    user = Staff.objects.get(id=id)
    img = avatarFormat(user.img)
    try:
        department = Departments.objects.get(id=user.departmentId).name
    except ObjectDoesNotExist:
        department = "Нет подразделения"
    groupsId = list(Groups_Staff.objects.filter(staffId=id).values_list("groupId", flat=True).order_by("groupId"))
    groups=[]
    for groupId in groupsId:
        groups.append(Groups.objects.get(id=groupId).name)
    return render(
         request,
         'modal_staff.html',
         context={'id':id, 'name':user.name, 'department':department, 'groups':groups, 'role':user.role, 'avatar':img},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_password(request, id):
    return render(
        request,
        'modal_change_password.html',
        context={'id':id},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_drop_2fa(request, id):
    return render(
        request,
        'modal_drop_2fa.html',
        context={'id':id},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_enable(request, id):
     
    user = y.modal_staff(id)
    isEnabled = bool(user["isEnabled"])
    if isEnabled:
        status = "активен"
        action = "Заблокировать"
    else:
        status = "заблокирован"
        action = "Разблокировать"
    return render(
        request,
        'modal_enable.html',
        context={'user':user["name"]["first"] + " " + user["name"]["last"], 'status':status, 'action':action, 'id':id},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_password_data(request, id):
    global y
    user = y.modal_staff(id)
    password = ""
    passwordChangeRequired = True
    if request.method == "POST":
        password = str(request.POST.get("password", None))
        if password == "" or password == None:
            return HttpResponse(status=400, content=json.dumps({"Error":["new-password"]}))
        passwordChangeRequired = request.POST.get("passwordChangeRequired", True)
    else:
        return HttpResponse(status=500, content=json.dumps({}))
    payload_dict = {
        "contacts": [{
            "type": "email",
            "value": user.get("email")
            }],
        "departmentId": int(user.get("departmentId")),
        "name": {
            "first": user.get("name")["first"],
            "last": user.get("name")["last"],
        },
        "password": password,
        "passwordChangeRequired": bool(passwordChangeRequired)
    }
    result = y.change_user(id, payload_dict)
    if result[1] != False:
        return HttpResponse(status=200, content=json.dumps({}))
    else:
        message = "Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже. "
        try:
            message = error_messages[result[2]["message"]]
        except Exception:
            pass
        return HttpResponse(status=result[0], content=json.dumps({"Error":message}))

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_drop_2fa_data(request, id):
    global y
    result = y.drop_2fa(id)
    if result[1] != False:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_enable_data(request, id):
    global y
    user = y.modal_staff(id)
    isEnabled = bool(user["isEnabled"])
    payload_dict={}
    if isEnabled:
        payload_dict = {
        "contacts": [{
            "type": "email",
            "value": user.get("email")
            }],
        "isEnabled": False,
        "name": {
            "first": user.get("name")["first"],
            "last": user.get("name")["last"],
            },
        }
    else:
        payload_dict = {
        "contacts": [{
            "type": "email",
            "value": user.get("email")
            }],
        "isEnabled": True,
        "name": {
            "first": user.get("name")["first"],
            "last": user.get("name")["last"],
            },
        }
    result = y.change_user(id, payload_dict)
    if result[1] != False:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])


@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_staff(request):
    departments = list(Departments.objects.values_list("id", "name").order_by("name"))
    return render(
        request,
        'modal_add_staff.html',
        context={'departments' : departments},
    )

@csrf_protect
@csrf_exempt
@apply_permissions
@login_required
def modal_add_staff_data(request):
    global y
    last=first=middle=email=login=password=""
    department=2
    errors = []
    if request.method == "POST":
        last = str(request.POST.get("last", ""))
        if last == "": errors.append("last")
        first = str(request.POST.get("first", ""))
        if first == "": errors.append("first")
        middle = str(request.POST.get("middle", ""))
        email = str(request.POST.get("email", ""))
        if email == "": errors.append("email")
        login = str(request.POST.get("login", ""))
        if login == "": errors.append("login")
        password = str(request.POST.get("password", ""))
        if password == "": errors.append("password")
        department = str(request.POST.get("department", 1))
    else:
        return HttpResponse(status=500)
    if errors:
        return HttpResponse(status=400, content=json.dumps({"Error":errors}))
    payload_dict = {
        "contacts": [
            {
            "type": "email",
            "value": email
            }
        ],
        "departmentId": int(department),
        "isAdmin": False,
        "name": {
            "first": first,
            "last": last,
            "middle": middle
        },
        "nickname": login,
        "password": password,
    }
    result = y.modal_staff_add_data(payload_dict)
    if result[1] != False:
        m_user = Staff()
        m_user.id = result[0]["id"]
        m_user.name = first + " " + last
        m_user.email = result[0]["email"]
        m_user.departmentId = department
        m_user.role = "Сотрудник"
        m_user.img = 0
        m_user.save()
        return HttpResponse(status=200, content=json.dumps({}))
    else:
        message = "Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже. "
        try:
            message = error_messages[result[2]["message"]]
        except Exception:
            pass
        return HttpResponse(status=result[0], content=json.dumps({"Error":message}))



#Departments
@login_required
@csrf_protect
@csrf_exempt
def department(request):
    result=[]
    main_department = Departments.objects.get(parentId=0)
    main_department_result=[main_department.id, main_department.name]
    departments = list(Departments.objects.filter(parentId=1).values_list("id", "name", "label"))
    for department in departments:
        result.append([department[0], department[1], department[2]])
    return render(
        request,
        'department.html',
        context={'mainDepartment':main_department_result, 'departments':result, 'total':Departments.objects.all().count()},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def departments_create(request, id):
    level=levelFormat(request)
    children = list(Departments.objects.filter(parentId=id).values_list("id", flat=True))
    users = list(Staff.objects.filter(departmentId=id).values_list("id", "name", "email", "img"))
    departmentsResult=[]
    usersResult=[]
    for child in children:
        department = Departments.objects.get(id=child)
        departmentsResult.append([department.id, department.name, department.parentId])
    for user in users:
        img = avatarFormat(user[3])
        usersResult.append([user[0], user[1], user[2], img, id])
    return render(
        request,
        'departments_create.html',
        context={'departments':departmentsResult, 'users':usersResult, 'level':level},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_department(request, id):
    domain = "@"+Domains.objects.get(isMaster = True).name
    return render(
        request,
        'modal_add_department.html',
        context={'domain':domain, 'id':id},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_department_data(request, id):
    global y
    name=description=label=""
    if request.method == "POST":
        name = str(request.POST.get("name", ""))
        if name == "" or name == None:
            return HttpResponse(status=400, content=json.dumps({"Error":["department-name-add"]}))
        description = str(request.POST.get("description", ""))
        label = str(request.POST.get("label", ""))
    else:
        return HttpResponse(status=500, content=json.dumps({}))
    payload_dict = {
        "description": description,
        "label": label,
        "name": name,
        "parentId": id
    }
    result = y.modal_add_department_data(payload_dict)
    if result[1] != False:
        m_department = Departments()
        m_department.id = result[0]["id"]
        m_department.name = name
        m_department.parentId = id
        m_department.membersCount = 0
        m_department.label = label
        m_department.save()
        return HttpResponse(status=200, content=json.dumps({}))
    else:
        message = "Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже. "
        try:
            message = error_messages[result[2]["message"]]
        except Exception:
            pass
        return HttpResponse(status=result[0], content=json.dumps({"Error":message}))
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_staff_department(request, id):
    users = list(Staff.objects.filter(~Q(departmentId=id)).values_list("id", "name", "email", "img"))
    usersResult=[]
    empty = False
    if len(users) == 0:
        empty = True
    else:
        for user in users:
            img = avatarFormat(user[3])
            departmentId = Staff.objects.get(id=user[0]).departmentId
            if departmentId != 0:
                department = Departments.objects.get(id=departmentId).name
                usersResult.append([user[0], user[1], user[2], department, img])
    return render(
        request,
        'modal_add_staff_department.html',
        context={'users':usersResult, 'empty':empty, 'id':id},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_staff_department_data(request, id):
    global y
    if request.method == "POST":
        users = json.loads(request.POST.get("users", ""))
        if len(users) == 0:
            return HttpResponse(status=400, content=json.dumps({"Error":"Ошибка! Выберите хотя бы одного сотрудника!"})) 
    else:
        return HttpResponse(status=500, content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
    for user in users:
        m_user = Staff.objects.get(id=int(user))
        info = y.modal_staff(str(user))
        payload_dict = {
            "contacts": [
                {
                "type": "email",
                "value": m_user.email,
                }
            ],
            "departmentId": id,
            "name": {
                "first": info.get("name")["first"],
                "last": info.get("name")["last"],
            },
        }
        result = y.modal_add_staff_department_data(user, payload_dict)
        if result[1] != False:
            m_user.departmentId = id
            m_user.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=result[0], content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
    return HttpResponse(status=200)

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_department(request, id):
    domain = "@"+Domains.objects.get(isMaster = True).name
    current_department = Departments.objects.get(id=id)
    return render(
        request,
        'modal_change_department.html',
        context={'domain':domain, 'id':id, 'name':current_department.name, 'description':current_department.description, 'label':current_department.label},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_department_data(request, id):
    global y
    m_department = Departments.objects.get(id=id)
    name=description=label=""
    if request.method == "POST":
        name = str(request.POST.get("name", ""))
        description = str(request.POST.get("description", ""))
        label = str(request.POST.get("label", ""))
    else:
        return HttpResponse(status=500)
    payload_dict = {
        "description": description,
        "label": label,
        "name": name,
        "parentId": m_department.parentId
    }
    result = y.modal_change_department_data(payload_dict, id)
    if result[1] != False:
        m_department.name = name
        m_department.description = description
        m_department.label = label
        m_department.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_department(request, id):
    department = Departments.objects.get(id=id)
    return render(
        request,
        'modal_delete_department.html',
        context={'id':id, 'department':department.name},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_department_data(request, id):
    global y
    result = y.modal_delete_department_data(id)
    if result[1] != False:
        Departments.objects.get(id=id).delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_department_staff(request, departmentId):
    staffId = ""
    if request.method == "POST":
        staffId = str(request.POST.get("staffId", ""))
    else:
        return HttpResponse(status=500)
    department = Departments.objects.get(id=departmentId)
    staff = Staff.objects.get(id=staffId)
    return render(
        request,
        'modal_delete_department_staff.html',
        context={'user':staff.name, 'department':department.name,'departmentId':departmentId, 'staffId':staffId},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_department_staff_data(request, id):
    global y
    staffId = ""
    if request.method == "POST":
        staffId = str(request.POST.get("staffId", ""))
    else:
        return HttpResponse(status=500)
    user = y.modal_staff(staffId)
    payload_dict = {
        "contacts": [{
            "type": "email",
            "value": user.get("email")
            }],
        "departmentId": 1,
        "name": {
            "first": user.get("name")["first"],
            "last": user.get("name")["last"],
        },
    }
    result = y.change_user(staffId, payload_dict)
    if result[1] != False:
        staff = Staff.objects.get(id=staffId)
        staff.departmentId = 1
        staff.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])
    

#Groups
@csrf_protect
@csrf_exempt
@login_required
def groups(request):
    base_groupsId = list(Groups_Hierarchy.objects.filter(parentId=None).values_list("childId", flat=True))
    result=[]
    for base_groupId in base_groupsId:
        base_group = Groups.objects.get(id=base_groupId)
        result.append([base_group.id, base_group.name])
    return render(
        request,
        'groups.html',
        context={'groups':result,'total':Groups.objects.all().count()},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def groups_create(request, id):
    level=levelFormat(request)
    children = list(Groups_Members.objects.filter(groupId=id, memberType="group").values_list("memberId", flat=True))
    users = list(Groups_Members.objects.filter(groupId=id, memberType="user").values_list("memberId", flat=True))
    groupsResult=[]
    usersResult=[]
    for child in children:
        group = Groups.objects.get(id=child)
        groupsResult.append([group.id, group.name])
    for user in users:
        if user_main_group(id, user):
            info = Staff.objects.get(id=user)
            img = avatarFormat(info.img)
            usersResult.append([info.id, info.name, info.email, img, id])
    return render(
        request,
        'groups_create.html',
        context={'groups':groupsResult, 'users':usersResult,'level':level},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_group(request, id):
    domain = "@"+Domains.objects.get(isMaster = True).name
    return render(
        request,
        'modal_add_group.html',
        context={'domain':domain, 'id':id},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_group_data(request, id):
    global y
    name=description=label=""
    if request.method == "POST":
        name = str(request.POST.get("name", ""))
        if name == "" or name == None:
            return HttpResponse(status=400, content=json.dumps({"Error":["group-name-add"]}))
        description = str(request.POST.get("description", ""))
        label = str(request.POST.get("label", ""))
    else:
        return HttpResponse(status=500, content=json.dumps({}))
    payload_dict = {
        "adminIds": [],
        "description": description,
        "externalId": None,
        "label": label,
        "members": [],
        "name": name
    }
    result = y.modal_add_group_data(payload_dict)
    if result[1] != False:
        if int(id) != 0:
            parent_dict = {
                "id": result[0]["id"],
                "type": "group"
            }
            parent = y.modal_add_group_member(id, parent_dict)
            if parent[1] != False:
                m_group = Groups()
                m_group.id = result[0]["id"]
                m_group.name = name
                m_group.membersCount = 0
                m_group.label = label
                m_group.save()
                m_parent = Groups.objects.get(id=id)
                m_parent.membersCount = m_parent.membersCount + 1
                m_parent.save()
                m_group_hierarchy = Groups_Hierarchy()
                m_group_hierarchy.parentId = Groups.objects.get(id=id)
                m_group_hierarchy.childId = result[0]["id"]
                m_group_hierarchy.save()
                m_group_members = Groups_Members()
                m_group_members.groupId = Groups.objects.get(id=id)
                m_group_members.memberId = result[0]["id"]
                m_group_members.memberType = "group"
                m_group_members.save()
                HttpResponse(status=200, content=json.dumps({}))
            else:
                return HttpResponse(status=parent[0])
        else:
            m_group = Groups()
            m_group.id = result[0]["id"]
            m_group.name = name
            m_group.membersCount = 0
            m_group.label = label
            m_group.save()
            m_group_hierarchy = Groups_Hierarchy()
            m_group_hierarchy.parentId = None
            m_group_hierarchy.childId = result[0]["id"]
            m_group_hierarchy.save()
            return HttpResponse(status=200)
    else:
        message = "Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже. "
        try:
            message = error_messages[result[2]["message"]]
        except Exception:
            pass
        return HttpResponse(status=result[0], content=json.dumps({"Error":message}))

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_staff_group(request, id):
    not_free_users = list(Groups_Staff.objects.filter(groupId=id).values_list("staffId"))
    all_users = list(Staff.objects.values_list("id"))
    free_users = []
    for all_user in all_users:
        if not all_user in not_free_users:
            free_users.append(all_user)
    usersResult=[]
    empty = False
    for free_user in free_users:
        user = Staff.objects.get(id=free_user[0])
        img = avatarFormat(user.img)
        usersResult.append([user.id, user.name, user.email, img])
    if len(usersResult) == 0:
        empty = True
    return render(
        request,
        'modal_add_staff_group.html',
        context={'users':usersResult, 'empty':empty, 'id':id},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_add_staff_group_data(request, id):
    global y
    if request.method == "POST":
        users = json.loads(request.POST.get("users", []))
        if len(users) == 0:
            return HttpResponse(status=400, content=json.dumps({"Error":"Ошибка! Выберите хотя бы одного сотрудника!"}))    
    else:
        return HttpResponse(status=500, content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
    for user in users:
        payload_dict = {
                "id": str(user),
                "type": "user"
            }
        result = y.modal_add_group_member(id, payload_dict)
        if result[1] != False:
            m_group = Groups.objects.get(id=id)
            m_group.membersCount = m_group.membersCount + 1
            m_group.save()
            m_group_staff = Groups_Staff()
            m_group_staff.staffId = Staff.objects.get(id=int(user))
            m_group_staff.groupId = Groups.objects.get(id=int(id))
            m_group_staff.save()
            m_group_members = Groups_Members()
            m_group_members.groupId = Groups.objects.get(id=int(id))
            m_group_members.memberId = int(user)
            m_group_members.memberType = "user"
            m_group_members.save()
            parents = find_group_parents(id)
            for parent in parents:
                m_parent = Groups.objects.get(id=parent)
                m_parent.membersCount = m_group.membersCount + 1
                m_parent.save()
                m_parent_staff = Groups_Staff()
                m_parent_staff.staffId = Staff.objects.get(id=int(user))
                m_parent_staff.groupId = Groups.objects.get(id=int(parent))
                m_parent_staff.save()
                m_parent_members = Groups_Members()
                m_parent_members.groupId = Groups.objects.get(id=int(parent))
                m_parent_members.memberId = int(user)
                m_parent_members.memberType = "user"
                m_parent_members.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=result[0], content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
            

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_group(request, id):
    domain = "@"+Domains.objects.get(isMaster = True).name
    current_group = Groups.objects.get(id=id)
    return render(
        request,
        'modal_change_group.html',
        context={'domain':domain, 'id':id, 'name':current_group.name, 'description':current_group.description, 'label':current_group.label},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_change_group_data(request, id):
    global y
    m_group = Groups.objects.get(id=id)
    name=description=label=""
    if request.method == "POST":
        name = str(request.POST.get("name", ""))
        description = str(request.POST.get("description", ""))
        label = str(request.POST.get("label", ""))
    else:
        return HttpResponse(status=500)
    payload_dict = {
        "adminIds": [],
        "description": description,
        "externalId": None,
        "label": label,
        "members":[],
        "name": name
    }
    result = y.modal_change_group_data(payload_dict, id)
    if result[1] != False:
        m_group.name = name
        m_group.description = description
        m_group.label = label
        m_group.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_group(request, id):
    group = Groups.objects.get(id=id)
    return render(
        request,
        'modal_delete_group.html',
        context={'id':id, 'group':group.name},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_group_data(request, id):
    global y
    members = y.modal_get_group_members(str(id))
    for user in members["users"]:
        try:
            Groups_Staff.objects.get(staffId = user["id"], groupId = id).delete()
            Groups_Members.objects.get(memberId = user["id"], groupId = id).delete()
        except ObjectDoesNotExist:
            pass
    try:
        parentId = Groups_Members.objects.get(memberId = id)
        parent = Groups.objects.get(id=parentId.groupId.id)
        parent.membersCount = parent.membersCount - 1
        parent.save()
    except ObjectDoesNotExist:
        pass
    result = delete_group(id)
    if result[1]:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_group_staff(request, groupId):
    staffId = ""
    if request.method == "POST":
        staffId = str(request.POST.get("staffId", ""))
    else:
        return HttpResponse(status=500)
    group = Groups.objects.get(id=groupId)
    staff = Staff.objects.get(id=staffId)
    return render(
        request,
        'modal_delete_group_staff.html',
        context={'user':staff.name, 'group':group.name,'groupId':groupId, 'staffId':staffId},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_delete_group_staff_data(request, groupId):
    global y
    staffId = ""
    if request.method == "POST":
        staffId = str(request.POST.get("staffId", ""))
    else:
        return HttpResponse(status=500)
    result = y.delete_group_member(groupId, "user", staffId)
    if result[1]:
        Groups_Staff.objects.get(groupId=groupId, staffId=staffId).delete()
        Groups_Members.objects.get(groupId=groupId, memberId=staffId).delete()
        parents = find_group_parents(groupId)
        for parent in parents:
            Groups_Staff.objects.get(groupId=parent, staffId=staffId).delete()
            Groups_Members.objects.get(groupId=parent, memberId=staffId).delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=result[0])

#Searches
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def department_lookup(request):
    value = ""
    if request.method == "POST":
        value = str(request.POST.get("value", ""))
    else:
        return HttpResponse(status=500)
    departments = list(Departments.objects.filter(name__iregex = value).values_list("id", flat=True))
    main_department = Departments.objects.get(parentId=0)
    main_department_result=[main_department.id, main_department.name]
    result = department_lookup_process(departments, False)
    return render(
        request,
        'union_lookup.html',
        context={'main':["department", main_department_result], 'result':result},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def department_staff_lookup(request):
    value = ""
    if request.method == "POST":
        value = str(request.POST.get("value", ""))
    else:
        return HttpResponse(status=500)
    departments = list(Staff.objects.filter(name__iregex = value).values_list("departmentId", flat=True))
    main_department = Departments.objects.get(parentId=0)
    main_department_result=[main_department.id, main_department.name]
    result = department_lookup_process(departments, True)
    return render(
        request,
        'union_lookup.html',
        context={'main':["department", main_department_result], 'result':result},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def group_lookup(request):
    value = ""
    if request.method == "POST":
        value = str(request.POST.get("value", ""))
    else:
        return HttpResponse(status=500)
    groups = list(Groups.objects.filter(name__iregex = value).values_list("id", flat=True))
    result = group_lookup_process(groups, False)
    return render(
        request,
        'union_lookup.html',
        context={'main':["group", []], 'result':result},
    )
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def group_staff_lookup(request):
    value = ""
    if request.method == "POST":
        value = str(request.POST.get("value", ""))
    else:
        return JsonResponse({'status':False, "result":[]})
    staff = list(Staff.objects.filter(name__iregex = value))
    groups = []
    for user in staff:
        try:
            m_groups = Groups_Staff.objects.filter(staffId = user)
            for m_group in m_groups:
                groups.append(m_group.groupId.id)
        except ObjectDoesNotExist:
            pass
    result = group_lookup_process(groups, True)
    return render(
        request,
        'union_lookup.html',
        context={'main':["group", []], 'result':result},
        )

#Utils
def avatarFormat(id):
    global avatarSrc
    img = avatarSrc.format("null")
    if id != "0":
        img = avatarSrc.format(id)
    return img

def levelFormat(request): #увеличивает число уровня на 1 (list-item0 -> list-item1), list-item4 - максимальный уровень
    level="list-item0"
    if request.method == "POST":
        level = str(request.POST.get("level", False))[:-8]
        if level != "list-item4":
            level = re.sub('\d+(?!.*\d)', lambda d: str(int(d[0]) + 1), level)
    return level
def department_level(id,staff): #устанавливает уровень для подразделения
    parents = find_department_parents(id)
    level="list-item0"
    if len(parents) < 4:
        if staff:
            return re.sub('\d+(?!.*\d)', lambda d: str(int(d[0]) + len(parents) + 1), level)
        else:
            return re.sub('\d+(?!.*\d)', lambda d: str(int(d[0]) + len(parents)), level)
    else:
        return "list-item4"

def group_level(id,staff): #устанавливает уровень для группы
    parents = find_group_parents(id)
    level="list-item0"
    if len(parents) < 4:
        if staff:
            return re.sub('\d+(?!.*\d)', lambda d: str(int(d[0]) + len(parents) + 1), level)
        else:
            return re.sub('\d+(?!.*\d)', lambda d: str(int(d[0]) + len(parents)), level)
    else:
        return "list-item4"

def delete_group(id): #кроме самой группы удаляет и всех потомков 
    global y
    for member in y.modal_get_group_members(str(id))["groups"]:
        result = delete_group(member["id"])
        if result[1] == False:
            return result
    g_h = Groups_Hierarchy.objects.filter(childId = id)
    for each_g_h in g_h:
        each_g_h.delete()
    g_m = Groups_Members.objects.filter(memberId = id)
    for each_g_m in g_m:
        each_g_m.delete()
    Groups.objects.get(id=id).delete()
    return y.modal_delete_group_data(str(id))

def department_lookup_process(departments, staff): #создает удобный для html словарь подразделений с соблюдением иерархии
    result = [] #элемент словаря имеет вид: {id:[type, level, name, status]}
    #если type == "user", то вид: {id:[type, level, name, email, avatar, parentType, parentId]}
    try:
        for department in departments:
            parents = find_department_parents(department)
            if staff:
                parents.append(department)
            for parent in parents:
                parent_name = Departments.objects.get(id=parent).name
                if parent not in keys(result):
                    result.append({parent:["department", department_level(parent, False), parent_name, "clicked"]})
                else:
                    result[keys(result).index(parent)][parent] = ["department", department_level(parent, False), parent_name, "clicked"]
                r = keys(result).index(parent)
                children = find_department_children(parent)
                for child in children:
                    if child not in result:
                        result.insert(r + 1, child)
            if department not in keys(result):
                department_name = Departments.objects.get(id=department).name
                result.append({department:["department", department_level(department, False), department_name, "empty"]})
    except ObjectDoesNotExist:
        pass
    return result
    
def find_department_parents(id):
    result = []
    parentId = 0
    curentId = id
    while parentId != 1:
        try:
            parentId = Departments.objects.get(id=curentId).parentId
            curentId = parentId
            if parentId != 1:
                result.append(parentId)
        
        except ObjectDoesNotExist:
            return result[::-1]
    return result[::-1]

def find_department_children(id):
    result = []
    children = list(Departments.objects.filter(parentId = id).values_list("id", "name"))
    bio = list(Staff.objects.filter(departmentId = id).values_list("id", "name", "email", "img"))
    for child in children:
        result.append({child[0]:["department", department_level(child[0], False), child[1], "empty"]})
    for user in bio:
        result.append({user[0]:["user", department_level(id, True)+"-user", user[1], user[2], avatarFormat(user[3]), "department", id]})
    return result[::-1]

def group_lookup_process(groups, staff): #аналогично department_lookup_process
    result = []
    try:
        for group in groups:
            parents = find_group_parents(group)
            if staff:
                parents.append(group)
            for parent in parents:
                parent_name = Groups.objects.get(id=parent).name
                if parent not in keys(result):
                    result.append({parent:["group", group_level(parent, False), parent_name, "clicked"]})
                else:
                    result[keys(result).index(parent)][parent] = ["group", group_level(parent, False), parent_name, "clicked"]
                r = keys(result).index(parent)
                children = find_group_children(parent)
                for child in children:
                    if child not in result and list(child.keys())[0] not in keys(result):
                        result.insert(r + 1, child)
            if group not in keys(result):
                group_name = Groups.objects.get(id=group).name
                result.append({group:["group", group_level(group, False), group_name, "empty"]})
    except ObjectDoesNotExist:
        pass
    return result

def find_group_parents(id):
    result = []
    parentId = 0
    curentId = id
    while parentId != None:
        try:
            parentId = Groups_Hierarchy.objects.get(childId=curentId).parentId
            curentId = parentId.id
            if parentId != None:
                result.append(parentId.id)
        except (ObjectDoesNotExist, AttributeError) as e:
            return result[::-1]
    return result[::-1]

def find_group_children(id):
    result = []
    children_groups = list(Groups_Members.objects.filter(groupId = Groups.objects.get(id=id), memberType="group").values_list("memberId", flat=True))
    children_users = list(Groups_Members.objects.filter(groupId = Groups.objects.get(id=id), memberType="user").values_list("memberId", flat=True))
    for group in children_groups:
        group_name = Groups.objects.get(id=group).name
        result.append({group:["group", group_level(group, False), group_name, "empty"]})
    for user in children_users:
        if user_main_group(id, user):
            m_user = Staff.objects.get(id=user)
            result.append({user:["user", group_level(id, True)+"-user", m_user.name, m_user.email, avatarFormat(m_user.img), "group", id]})
    return result[::-1]

def keys(array): #для получения списка ключей словаря
        keys = []
        for d in array:
            keys.append(list(d.keys())[0])
        return keys

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def close_unit(request, id): #запрос списка юнитов, которые нужно удалить(закрыть) onclick на родителя, реализация в multilevel_list.js
    type_=""
    if request.method == "POST":
        type_ = str(request.POST.get("type", ""))
    else:
        return JsonResponse({'status':False, "result":[]})
    result = []
    if type_ == "department":
        result = close_department(id, [])
    elif type_ == "group":
        result = close_group(id, [])
    else:
        return JsonResponse({'status':False, 'result':result})
    return JsonResponse({'status':True, 'result':result})


def close_department(id, result):
    departments = list(Departments.objects.filter(parentId=id).values_list("id", flat=True))
    for department in departments:
        result.append(department)
        close_department(department, result)
    return result

def close_group(id, result):
    groups = list(Groups_Hierarchy.objects.filter(parentId=Groups.objects.get(id=id)).values_list("childId", flat=True))
    for group in groups:
        result.append(group)
        close_group(group, result)
    return result

def user_main_group(groupId, staffId): #проверка, ближайшая ли группа для заданного id юзера
    groups = list(Groups_Staff.objects.filter(staffId=Staff.objects.get(id=staffId)).values_list("groupId", flat=True))
    children = list(Groups_Hierarchy.objects.filter(parentId = Groups.objects.get(id=groupId)).values_list("childId", flat=True))
    for group in groups:
        if group in children:
            return False            
    return True




#ver2
@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_paste(request, id):
    type = ""
    if request.method == "POST":
        type = str(request.POST.get("type", ""))
    else:
        return JsonResponse({'status':False, "result":[]})
    
    typeFormat = ""
    unit = []
    if type == "department":
        departments = list(Departments.objects.filter(~Q(id=id)).values_list("id", "name").order_by("name"))
        groups = list(Groups.objects.values_list("id", "name").order_by("name"))
        typeFormat = "подразделение"
        unit.append(id)
        unit.append(Departments.objects.get(id=id).name)
    else:
        departments = list(Departments.objects.values_list("id", "name").order_by("name"))
        groups = list(Groups.objects.filter(~Q(id=id)).values_list("id", "name").order_by("name"))
        typeFormat = "группу"
        unit.append(id)
        unit.append(Groups.objects.get(id=id).name)
    
    return render(
        request,
        'modal_paste.html',
        context={'type':type, 'typeFormat':typeFormat, 'unit':unit, 'departments':departments, 'groups':groups},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_paste_show_department(request, id): #получаем сотрудников подразделения, которые можно вставить в юнит
    unitForType = "" #тип юнита (подразделение/группа), в который нужно добавить сотрудников
    unitFor = "" #id юнита, в который нужно добавить сотрудников
    if request.method == "POST":
        unitForType = str(request.POST.get("type", ""))
        unitFor = str(request.POST.get("for", ""))
    else: 
        return HttpResponse(status=500)
    usersAlready=[] #список id сотрудников, которые уже в подразделении
    usersAlreadyResult=[] #список сотрудников, которые уже в подразделении
    if unitForType == "group": #для групп нужно проверять потомков, т.к. пользователи могут быть в нескольких группах одновременно
        usersAlready = list(Groups_Staff.objects.filter(groupId=unitFor).values_list("staffId", flat=True))
        children_groups = list(Groups_Members.objects.filter(groupId = Groups.objects.get(id=unitFor), memberType="group").values_list("memberId", flat=True))
        for children_group in children_groups:
            children_users = list(Groups_Staff.objects.filter(groupId=children_group).values_list("staffId", flat=True))
            for children_user in children_users:
                if children_user not in usersAlready:
                    usersAlready.append(children_user)
    users = list(Staff.objects.filter(departmentId=id).values_list("id", "name", "email", "img"))
    usersResult=[] #список сотрудников, которых можно добавить
    empty = False
    for user in users:
        img = avatarFormat(user[3])
        if user[0] not in usersAlready:
            usersResult.append([user[0], user[1], user[2], img])
        else:
            usersAlreadyResult.append([user[0], user[1], user[2], img])
    if len(usersResult) == 0 and len(usersAlreadyResult) == 0:
        empty = True
    return render(
        request,
        'modal_paste_show_unit.html',
        context={'users':usersResult, 'empty':empty, 'type':"department",'forType':unitForType, 'usersAlready':usersAlreadyResult},
    )

@csrf_protect
@csrf_exempt
@login_required
@apply_permissions
def modal_paste_show_group(request, id): #получаем сотрудников группы, которые можно вставить в юнит
    unitForType = "" #тип юнита (подразделение/группа), в который нужно добавить сотрудников
    unitFor = "" #id юнита, в который нужно добавить сотрудников
    if request.method == "POST":
        unitForType = str(request.POST.get("type", ""))
        unitFor = str(request.POST.get("for", ""))
    else: 
        return HttpResponse(status=500)
    users = list(Groups_Staff.objects.filter(groupId=id).values_list("staffId", flat=True))
    usersResult=[] #список сотрудников, которых можно добавить
    usersAlready=[] #список id сотрудников, которые уже в группе
    usersAlreadyResult=[] #список сотрудников, которые уже в группе
    if unitForType == "group": #для групп нужно проверять потомков, т.к. пользователи могут быть в нескольких группах одновременно
        usersAlready = list(Groups_Staff.objects.filter(groupId=unitFor).values_list("staffId", flat=True))
        children_groups = list(Groups_Members.objects.filter(groupId = Groups.objects.get(id=unitFor), memberType="group").values_list("memberId", flat=True))
        for children_group in children_groups:
            children_users = list(Groups_Staff.objects.filter(groupId=children_group).values_list("staffId", flat=True))
            for children_user in children_users:
                if children_user not in usersAlready:
                    usersAlready.append(children_user)

    else: #для подзразделения достаточно получить список входящих сотрудников
        usersAlready = list(Staff.objects.filter(departmentId=unitFor).values_list("id", flat=True))
    empty = False
    for user in users:
        m_user = Staff.objects.get(id=user)
        img = avatarFormat(m_user.img)
        if user not in usersAlready:
            usersResult.append([m_user.id, m_user.name, m_user.email, img])
        else:
            usersAlreadyResult.append([m_user.id, m_user.name, m_user.email, img])
    if len(usersResult) == 0 and len(usersAlreadyResult) == 0:
        empty = True
    return render(
        request,
        'modal_paste_show_unit.html',
        context={'users':usersResult, 'empty':empty, 'type':"group", 'forType':unitForType, 'usersAlready':usersAlreadyResult},
    )


@csrf_protect
@csrf_exempt
@login_required
def modal_paste_department(request, id):
    global y
    users = []
    if request.method == "POST":
        users = json.loads(request.POST.get("users", []))
        if len(users) == 0:
            return HttpResponse(status=400, content=json.dumps({"Error":"Ошибка! Выберите хотя бы одного сотрудника!"}))  
    for user in users:
        m_user = Staff.objects.get(id=int(user))
        info = y.modal_staff(str(user))
        payload_dict = {
            "contacts": [
                {
                "type": "email",
                "value": m_user.email,
                }
            ],
            "departmentId": id,
            "name": {
                "first": info.get("name")["first"],
                "last": info.get("name")["last"],
            },
        }
        result = y.change_user(user, payload_dict)
        if result[1] != False:
            m_user.departmentId = id
            m_user.save()
        else:
            return HttpResponse(status=result[0], content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
    return HttpResponse(status=200)
            
            
            


@csrf_protect
@csrf_exempt
@login_required
def modal_paste_group(request, id):
    global y
    users = []
    if request.method == "POST":
        users = json.loads(request.POST.get("users", []))
        if len(users) == 0:
            return HttpResponse(status=400, content=json.dumps({"Error":"Ошибка! Выберите хотя бы одного сотрудника!"}))  
    for user in users:
        payload_dict = {
                "id": str(user),
                "type": "user"
            }
        result = y.modal_add_group_member(id, payload_dict)
        if result[1] != False: #добавляем сотрудников и в родительские группы
            m_group = Groups.objects.get(id=id)
            m_group.membersCount = m_group.membersCount + 1
            m_group.save()
            m_group_staff = Groups_Staff()
            m_group_staff.staffId = Staff.objects.get(id=int(user))
            m_group_staff.groupId = Groups.objects.get(id=int(id))
            m_group_staff.save()
            m_group_members = Groups_Members()
            m_group_members.groupId = Groups.objects.get(id=int(id))
            m_group_members.memberId = int(user)
            m_group_members.memberType = "user"
            m_group_members.save()
            parents = find_group_parents(id)
            for parent in parents:
                m_parent = Groups.objects.get(id=parent)
                m_parent.membersCount = m_group.membersCount + 1
                m_parent.save()
                m_parent_staff = Groups_Staff()
                m_parent_staff.staffId = Staff.objects.get(id=int(user))
                m_parent_staff.groupId = Groups.objects.get(id=int(parent))
                m_parent_staff.save()
                m_parent_members = Groups_Members()
                m_parent_members.groupId = Groups.objects.get(id=int(parent))
                m_parent_members.memberId = int(user)
                m_parent_members.memberType = "user"
                m_parent_members.save()
        else:
            return HttpResponse(status=result[0], content=json.dumps({"Error":"Произошла непредвиденная ошибка, попробуйте изменить данные или отправить запрос позже."}))
    return HttpResponse(status=200)
