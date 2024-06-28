from bson import ObjectId
from django.contrib.auth import authenticate, login, logout;
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponse;

# database connection
import pymongo
url = "mongodb://localhost:27017"
client = pymongo.MongoClient(url)
DB = client['task_management']



def home(request):
    b = request.GET.get('q', '')
    return render(request, "home.html", {'a': b})


def read(request):

    data1 = DB.users.find_one({'email': b})
    d = data1['_id']
    data2 = DB.tasks.find({'user_id': d})

    datalist = []
    for x in data2:
        datalist.append(x)
    for x in datalist:
        DB.tasks.find_one_and_update({"_id": x['_id']}, {"$set":{"task_id": x['_id']}})


    data3 = DB.tasks.find({'user_id': d})
    dlist = []
    for x in data3:
        dlist.append(x)
    record = {
        'data': dlist,
    }

    return render(request, "read.html", record)

def create(request):
    
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        stat = request.POST.get('status')
        date = request.POST.get('date')
        
        if stat == 'Pending':
            stat1 = True
            stat2 = False
            stat3 = False
        elif stat == 'In Progress':
            stat1 = False
            stat2 = True
            stat3 = False
        elif stat == 'Completed':
            stat1 = False
            stat2 = False
            stat3 = True

        record = {
            'title': title,
            'description': desc,
            'pending': stat1,
            'in_progress': stat2,
            'completed': stat3,
            'date': date,
        }
        try:
            data = DB.users.find_one({'email': b})

            record['user_id'] = data['_id']
            DB.tasks.insert_one(record)
            return redirect("/dashboard/")
           
        except:
            messages.warning(request, "Server Not Responding")
            return redirect("/dashboard/")
    else:
        return render(request, "create.html")



def detail(request):
    a = request.GET.get('q', '')
    data3 = DB.tasks.find_one({'_id': ObjectId(a)})

    record = {
        'data': data3,
    }

    return render(request, "detail.html", record)

def signin(request):
    if request.method == "POST":
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Mongodb -----------
        record = {
            'first_name': fn,
            'last_name': ln,
            'email': email,
            'password': password,
        }
        try:
            global b
            b = email
            x = DB.users.find_one({"email":email})
            if not x:
                DB.users.insert_one(record)
                return redirect("/dashboard/")
            else:
                raise Exception
        except:
            messages.warning(request, "Already used email")
            return render(request, 'sign_in.html')
        
    else:
        return render(request, "sign_in.html")
    

def login(request):
    if request.method == "POST":
        em = request.POST.get('em')
        pswd = request.POST.get('pswd')

        try:
            global b
            a = DB.users.find_one({'email': em})
            b = a['email']
            if a['password'] != pswd:
                raise Exception
            
            return redirect("/dashboard/")
        except:
            messages.warning(request, "Invalid ID or Password")
            return render(request, 'log_in.html')

        
    else:
        return render(request, "log_in.html")
    
def dashboard(request):
    p = 0
    q = 0
    r = 0

    data1 = DB.users.find_one({'email': b})
    d = data1['_id']
    data2 = DB.tasks.find({'user_id': d})

    for x in data2:
        if x['pending']:
            p += 1
        elif x['in_progress']:
            q += 1
        elif x['completed']:
            r += 1
    
    return render(request, "dashboard.html", {'p': p, 'q': q, 'r': r})

def update(request):
    a = request.GET.get('q', '')
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        stat = request.POST.get('status')
        date = request.POST.get('date')
        
        if stat == 'Pending':
            stat1 = True
            stat2 = False
            stat3 = False
        elif stat == 'In Progress':
            stat1 = False
            stat2 = True
            stat3 = False
        elif stat == 'Completed':
            stat1 = False
            stat2 = False
            stat3 = True

        record = {
            'title': title,
            'description': desc,
            'pending': stat1,
            'in_progress': stat2,
            'completed': stat3,
            'date': date,
        }
        try:
            DB.tasks.find_one_and_update({'_id': ObjectId(a)}, {'$set': 
                {
                'title': title,
                'description': desc,
                'pending': stat1,
                'in_progress': stat2,
                'completed': stat3,
                'date': date,
                }
            })
            return redirect("/dashboard/")
           
        except:
            messages.warning(request, "Server Not Responding")
            return redirect("/dashboard/")
    
    else:
        
        data3 = DB.tasks.find_one({'_id': ObjectId(a)})

        record = {
            'data': data3,
        }
        return render(request, "update.html", record)


def delete(request):
    a = request.GET.get('q', '')
    DB.tasks.delete_one({'_id': ObjectId(a)})
    return redirect("/dashboard/")

