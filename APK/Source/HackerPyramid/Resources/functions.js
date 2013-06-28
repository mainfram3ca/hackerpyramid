function HandleUpdate(Data) {
	Ti.API.debug(Data);
	switch(Data['view']) {
		case 0:
			// Show penny screen
			CategoryView.visible = false;
			WordView.visible = false;
			PennyView.visible = true;
			break;
		case 1:
			// show the category screen
		    catagories = Data['catagory'][0]['name']                                                               
            for (var i=1; i < Data['catagory'].length; i++) { // >                                              
                catagories = catagories + "\n" + Data['catagory'][i]['name']                                     
            }
			Label_List_Categories.text = catagories
			PennyView.visible = false;
			WordView.visible = false;
			CategoryView.visible = true;
			break;
		case 2:
			// show the word screen
			// Reset the view first
			Label_Time.left = Titanium.Platform.displayCaps.platformWidth - 200
			Label_Word.top = Titanium.Platform.displayCaps.platformHeight / 2 - 30

			Label_Category.text = "Category is: " + Data['catagory']
			Label_Word.text = Data['word']
			Label_Time.text = "Time Left: " + Data['time']
			PennyView.visible = false;
			CategoryView.visible = false;
			WordView.visible = true;
			break;
	}
}

//=============================================================================
// screenWidth - return screen width in inches
//=============================================================================
function screenWidth()
{
    return Titanium.Platform.displayCaps.platformWidth / Titanium.Platform.displayCaps.dpi;
}

//=============================================================================
// screenHeight - return screen height in inches
//=============================================================================
function screenHeight()
{
    return Titanium.Platform.displayCaps.platformHeight / Titanium.Platform.displayCaps.dpi;
}
