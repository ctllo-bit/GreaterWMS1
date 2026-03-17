from django.http import JsonResponse
from userprofile.models import Users
from utils.fbmsg import FBMsg
from utils.md5 import Md5
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User
from staff.models import ListModel as staff
import json, random, os
from django.conf import settings
from scanner.models import ListModel as scanner

def randomPhone():
    List = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
               "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
               "186", "187", "188", "189"]
    return (random.choice(List) + "".join(random.choice("0123456789") for i in range(8)))

randomcity = ["shanghai", "nanjing", "hangzhou", "beijing", "chongqing", "shenzhen", "guangzhou", "suzhou", "hefei",
                "chengdu", "kunming", "wuhan"]

randomcolor = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Purple"]

randomclass = ["Electronics", "Computers", "Smart Home", "Arts & Crafts", "Automotive", "Baby", "Health", "Kitchen",
               "Industrial", "Luggage", "Movies", "Software"]

randomunit = ["Box", "Package", "Piece", "Pallet"]

randomname = ["Aaron", "Abbott", "Abel", "Baird", "Baldwin", "Bancroft", "Caesar", "Calvin", "Camille", "chengdu",
              "Daisy", "Dale", "Dana", "Earl", "Eartha", "Ed", "Fabian", "Faithe", "Fanny", "Gabriel", "Gabrielle",
              "Gail", "Hale", "Haley", "Hamiltion", "Ian", "Ida", "Ina", "Jack", "Jacob", "Jacqueline", "Kama",
              "Karen", "Katherine", "Lambert", "Lance", "Larry", "Mabel", "Madeline", "Madge", "Nancy", "Naomi",
              "Nat", "Octavia", "Odelette", "Odelia", "Paddy", "Pag", "Page", "Queena", "Quennel", "Quentin",
              "Rachel", "Rae", "Ralap", "Sabina", "Sabrina", "Sally", "Tab", "Tabitha", "Tammy", "Ula", "Ulysses",
              "Una", "Valentina", "Valentine", "Valentine", "Wade", "Walker", "Wallis", "Xanthe", "Xavier", "Xaviera",
              "Yale", "Yedda", "Yehudi", "Zachary", "Zebulon", "Zenobia"
            ]

randomshape = ["Square", "Rectangle", "Cone", "Cylinder", "Irregular"]

randomspecs = ["1 x 10", "3 x 3", "5 x 5", "6 x 6"]

def randomStaffType():
    List = ["Manager", "Supervisor", "Inbound", "Outbound", "StockControl"]
    return (random.choice(List))

randombinproperty = ["Normal", "Holding", "Damage", "Inspection"]

randombinsize = ["Big", "Floor", "Tiny", "Small"]

@method_decorator(csrf_exempt, name='dispatch')
def register(request, *args, **kwargs):
    post_data = json.loads(request.body.decode())
    data = {
        "name": post_data.get('name'),
        "password1": post_data.get('password1'),
        "password2": post_data.get('password2')
    }
    ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
        'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
    if Users.objects.filter(name=str(data['name']), developer=1, is_delete=0).exists():
        err_user_same = FBMsg.err_user_same()
        err_user_same['ip'] = ip
        err_user_same['data'] = data['name']
        return JsonResponse(err_user_same)
    else:
        if data.get('password1') is None:
            err_password1_empty = FBMsg.err_password1_empty()
            err_password1_empty['ip'] = ip
            err_password1_empty['data'] = data['name']
            return JsonResponse(err_password1_empty)
        else:
            if str(data['password1']) == '':
                err_password1_empty = FBMsg.err_password1_empty()
                err_password1_empty['ip'] = ip
                err_password1_empty['data'] = data['name']
                return JsonResponse(err_password1_empty)
            else:
                if data.get('password2') is None:
                    err_password2_empty = FBMsg.err_password2_empty()
                    err_password2_empty['ip'] = ip
                    err_password2_empty['data'] = data['name']
                    return JsonResponse(err_password2_empty)
                else:
                    if str(data['password2']) == '':
                        err_password2_empty = FBMsg.err_password2_empty()
                        err_password2_empty['ip'] = ip
                        err_password2_empty['data'] = data['name']
                        return JsonResponse(err_password2_empty)
                    else:
                        if str(data['password1']) != str(data['password2']):
                            err_password_not_same = FBMsg.err_password_not_same()
                            err_password_not_same['ip'] = ip
                            err_password_not_same['data'] = data['name']
                            return JsonResponse(err_password_not_same)
                        else:
                            transaction_code = Md5.md5(data['name'])
                            user = User.objects.create_user(username=str(data['name']),
                                                            password=str(data['password1']))
                            Users.objects.create(user_id=user.id, name=str(data['name']),
                                                 openid=transaction_code, appid=Md5.md5(data['name'] + '1'),
                                                 t_code=Md5.md5(str(timezone.now())),
                                                 developer=1, ip=ip)
                            auth.login(request, user)
                            check_code = random.randint(1000, 9999)
                            staff.objects.create(staff_name=str(data['name']),
                                                 staff_type='Admin',
                                                 check_code=check_code,
                                                 openid=transaction_code)
                            user_id = staff.objects.filter(openid=transaction_code, staff_name=str(data['name']),
                                                 staff_type='Admin', check_code=check_code).first().id
                            folder = os.path.exists(os.path.join(settings.BASE_DIR, 'media/' + transaction_code))
                            if not folder:
                                os.makedirs(os.path.join(settings.BASE_DIR, 'media/' + transaction_code))
                                os.makedirs(os.path.join(settings.BASE_DIR, 'media/' + transaction_code + "/win32"))
                                os.makedirs(os.path.join(settings.BASE_DIR, 'media/' + transaction_code + "/linux"))
                                os.makedirs(os.path.join(settings.BASE_DIR, 'media/' + transaction_code + "/darwin"))
                            ret = FBMsg.ret()
                            ret['ip'] = ip
                            data['openid'] = transaction_code
                            data['name'] = str(data['name'])
                            data['user_id'] = user_id
                            data.pop('password1', '')
                            data.pop('password2', '')
                            ret['data'] = data
                            from company.models import ListModel as company
                            company.objects.create(openid=transaction_code,
                                                   company_name='GreaterWMS',
                                                   company_city=str(random.choice(randomcity)),
                                                   company_address='People’s Square # 666 Room 1F',
                                                   company_contact=str(randomPhone()),
                                                   company_manager='Elvis.Shi',
                                                   creater='DemoData'
                                                   )
                            from warehouse.models import ListModel as warehouse
                            warehouse.objects.create(openid=transaction_code,
                                                     warehouse_name='Center Warehouse',
                                                     warehouse_city=str(random.choice(randomcity)),
                                                     warehouse_address='People’s Square # 666 Room 2F',
                                                     warehouse_contact=str(randomPhone()),
                                                     warehouse_manager='Tim.Yao',
                                                     creater='DemoData'
                                                     )
                            return JsonResponse(ret)
                            