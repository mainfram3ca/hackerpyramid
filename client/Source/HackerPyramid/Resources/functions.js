function HandleUpdate(Data) {
	if (typeof Data.scores != "undefined") {
			var tbl_data = [];
			teams = Data.scores;
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
		    if (presenter) {
				PennyView_Scores.addEventListener('click',function(e){
					ShowTeam(e.index);
				});
		    }
	} else if (typeof Data.catagories != "undefined") {
	    catagories = Data.catagories[0]['title'];                                                           
        for (var i=1; i < Data.catagories.length; i++) { // >                                              
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

function ShowTeam(team) {
	Ti.API.debug(teams[team]['name']);
	alert(teams[team]['name']);
}

function ShowConfig() {
	AppConfig = Titanium.UI.createWindow({
        title: 'App Config'
    });

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
	   Ti.App.Properties.setString("wssocket",textArea.value);
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
	WS.addEventListener('open', function () {
		Ti.API.debug('websocket opened');
	});

	WS.addEventListener('close', function (ev) {
		Ti.API.info(ev);
	});

	WS.addEventListener('error', function (ev) {
		alert(ev.error);
		
	});

	WS.addEventListener('message', function (ev) {
		Ti.API.debug(ev.data);
		HandleUpdate(JSON.parse(ev.data));
	});

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
