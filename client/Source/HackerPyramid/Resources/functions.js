function HandleUpdate(Data) {
	if (typeof Data.teams != "undefined") {
			teams = Data.teams;
	} else if (typeof Data.catagories != "undefined") {
	    catagories = Data.catagories[0]['title'];
        for (var i=1; i < Data.catagories.length; i++) {
            catagories = catagories + "\n" + Data.catagories[i]['title'];
        }
		Label_List_Categories.text = catagories;
		PennyView.visible = false;
		WordView.visible = false;
		CategoryView.visible = true;
	} else if (typeof Data.timer != "undefined") {
		Label_Time.text = "Time Left: " + Data.timer;
	} else if (typeof Data.timecode != "undefined" && presenter) {
		Label_Time.text = "Time Left: " + Data.timecode;
	} else if (typeof Data.video != "undefined" && presenter) {
				Label_Time.left = Titanium.Platform.displayCaps.platformWidth - 200;
				Label_Word.top = Titanium.Platform.displayCaps.platformHeight / 2 - 30;
				Label_Category.text = "Playing Video";
				Label_Word.text = Data.video;
				PennyView.visible = false;
				CategoryView.visible = false;
				WordView.visible = true;
	}

	// Things that can be sent with other events

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
	if (typeof Data.runtime != "undefined" && presenter) {
		Label_RunTime.text = "Run: " + Data.runtime;
	}
	if (typeof Data.word != "undefined") {
		// show the word screen
		// Reset the view first
		Label_Time.left = Titanium.Platform.displayCaps.platformWidth - 200;
		Label_Word.top = Titanium.Platform.displayCaps.platformHeight / 2 - 30;
		Label_Category.text = "Category is: " + Data['catagory'];
		Label_Word.text = Data['word'];
		PennyView.visible = false;
		CategoryView.visible = false;
		WordView.visible = true;
	}
	if (typeof Data.state != "undefined") {
		switch(Data['state']) {
			case 0:
				// Show penny screen
				CategoryView.visible = false;
				WordView.visible = false;
				PennyView.visible = true;
				break;
		}
	}
}

function ShowTeam(team) {
	Ti.API.debug(teams[team]['name']);
	TeamWindow = Titanium.UI.createWindow({
	    title: teams[team]['name']
	});

	var scrollView = Titanium.UI.createScrollView({
	    contentHeight:'auto',
	    scrollType: 'vertical'
	});

	newtop = 10;
	// Celeb
	scrollView.add(Ti.UI.createLabel({
	    top		: newtop,
	    left	: 0,
	    width	: Titanium.Platform.displayCaps.platformWidth - 10,
	    height	: 20,
	    color	: '#F0FFFF',
	    text	: teams[team]['celeb_name'] 
	)));

	newtop = newtop + 20 + 10;

	celeb_bio = Ti.UI.createLabel({
	    verticalAlign: Titanium.UI.TEXT_VERTICAL_ALIGNMENT_TOP,
	    top		: newtop,
	    left	: 0,
	    height	: Math.floor(Titanium.Platform.displayCaps.platformHeight / 2) - 20,      
	    width 	: Titanium.Platform.displayCaps.platformWidth - 10,
	    color	: '#F0FFFF',
	    text	: teams[team]['celeb_bio'] 
	});

	scrollView.add(celeb_bio);

	newtop = newtop + celeb_bio.height + 10;
	
	// Partner
	scrollView.add(Ti.UI.createLabel({
	    top		: newtop,
	    left	: 0,
	    width	: Titanium.Platform.displayCaps.platformWidth - 10,
	    height	: 20,
	    color	: '#F0FFFF',
	    text	: teams[team]['partner_name'] 
	}));

	newtop = newtop + 20 + 10;

	partner_bio = Ti.UI.createLabel({
	    verticalAlign: Titanium.UI.TEXT_VERTICAL_ALIGNMENT_TOP,
	    top		: newtop,
	    left	: 0,
	    height	: Math.floor(Titanium.Platform.displayCaps.platformHeight / 2) - 20,      
	    width	: Titanium.Platform.displayCaps.platformWidth - 10,
	    color	: '#F0FFFF',
	    text	: teams[team]['celeb_bio'] 
	});

	scrollView.add(partner_bio);

	Ti.API.info('Label size: '+JSON.stringify(partner_bio.height));
	
	newtop = newtop + partner_bio.height + 10;

	var button = Titanium.UI.createButton({
	   title: 'OK',
	   top: newtop,
	   width: 100,
	   height: 75
	});
	button.addEventListener('click',function(e) {
	   TeamWindow.close();
	   // e.source.parent.parent.close();
	});
	scrollView.add(button);

	TeamWindow.add(scrollView);
	TeamWindow.open();
}

function ShowConfig() {
	AppConfig = Titanium.UI.createWindow({
	    title: 'App Config',
	    backgroundColor: 'black'
	});

	AppConfig.orientationModes=[
	    Titanium.UI.LANDSCAPE_LEFT,
	    Titanium.UI.LANDSCAPE_RIGHT
	];

    // Endpoint
    AppConfig.add(Ti.UI.createLabel({
      top		: 10,
	  left		: 0,
      width     : Titanium.Platform.displayCaps.platformWidth - 50,
      height    : 20,      
	  color		: '#F0FFFF',
      text     : 'Websocket Endpoint (ws://host:port/ws):'
    }));
	var textArea = Ti.UI.createTextArea({
	  top          	: 50,
	  left			: 0,
	  width        	: Titanium.Platform.displayCaps.platformWidth - 50,
	  height       	: 70,
	  textAlign    	: 'left',
	  value			: Ti.App.Properties.getString('wssocket', "")
	});
	AppConfig.add(textArea);

    // Presenter
    AppConfig.add(Ti.UI.createLabel({
	  top		: 140,
      width     : Titanium.Platform.displayCaps.platformWidth - 300,
	  left		: 0,
      height    : 50,
      font		: { fontSize:36 },
	  color		: '#F0FFFF',
      text     	: 'Host Mode'
    }));

    var basicSwitch = Ti.UI.createSwitch({
	  top 	: 140,
	  left	: Titanium.Platform.displayCaps.platformWidth - 200,
      value	: Ti.App.Properties.getBool('host', false) 
	});

	AppConfig.add(basicSwitch);

    // Save
    var button = Titanium.UI.createButton({
	   title: 'Save',
	   top: 240,
	   width: 100,
	   height: 75
	});
	button.addEventListener('click',function(e)
	{
	   // Ti.App.Properties.setString(key,value);
	   Ti.App.Properties.setString("wssocket",textArea.value.toLowerCase());
	   Ti.App.Properties.setBool('host',basicSwitch.value);
	   presenter = Ti.App.Properties.getBool('host', false);
	   STARTPOINT = Ti.App.Properties.getString('wssocket', "");
	   Reconnect();
	   AppConfig.close();
	});
	AppConfig.add(button);

	AppConfig.open();
}

function Reconnect(){
	WS.close();
	startws();
}

function startws() {
	WS.open(STARTPOINT);
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

function getDate() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var month = currentTime.getMonth() + 1;
    var day = currentTime.getDate();
    var year = currentTime.getFullYear();
 
//    return month+"/"+day+"/"+year+" - "+hours +":"+minutes;
    return hours +":"+minutes;
};

function UpdateDate() {
	Label_Date.text = "Time: " + getDate();

}
