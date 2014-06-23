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
var WS = require('net.iamyellow.tiws').createWS();

//bootstrap and check dependencies
if (Ti.version < 1.8 ) {
	alert('Sorry - this application template requires Titanium Mobile SDK 1.8 or later');	  	
}

Ti.include ("functions.js");
Ti.include ("create_windows.js");
// Begin main functions

STARTPOINT = "ws://10.0.0.100:9000/ws";

function startws() {
	WS.addEventListener('open', function () {
		Ti.API.debug('websocket opened');
	});

	WS.addEventListener('close', function (ev) {
		Ti.API.info(ev);
	});

	WS.addEventListener('error', function (ev) {
		Ti.API.error(ev);
	});

	WS.addEventListener('message', function (ev) {
		HandleUpdate(JSON.parse(ev.data));
	});

	WS.open(STARTPOINT);
}


if (myFile.exists()) {
	readContents = myFile.read();
	STARTPOINT = readContents.text;
	Ti.API.info('File Exists'); 
	startws();
} else if (STARTPOINT != ""){
	startws();
} else {
	// Yeah, file doesn't exist
	    var alertDialog = Ti.UI.createAlertDialog({
        title: "Alert",
        message: 'You really should have a hackerpyramid.txt file in ' + sdcardDir.nativePath + '/hackerpyramid.txt',
        buttonNames: ['OK'],
        cancel:0
    });
    alertDialog.show();
	//STARTPOINT = "https://coolacid.net/pyr/audiance/ajax_info.php"
}



