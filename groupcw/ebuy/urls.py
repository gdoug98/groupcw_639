from django.urls import path
from . import views

app_name = 'ebuy'
urlpatterns = [
	path('', views.redirectPage, name='redirectPage'),
	path('index/', views.index, name='index'),
	path('additems/', views.add_items, name='add_items'),
	path('loginpage/', views.logInPage, name='logInPage'),
	path('addauctionpage/', views.addAuctionPage, name='addAuctionPage'),
	path('closedauctions/', views.load_closed_auctions, name='closed_auctions'),
	path('createprofile/', views.create_profile, name='create_profile'),
	path('createuser/',views.createUser, name='createUser'),
	path('createitem/',views.createItem, name='createItem'),
	path('createauction/',views.createAuction, name='createAuction'),
	path('submitlogin/',views.submitLogin, name='submitLogin'),
	path('profile/<int::id>', views.view_profile, name="get_profile"),
	path('profile/', views.view_profile, name='raw_profile'),
	path('auction/', views.view_auctions, name='get_auctions'),
	path('profile/get_auction/<int:user_id>', views.auctions_by_user),
	path('logout/', views.logOut, name='logOut'),
	path('auction/<int:id>', views.view_auction, name='auction_by_id'),
	path('bid/submit/', views.createBid),
	path('searchauction/', views.searchAuctions, name="searchAuctions"),
	path('loadViewItems/', views.loadViewItems, name="loadViewItems"),
	path('listitems/', views.listitems, name="listitems"),
	path('messagetoowner/', views.messageToOwner,name="messageToOwner"),
	path('messagetocustomer/', views.messageToCustomer,name="messageToCustomer"),
#    path('items', views.items),
#    path('items/<int::id>', views.get_item, name='item_id'),
#    path('items/<int::user_id', views.item_by_user, name='user_id'),
#    path('user/authorise', views.authorise),
#    path('user/new_user', views.create_user),
#    path('auction/<int::user_id>', views.auction_by_user, name='load_auctions'),
#    path('auction/<int::id>', views.get_auction, name='get_auction')
]
