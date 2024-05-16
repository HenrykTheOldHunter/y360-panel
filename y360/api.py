import requests
import sys
import json
import main_settings as main

class Yapi(object):
    def __init__(self):
        self.BASE_URL='https://api360.yandex.net'
        self.API_KEY=main.API_KEY
        self.ORG_ID=main.ORG_ID
        self.BASE_HEADERS={'Authorization':f'OAuth {self.API_KEY}'}

    def staff(self, page, perPage):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users?page="+page+"&perPage="+perPage
        return self.getJSON(url, self.BASE_HEADERS)
    def modal_staff(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users/"+id
        return self.getJSON(url, self.BASE_HEADERS)
    def modal_staff_add_data(self, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users"
        return self.postJSON(url, data, self.BASE_HEADERS)
    def department(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/departments/"+id
        return self.getJSON(url, self.BASE_HEADERS)
    def departments(self, page, perPage):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/departments?page="+page+"&perPage="+perPage
        return self.getJSON(url, self.BASE_HEADERS)
    def modal_add_department_data(self, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/departments"
        return self.postJSON(url, data, self.BASE_HEADERS)
    def modal_add_staff_department_data(self, id, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users/"+id
        return self.patchJSON(url, data, self.BASE_HEADERS)
    def modal_change_department_data(self, data, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/departments/"+id
        return self.patchJSON(url, data, self.BASE_HEADERS)
    def modal_delete_department_data(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/departments/"+id
        return self.deleteJSON(url, self.BASE_HEADERS)
    def group(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id
        return self.getJSON(url, self.BASE_HEADERS)
    def groups(self, page, perPage):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups?page="+page+"&perPage="+perPage
        return self.getJSON(url, self.BASE_HEADERS)
    def group_members(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id+"/members"
        return self.getJSON(url, self.BASE_HEADERS)
    def modal_add_group_data(self, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups"
        return self.postJSON(url, data, self.BASE_HEADERS)
    def modal_add_group_member(self, id, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id+"/members"
        return self.postJSON(url, data, self.BASE_HEADERS)
    def modal_change_group_data(self, data, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id
        return self.patchJSON(url, data, self.BASE_HEADERS)
    def modal_delete_group_data(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id
        return self.deleteJSON(url, self.BASE_HEADERS)
    def modal_delete_group_members(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id+"/members"
        return self.deleteJSON(url, self.BASE_HEADERS)
    def modal_get_group_members(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id+"/members"
        return self.getJSON(url, self.BASE_HEADERS)
    def change_user(self, id, data):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users/"+id
        return self.patchJSON(url, data, self.BASE_HEADERS)
    def delete_group_member(self, id, type, memberId):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/groups/"+id+"/members/"+type+"/"+memberId
        return self.deleteJSON(url, self.BASE_HEADERS)
    def drop_2fa(self, id):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/users/"+id+"/2fa"
        return self.deleteJSON(url, {}, self.BASE_HEADERS)
    def domains(self, page, perPage):
        url=self.BASE_URL+"/directory/v1/org/"+self.ORG_ID+"/domains?page="+page+"&perPage="+perPage
        return self.getJSON(url, self.BASE_HEADERS)



    def getJSON(self, url, headers):
        self.response=requests.get(url=url, headers=headers)
        if(self.response.status_code == requests.codes.ok):
            return json.loads(self.response.text)
        else:
            print(self.response.text)
            return [self.response.status_code, False, json.loads(self.response.text)]

    def postJSON(self, url, data, headers):
        self.response=requests.post(url=url, data=json.dumps(data), headers=headers)
        if(self.response.status_code == requests.codes.ok):
            return [json.loads(self.response.text), True]
        else:
            print(self.response.text)
            return [self.response.status_code, False, json.loads(self.response.text)]

    def deleteJSON(self, url, headers):
        self.response=requests.delete(url=url, headers=headers)
        if(self.response.status_code == requests.codes.ok):
            return [json.loads(self.response.text), True]
        else:
            print(self.response.text)
            return [self.response.status_code, False]

    def patchJSON(self, url, data, headers):
        self.response=requests.patch(url=url, data=json.dumps(data), headers=headers)
        if(self.response.status_code == requests.codes.ok):
            return [json.loads(self.response.text), True]
        else:
            print(self.response.text)
            return [self.response.status_code, False, json.loads(self.response.text)]
        
    def putJSON(self, url, data, headers):
        self.response=requests.put(url=url, data=json.dumps(data), headers=headers)
        if(self.response.status_code == requests.codes.ok):
            return [json.loads(self.response.text), True]
        else:
            print(self.response.text)
            return [self.response.status_code, False, json.loads(self.response.text)]
        
