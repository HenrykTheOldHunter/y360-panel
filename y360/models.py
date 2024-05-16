from django.db import models
from .api import Yapi
from django.core.exceptions import ObjectDoesNotExist
import asyncio
from asgiref.sync import sync_to_async
y = Yapi()

class Staff(models.Model):
    id = models.IntegerField(primary_key=True, help_text="personal ID")
    name = models.CharField(max_length=200, help_text="full name")
    email = models.CharField(max_length=200, help_text="personal email")
    departmentId = models.IntegerField(help_text="ID of department")
    role = models.CharField(max_length=100, help_text="Staff or Bot or Admin")
    img = models.CharField(max_length=100, help_text="Ico ID from yandex")

    def __str__(self):
        return self.name

class Departments(models.Model):
    id = models.IntegerField(primary_key=True, help_text="department ID")
    name = models.CharField(max_length=200, help_text="department name")
    description = models.CharField(max_length=200, help_text="department description", null=True)
    parentId = models.IntegerField(help_text="parent ID")
    membersCount = models.IntegerField(help_text="count of members")
    label = models.CharField(max_length=200, help_text="email part before @", null=True)

    def __str__(self):
        return self.name

class Groups(models.Model):
    id = models.IntegerField(primary_key=True, help_text="group ID")
    name = models.CharField(max_length=200, help_text="group name")
    description = models.CharField(max_length=200, help_text="department description", null=True)
    membersCount = models.IntegerField(help_text="count of members")
    label = models.CharField(max_length=200, help_text="email part before @", null=True)

    def __str__(self):
        return self.name

class Groups_Staff(models.Model):
    staffId = models.ForeignKey('Staff', on_delete=models.CASCADE, null=True)
    groupId = models.ForeignKey('Groups', on_delete=models.CASCADE, null=True)

class Groups_Hierarchy(models.Model):
    parentId = models.ForeignKey('Groups', on_delete=models.CASCADE, null=True, help_text="id of a parent group")
    childId = models.IntegerField(help_text="id of a group")

class Groups_Members(models.Model):
    groupId = models.ForeignKey('Groups', on_delete=models.CASCADE, help_text="group ID", null=True)
    memberId = models.IntegerField(help_text="member's ID")
    memberType = models.CharField(max_length=100, help_text="group or user")

class Domains(models.Model):
    name = models.CharField(primary_key=True, max_length=200, help_text="full domain name")
    isMaster = models.BooleanField(help_text="is main or alias")

def update():
    global y
    staff_update(y)
    group_update(y)
    department_update(y)
    domain_update(y)
    print("db is ready")
     
def staff_update(y):
    staff_prepare = y.staff("1", "1")
    staff_pages = staff_prepare.get("total")
    staff = y.staff("1", str(staff_pages))
    staff_users = staff.get("users")
    staff_users_id = []
    for user in staff_users:
        m_user = Staff()
        m_user.id = int(user["id"])
        staff_users_id.append(int(user["id"]))
        m_user.name = user["name"]["first"] + " " + user["name"]["last"]
        m_user.email = user["email"]
        department = user["departmentId"]
        if department == "":
            m_user.departmentId = 0
        else:
            m_user.departmentId = int(department)
        isAdmin = user.get("isAdmin")
        isRobot = user.get("isRobot")
        if isAdmin == True:
            m_user.role = "Администратор"
        elif isRobot == True:
            m_user.role = "Бот"
        else:
            m_user.role = "Сотрудник"
        avatar = user["avatarId"]
        if avatar == "":
            m_user.img = "0"
        else:
            m_user.img = avatar

        m_user.save()


    #Groups_Staff   
    for user in staff_users:
            user_groups = user["groups"]
            pairs = []
            for user_group in user_groups:
                try:
                    Groups_Staff.objects.get_or_create(staffId = Staff.objects.get(id=user["id"]),
                                                                             groupId = Groups.objects.get(id=user_group))
                    pairs.append((user["id"], user_group))
                except ObjectDoesNotExist:
                    continue

def department_update(y):
    departments_prepare = y.departments("1", "1")
    departments_pages = departments_prepare.get("total")
    departments = y.departments("1", str(departments_pages))
    departments_departments = departments.get("departments")
    departments_id = []
    for department in departments_departments:
        m_department = Departments()
        m_department.id = int(department["id"])
        departments_id.append(int(department["id"]))
        m_department.name = department["name"]
        m_department.description = department["description"]
        m_department.parentId = int(department["parentId"])
        m_department.membersCount = int(department["membersCount"])
        m_department.label = department["label"]
        m_department.save()

def group_update(y):
    groups_prepare = y.groups("1", "1")
    groups_pages = groups_prepare.get("total")
    groups = y.groups("1", str(groups_pages))
    groups_groups = groups.get("groups")
    groups_id = []
    for group in groups_groups:
        if group.get("type") == "generic" or group.get("type") == "robots":
            m_group = Groups()
            m_group.id = int(group["id"])
            groups_id.append(int(group["id"]))
            m_group.name = group["name"]
            m_group.description = group["description"]
            m_group.membersCount = int(group["membersCount"])
            m_group.label = group["label"]
            m_group.save()

            #Groups_Hierarchy
            groups_hierarchy_pairs = []
            if not group.get("memberOf"):
                Groups_Hierarchy.objects.get_or_create(parentId=None, childId=group["id"])
                groups_hierarchy_pairs.append((None, group["id"]))
            else:
                for member in group.get("memberOf"):
                    try:
                        Groups_Hierarchy.objects.get_or_create(parentId=Groups.objects.get(id=member),
                                                                                            childId=group["id"])
                        groups_hierarchy_pairs.append((member, group["id"]))
                    except ObjectDoesNotExist:
                        continue

            #Groups_Members
            groups_members_elements = []
            if group.get("members"):
                for member in group.get("members"):
                    try:
                        Groups_Members.objects.get_or_create(groupId=Groups.objects.get(id=group["id"]),
                                                                                        memberId=member["id"],
                                                                                        memberType=member["type"])
                        groups_members_elements.append((group["id"], member["id"], member["type"]))
                    except ObjectDoesNotExist:
                        continue


def domain_update(y):
    domains_prepare = y.domains("1", "1")
    domains_pages = domains_prepare.get("total")
    domains = y.domains("1", str(domains_pages))
    domains_domains = domains.get("domains")
    domain_names = []
    for domain in domains_domains:
        m_domain = Domains()
        m_domain.name = domain["name"]
        domain_names.append(domain["name"])
        m_domain.isMaster = domain["master"]
        m_domain.save()
    for domain in list(Domains.objects.values_list("name", flat=True)):
        if domain not in domain_names:
            Domains.objects.get(name=domain).delete()
