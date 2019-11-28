from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Item, Auction, Bid, Question
from django.template import loader
from django.shortcuts import render , get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.request import QueryDict
from django.core import serializers
from datetime import datetime
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.forms.models import model_to_dict
import datetime as D
from django.db.models import Max

def redirectPage(request):
    return redirect('/index')

def index(request):
    # user_id = request.GET['id']
    #user_id = request.session['user_id']
    # if user_id is None:
    #     id = ""
    # else:
    #      id = user_id
    context = {
		'Title': 'Ibid',
        # 'user_id': id
	}
    return render(request, 'ebuy/index.html', context)

def add_items(request):
    return render(request, 'ebuy/add_items.html')

def loadViewItems(request):
	return render(request, 'ebuy/list_items.html')

def listitems(request):
    #return a list containing all data in the table
    return JsonResponse(
    {
        'items' : list(Item.objects.values())
    })

def addAuctionPage(request):
    loggedin = is_logged_in(request)
    if loggedin == True:
        context = {
        'myitems': list(Item.objects.filter(useritem=request.session['id'])),
        }
        return render(request, 'ebuy/create_auction.html', context)
    else:
        context={
        'status': "User Not Logged In"
        }
        return render(request, 'ebuy/logInPage.html', context )


def logInPage(request):

    return render(request, 'ebuy/logInPage.html')

def load_closed_auctions(request):
    # closedauctions = getClosedAuctions(request)
    # print(closedauctions)
    # closedauctions = getClosedAuctions(request)
    # print(list(closedauctions))
    # print(list(closedauctions.auctionitem))
    closed = Auction.objects.filter(ends__lt=datetime.now())
    toreturn = []
    for auction in closed:
        try:
            bid = Bid.objects.filter(belongstoauction=auction.id).order_by('-amount')[0]
            maxBid = str(bid.amount)
            winningUser = str(bid.belongstouser.name)
        except:
            maxBid  = "No Bids Placed"
            winningUser = "No User Placed A Bid"
        toreturn.append("Auction Number: " + str(auction.id) + " | Item: " + str(auction.auctionitem.name) + " | Winning Bid: " + maxBid + " - By User: " + winningUser)
    context = {
        'auctions': toreturn,
    }
    # except:
    #     context = {
    #         'closedauctions': None,
    #     }
    #print(closedauctions)
    return render(request,'ebuy/closed_auctions.html', context)

def logOut(request):
    request.session.flush()
    return redirect('/index')


def submitLogin(request):
    print("inside submit login handler")
    email1 = request.POST['email']
    #print(email1)
    password = request.POST['password']
    #print(password)
    try:
        user1 = User.objects.get(email=email1) #if user exists
        if user1.password == password: # if their password is correct
            #print("correct password")
            request.session['email'] = email1
            request.session['password'] = password
            request.session['name'] = user1.name
            request.session['email'] = user1.name
            request.session['bankNo'] = user1.name
            request.session['phoneNo'] = user1.name
            request.session['id'] = user1.id
        else:
            return JsonResponse({
                'status': "Incorrect Password"
                })
    except:
        return JsonResponse({
            'status': "User Does Not Exist"
            })
    context = {
		'user':user1.name,
        'loggedin': True,
	}
    return JsonResponse({
        'status': "Valid User"
        })
    #response = render(request, 'ebuy/index.html', context)
    # Example Code to add any extra cookies
    # now = D.datetime.utcnow()
    # max_age = 365 * 24 * 60 * 60  #one year
    # delta = now + D.timedelta(seconds=max_age)
    # format = "%a, %d-%b-%Y %H:%M:%S GMT"
    # expires = D.datetime.strftime(delta, format)
    # response.set_cookie('User', user1.id , expires=expires)
    #return response

def create_profile(request):
	context = {
		'Title': 'Ibi'
	}
	return render(request, 'ebuy/create_profile.html', context)

def view_profile(request):
    user = getUserInfo(request)
    context = None
    if user is None:
        context = {'loggedIn': False, 'message': 'Not logged in.'}
    else:
        print("helloooo")
        userid = request.session['id']
        questions = Question.objects.filter(toUser=userid)
        print(questions)
        context = {'user' : model_to_dict(user), 'loggedIn': True, 'questions': questions, }
    return render(request, 'ebuy/view_profile.html', context)

def view_auctions(request):
    userId = request.session.get('id')
    print(userId)
    user_bids = None
    try:
        user_bids = Bid.objects.filter(belongstouser=userId)
    except:
        print('No bids')
    auction_list = Auction.objects.filter(ends__gt=datetime.now())
    bid_auctions = set([bid.belongstoauction for bid in user_bids])
    bid_auction_id = [auction.id for auction in bid_auctions]
    bid_auctions = Auction.objects.filter(id__in=auction_list)
    # print('recent auctions: '+str(bid_auctions))
    # print('all auctions: '+str(auction_list))
    context = { 'loggedIn' : True,
    'recent_auction_list' : list(bid_auctions),
    'auction_list' : list(auction_list)
    }
    if userId is None:
        context['loggedIn'] = False
    return render(request, 'ebuy/view_auctions.html', context)

def auctions_by_user(request, user_id):
    print("In views::auction_by_user")
    items = Item.objects.filter(useritem=user_id)
    auctions = Auction.objects.filter(auctionitem__in=items).values()
    print(auctions)
    print(list(auctions))
    context = {
        'items': list(auctions),
        'message': "Successfully retrieved {0} auctions".format(len(auctions))
        }
    return JsonResponse(context)

def view_auction(request, id):
    auction = getAuctionInfo(request, id)
    # item = Item.objects.get(id=auction.auctionitem.id)
    context = {
        'auction': model_to_dict(auction),
        'auctionitem': model_to_dict(auction.auctionitem),
        'messages': Question.objects.filter(aboutAuction=id)
    }
    return render(request, 'ebuy/auction_info.html', context)

def getUserInfo(request):
    print("inside getUser Data")
    userID = request.session.get('id')
    print(userID)
    try:
        getUser = User.objects.get(id=userID)
    except:
        return None
    # request.session['user_id'] = userID
    return getUser

def getItemInfo(request):
    print("inside getItemInfo Data")
    itemID = request.GET['id']
    getitem = Item.objects.get(id=itemID)
    return JsonResponse({
        'infodata': list(getItem),
    })

def getAuctionInfo(request, id):
    print("inside getauction Data")
    # auctionID = request.GET['id']
    getAuction = Auction.objects.get(id=id)
    return getAuction

def getBidInfo(request):
    print("inside get Bid Data")
    bidID = request.session['id']
    getBid = Bid.objects.get(id=bidID)
    return JsonResponse({
        'biddata': list(getBid),
    })

def createUser(request):
    print("inside create user")
    try:
        name1 = request.POST['name']
        surname1 = request.POST['surname']
        dob1 = request.POST['DOB']
        email1 = request.POST['email']
        bankno1 = request.POST['bankno']
        phoneno1 = request.POST['phoneno']
        password = request.POST['password']
        datecreated1 = datetime.now()
    except:
        return JsonResponse({
            'Status': "Input All Fields"
        })
    try:
        user = User.objects.get(email=email1)
        print("Email Exists")
        return JsonResponse({
            'Status': "User Exists"
        })
    except:
        newUser = User(name=name1, surname=surname1,password=password, dob=dob1, email=email1,bankNo=bankno1, phoneNo=phoneno1, profileCreated=datecreated1)
        newUser.save()
        print("user created")
        return JsonResponse({
            'Status': "Profile Created Succesfully",
        })

def createItem(request):
    print("inside create item")
    try:
        userID = request.session["id"]
        user1 = User.objects.get(id=userID)
    except:
        return JsonResponse({
            "status": "User Not Logged In",
        })
    name1 = request.POST['itemname']
    description1 = request.POST['itemdescription']
    condition1 = request.POST['itemcondition']
    try:
    	image1 = request.FILES['image']
    	newItem = Item(name= name1, description= description1, condition= condition1, image=image1, useritem= user1)
    except:
        newItem = Item(name= name1, description= description1, condition= condition1, useritem= user1)
    newItem.save()
    return JsonResponse({
        'itemname': name1,
	    'description': description1,
	    'condition' :condition1,
	    'belongsTo': user1.name,
        'status': "Item created succesfully"
	})

def createAuction(request):
    start = request.POST["starts"]
    end = request.POST["ends"]
    itemID = request.POST["itemID"]
    item = Item.objects.get(id=itemID)
    newAuction = Auction(starts=start,ends=end,auctionitem=item)
    newAuction.save()
    return JsonResponse({
        'startdate': start,
        'enddate': end,
        'auctionitem': item.name,
        'message': 'Auction created successfully'
    })

@csrf_exempt
def createBid(request):
    if not is_logged_in(request):
        return JsonResponse({'redirect': '/loginpage'})
    auctionID = request.POST["auctionID"]
    userID = request.POST["userID"]
    money = request.POST["amount"]
    auction = Auction.objects.get(id=auctionID)
    user = User.objects.get(id=userID)
    newBid = Bid(belongstoauction=auction,belongstouser=user,amount=money)
    newBid.save()
    return JsonResponse({
        'amount': money,
        'message': 'Bid created successfully'
    })

def is_logged_in(request):
    try:
        test = request.session.get('id')
        print(test)
        return test is not None
    except:
        return False

def searchAuctions(request):
    print("inside search auctions")
    auctionname = request.POST.get("auctionname")
    items = Item.objects.filter(name__contains = auctionname)
    #auctions = Auction.objects.filter(auctionitem__in = items).values()
    auctions = Auction.objects.filter(auctionitem__in = items).filter(ends__gt=datetime.now()).values()
    return JsonResponse({
        'filtereditems': list(Item.objects.filter(name__contains = auctionname).values()),
        'filteredauctions' : list(auctions)
    })

def messageToOwner(request):
    try:
        print("inside messageToOwner")
        auctionid = request.POST["auctionid"]
        fromuser = request.session['id']
        gettouser = Auction.objects.get(id = auctionid)
        touser = gettouser.auctionitem.useritem.id
        message1 = request.POST["message"]
        if message1 == "":
            return JsonResponse({
                'status':'Message NOT Succesful'
            })
        print(auctionid)
        print(fromuser)
        print(touser)
        print(message1)
        newMessage = Question(aboutAuction=auctionid,fromUser=fromuser,toUser=touser,message=message1,response="No Response",answered=False)
        newMessage.save()
        return JsonResponse({
            'status':'Message Succesful'
        })
    except:
        return JsonResponse({
            'status':'Message NOT Succesful'
        })


def messageToCustomer(request):
    print("inside message to customer")
    responsemessage = request.POST["message"]
    questionid = request.POST["questionid"]
    print(responsemessage)
    print(questionid)
    message = Question.objects.get(id=questionid)
    message.response = responsemessage
    message.answered = True
    message.save()
    return JsonResponse({
        'status': "response succesfull",
    })
