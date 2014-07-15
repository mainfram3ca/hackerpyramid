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

var presenter = Ti.App.Properties.getBool('host', false);
var STARTPOINT = Ti.App.Properties.getString('wssocket', "");
var teams = [];

//bootstrap and check dependencies
if (Ti.version < 1.8 ) {
	alert('Sorry - this application template requires Titanium Mobile SDK 1.8 or later');
}

Ti.include ("functions.js");
Ti.include ("create_windows.js");
// Begin main functions

var WS = require('net.iamyellow.tiws').createWS();

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
	var data = null;
	try {
		data = JSON.parse(ev.data);
	} catch(e) {
		Ti.API.debug("Got invalid JSON");
	}
	if (data != null) {
		HandleUpdate(data);
	}
});

if (STARTPOINT != ""){
	startws();
} else {
	MainWin.hide();
	ShowConfig();
	MainWin.show();
}
