/*
 * Single Window Application Template:
 * A basic starting point for your application.  Mostly a blank canvas.
 * 
 * In app.js, we generally take care of a few things:
 * - Bootstrap the application with any data we need
 * - Check for dependencies like device type, platform version or network connection
 * - Require and open our top-level UI component
 *  
 */

var myAppDir = Ti.Filesystem.getFile(Ti.Filesystem.externalStorageDirectory);
var sdcardDir = myAppDir.getParent();
var myFile = Titanium.Filesystem.getFile(sdcardDir.nativePath, '/hackerpyramid.txt');

if (myFile.exists()) {
	readContents = myFile.read();
	STARTPOINT = readContents.text;
	Ti.API.info('File Exists');  
} else {
	// Yeah, file doesn't exist
	alert ('You really should have a hackerpyramid.txt file in the sdCard root!');
	STARTPOINT = "https://coolacid.net/pyr/audiance/ajax_info.php"
}


//bootstrap and check dependencies
if (Ti.version < 1.8 ) {
	alert('Sorry - this application template requires Titanium Mobile SDK 1.8 or later');	  	
}

Ti.include ("functions.js");
Ti.include ("create_windows.js");
// Begin main functions

function Update() {
	var Loader = Titanium.Network.createHTTPClient();
	Loader.open('GET', STARTPOINT);
	Loader.onload = function ()
	{
		var Data = JSON.parse(this.responseData);
		HandleUpdate(Data);
	}
	Loader.send();
	
}

setInterval(function(){
   Update();
}, 500);

