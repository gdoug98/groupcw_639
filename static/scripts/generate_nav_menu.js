$(document).ready(function()
{
	$menuItems = ["Log In/Register", "View Auctions", "My Auctions", "My Bids", "View Profile", "Add Item", "Log Out"]
	//$correspondingLinks = []
	
	$('#generateMenuItems').html("<ul class='navbar-nav'>")
	for(var i=0; i<$menuItems.length; i++)
	{
		$('#generateMenuItems').append("<li class='nav-item'>")
		$('#generateMenuItems').append("<a class='nav-link' href='#'>") //just using a dummy link for now
		$('#generateMenuItems').append($menuItems[i] + "</a></li>")
	}	
	$('#generateMenuItems').append("</ul>")	
});
