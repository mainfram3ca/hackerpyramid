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

if (STARTPOINT != ""){
	startws();
} else {
	MainWin.hide();
	ShowConfig();	
}



