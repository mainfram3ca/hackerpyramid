function HandleUpdate(Data) {
	Ti.API.debug(Data);
	if (typeof Data.scores != "undefined") {
			var tbl_data = [];
            for (var i=0; i < Data.scores.length; i++) {                                              
			    var row = Ti.UI.createTableViewRow();
			    var label = Ti.UI.createLabel({
			        left: 10,
			        color: 'black',
			        text: Data.scores[i]['name']
			    });
			    var label2 = Ti.UI.createLabel({
			        right: 10,
			        color: 'black',
			        text: Data.scores[i]['score']
			    });
			    row.add(label);
			    row.add(label2);
			    tbl_data.push(row);
			}
			PennyView_Scores.setData(tbl_data);
	}	
	if (typeof Data.catagories != "undefined") {
	    catagories = Data.catagories[0]['title'];                                                           
        for (var i=1; i < Data.catagories.length; i++) { // >                                              
            catagories = catagories + "\n" + Data.catagories[i]['title'];                                     
        }
		Label_List_Categories.text = catagories;
		PennyView.visible = false;
		WordView.visible = false;
		CategoryView.visible = true;
	}
	if (typeof Data.timer != "undefined") {
		Label_Time.text = "Time Left: " + Data.timer;
	}
	if (typeof Data.state != "undefined") {
		switch(Data['state']) {
			case 0:
				// Show penny screen
				CategoryView.visible = false;
				WordView.visible = false;
				PennyView.visible = true;
				break;
			case 3:
				// show the word screen
				// Reset the view first
				Label_Time.left = Titanium.Platform.displayCaps.platformWidth - 200;
				Label_Word.top = Titanium.Platform.displayCaps.platformHeight / 2 - 30;
	
				Label_Category.text = "Category is: " + Data['catagory'];
				Label_Word.text = Data['word'];
				PennyView.visible = false;
				CategoryView.visible = false;
				WordView.visible = true;
				break;
		}
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
