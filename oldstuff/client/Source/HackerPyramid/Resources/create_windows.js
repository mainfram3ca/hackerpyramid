// Create the main window

var MainWin = Ti.UI.createWindow({
	exitOnClose: true,
	navBarHidden : true,
	fullscreen : true,
	backgroundColor:'white'
});

// Set so that only Landscape works -- We want to force all we can.
MainWin.orientationModes=[
     Titanium.UI.LANDSCAPE_LEFT,
     Titanium.UI.LANDSCAPE_RIGHT
];

// Now, lets create some views shall we?

// How the penny looks
var Penny_fn=Ti.Filesystem.getFile(Titanium.Filesystem.resourcesDirectory,'10kpenny.jpg');
var PennyView= Ti.UI.createView();

var PennyView_Penny = Titanium.UI.createImageView({
    image:Penny_fn,
    top:10,
    right: 10,
    left: 0,
    width:'70%'
});

if (presenter) {
	var PennyView_Scores = Titanium.UI.createTableView({
		width:'30%',
		right:0,
		borderWidth:1,
		borderColor:'black',
		height:'70%',
		top: 0
	});

	var PennyView_Info = Titanium.UI.createView({
		width:'30%',
		right:0,
		borderWidth:1,
		borderColor:'black',
		height:'30%',
		bottom: 0
	}); 
	
	var Label_Date = Ti.UI.createLabel({
		text: "Time: ",
		font:{fontSize:24,fontWeight:'bold'},
		width:'auto',
		textAlign:'left',
		top:2,
		color:'black',
		left:4
	});

	var Label_RunTime = Ti.UI.createLabel({
		text: "Run: ",
		font:{fontSize:24,fontWeight:'bold'},
		width:'auto',
		textAlign:'left',
		top:28,
		color:'black',
		left:4
	});

	PennyView_Info.add(Label_Date);
	PennyView_Info.add(Label_RunTime);

	UpdateDate();
	var myTimer = setInterval(function(){
 		UpdateDate();
	}, 60000);

} else {
	var PennyView_Scores = Titanium.UI.createTableView({
		width:'30%',
		right:0,
		borderWidth:1,
		borderColor:'black'
	});

}

PennyView_Scores.addEventListener('click',function(e){
	if (presenter) {
		ShowTeam(e.index);
	}
});

PennyView.add(PennyView_Scores);
PennyView.add(PennyView_Penny);

if (presenter) {
	PennyView.add(PennyView_Info);
}

// now the category selection screen
// should be hidden by default

var CategoryView = Ti.UI.createView();

var Label_Categories = Ti.UI.createLabel({
	text: "Categories are:",
	font:{fontSize:40,fontWeight:'bold'},
	width:'auto',
	textAlign:'left',
	top:2,
	color:'black',
	left:4
});

var Label_List_Categories = Ti.UI.createLabel({
	text: "",
	font:{fontSize:40},
	width:'auto',
	textAlign:'left',
	top:50,
	color:'black',
	left:4
});


CategoryView.add(Label_Categories);
CategoryView.add(Label_List_Categories);

// Finally, the word screen
// should be hidden by default

var WordView = Ti.UI.createView();

var Label_Category = Ti.UI.createLabel({
	text: "Category: ",
	font:{fontSize:20},
	width:'auto',
	textAlign:'left',
	top:2,
	color:'black',
	left:4
});

var Label_Time = Ti.UI.createLabel({
	text: "Time Left: ",
	font:{fontSize:20},
	width:'auto',
	textAlign:'right',
	top:2,
	color:'black',
	left:500
});


var Label_Word = Ti.UI.createLabel({
	text: "",
	font:{fontSize:60,fontWeight:'bold'},
	width:'auto',
	textAlign:'center',
	top:66,
	color:'black',
	left:4
});

Label_Time.left = Titanium.Platform.displayCaps.platformWidth - 200;
Label_Word.top = Titanium.Platform.displayCaps.platformHeight / 2 - 30;

WordView.add(Label_Category);
WordView.add(Label_Time);
WordView.add(Label_Word);

MainWin.addEventListener("longpress", function(e){
	ShowConfig();
});
// Now, lets add the views to the window and open it
MainWin.add(PennyView);
MainWin.add(CategoryView);
MainWin.add(WordView);
MainWin.open();

CategoryView.visible = false;
WordView.visible = false;
