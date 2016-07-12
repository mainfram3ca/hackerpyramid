laststatus = 0
oldtime = null
Background = null
ws = null

function update_score(scoredata) 
{
    $('#scoretable tbody').remove()
    $('#scoretable').append("<tbody></tbody>")
    for (x in scoredata) {
	$('#scoretable tbody:last').append("<tr><td>" + scoredata[x].name + "</td><td>" + scoredata[x].score + "</td></tr>")
    }
    $('#scoretable').colorize();
}

function Init()
{
	if ($(location).attr('hash') == "#s") {
		// chatback function for podium
		data = '{state: 0}'
		document.body.style.background = Background
		document.getElementById("main").style.visibility='visible'                                  
		document.getElementById("penny").style.visibility='hidden'                                  
		document.getElementById("catagories").style.visibility='hidden'                              
		document.getElementById("questions").style.visibility='hidden'                               
		document.getElementById("video").style.visibility='hidden'                               
		document.getElementById("chat").style.visibility='visible'                               
		VideoPlayer = document.getElementById("VideoPlayer")
		VideoPlayer.pause()
		$(".dial").val(0).trigger('change')
	} else {
		data = '{state: 0}'
		document.body.style.background = Background
		document.getElementById("main").style.visibility='visible'                                  
		document.getElementById("penny").style.visibility='visible'                                  
		document.getElementById("catagories").style.visibility='hidden'                              
		document.getElementById("questions").style.visibility='hidden'                               
		document.getElementById("video").style.visibility='hidden'                               
		document.getElementById("chat").style.visibility='hidden'                               
		VideoPlayer = document.getElementById("VideoPlayer")
		VideoPlayer.pause()
		$(".dial").val(0).trigger('change')
	}
}

function formSend()
{
	message = document.getElementById("sendMessage").value
	jsonmessage = '{"message":"' + message + '","name":"' + document.getElementById('clientName').value + '"}'
	ws.send(jsonmessage)
	document.getElementById("sendMessage").value = ""
}

function HandleEvent(data)
{
    data = JSON.parse(data)
    if (typeof data.timer != "undefined") {
	//newtime = Math.floor(data.timer*10)/10
	newtime = Math.ceil(data.timer)
	if (newtime != oldtime) { 
	    $(".dial").val(data.timer).trigger('change')
	    oldtime = newtime
	}
    } else if (typeof data.scores != "undefined") {
	update_score(data.scores)
    } else if (data.setcatateam  && $(location).attr('hash') == "#s") {
	//{"setcatateam": ["", "Team A"]}
	$('#ActiveTeam').empty()
	$('#ActiveTeam').append('<span id="thisteam"></span>')
	document.getElementById("thisteam").innerHTML = data.setcatateam[1]
    } else if ((typeof data.word != "undefined") && !($(location).attr('hash') == "#s")) {
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.pause()
	document.body.style.background = Background
        document.getElementById("main").style.visibility='visible'                                  
        document.getElementById("penny").style.visibility='hidden'                                   
        document.getElementById("catagories").style.visibility='hidden'                              
        document.getElementById("video").style.visibility='hidden'                               
        document.getElementById("questions").style.visibility='visible'                              
	$('#questions').empty();
	$('#questions').append("<span id='word'></span>") //.attr('id', 'word')
        document.getElementById("word").innerHTML=data.word                                          
	$('#questions').textfill( {debug: false, widthOnly: true, maxFontPixels: 250})
	$('#word').center()
    } else if (data.video && !($(location).attr('hash') == "#s")) {
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.src = "videos/" + data.video
	// Video Handler
	document.body.style.background='black'
	document.getElementById("main").style.visibility='hidden'                                  
	document.getElementById("penny").style.visibility='hidden'                                  
	document.getElementById("catagories").style.visibility='hidden'                              
	document.getElementById("questions").style.visibility='hidden'                               
	document.getElementById("video").style.visibility='visible'                               
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.play()
    } else if (data.playfx) {
	audiomedia = document.getElementById(data.playfx)
	if (data.loop == true) {
	    if (audiomedia.loop == true) {
		audiomedia.loop = false
		audiomedia.pause()
		audiomedia.currentTime = 0
	    } else {
		audiomedia.loop = true
		audiomedia.play()
	    }
	} else {
	    audiomedia.play()
	}
    } else if (data.catagories) {                                                                     
	// Catagories
	document.body.style.background = Background
	document.getElementById("cata").innerHTML = ''                                               
	document.getElementById("main").style.visibility='visible'                                  
	document.getElementById("penny").style.visibility='hidden'                                   
	document.getElementById("catagories").style.visibility='visible'                             
	document.getElementById("questions").style.visibility='hidden'                               
	document.getElementById("video").style.visibility='hidden'                               
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.pause()
	$('#catagories').empty();
	$('#catagories').append("<span id='cata'></span>") //.attr('id', 'word')
	catagories = ""
        for (var i=0; i < data.catagories.length; i++) { 
		//jsonmessage = '{"message":"<x style=color:red;>' + data.catagories[i].title + '</x>(' + data.catagories[i].hint +')","name":"CATEGORY"}'
		var pre = document.createElement("div");
		pre.style.wordWrap = "break-word"
		pre.style.align = "left"
		pre.style.color = "white"
		pre.innerHTML = '<x style="color:grey;">CATEGORY: </x><x style=color:red;>' + data.catagories[i].title + "</x> HINT: "+data.catagories[i].hint
		document.getElementById("output").appendChild(pre)
		var objDiv = document.getElementById("output")
		objDiv.scrollTop = objDiv.scrollHeight

	    if (i == 0) {
            	catagories = catagories + "" + data.catagories[i].title                                 
	    } else {
            	catagories = catagories + "<BR>" + data.catagories[i].title                                 
	    }
            if ($(location).attr('hash') == "#s") {
                catagories = catagories + "<BR><span id='hint'>" + data.catagories[i].hint + "</span>"
            }
        }                                                                                            
	if (!($(location).attr('hash') == "#s")) {
        	document.getElementById("cata").innerHTML = catagories                                       
		$('#catagories').textfill( {debug: false, maxFontPixels: 150})
		$('#cata').center()
	}
    } else if ($(location).attr('hash') == "#s" && data.message) {
    	// check for chat message
	document.body.style.background = Background
        document.getElementById("main").style.visibility='visible'
        document.getElementById("penny").style.visibility='hidden'
        document.getElementById("catagories").style.visibility='hidden'
        document.getElementById("questions").style.visibility='hidden'
        document.getElementById("video").style.visibility='hidden'
        document.getElementById("chat").style.visibility='visible'
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.pause()
	$(".dial").val(0).trigger('change')

	var pre = document.createElement("div");
	pre.style.wordWrap = "break-word"
	pre.style.align = "left"
	pre.style.color = "white"
	pre.innerHTML = '<x style="color:grey;">' + data.name + ":</x> "+data.message
	document.getElementById("output").appendChild(pre)
	var objDiv = document.getElementById("output")
	objDiv.scrollTop = objDiv.scrollHeight
	
    } else {
      if (data.state == 0 && !($(location).attr('hash') == "#s")) { 
	document.body.style.background = Background
        document.getElementById("main").style.visibility='visible'                                  
        document.getElementById("penny").style.visibility='visible'                                  
        document.getElementById("catagories").style.visibility='hidden'                              
        document.getElementById("questions").style.visibility='hidden'                               
        document.getElementById("video").style.visibility='hidden'                               
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.pause()
	$(".dial").val(0).trigger('change')
      }
    }
};

function video_ended() {
	console.log("Video Ended")
	var message = { videoended: true }
	ws.send(JSON.stringify( message ))
}

$(function() {
    StartWebSocket()
    $(".dial").knob({
        'min':0,
        'max':30,
        'readOnly': 'True',
	'data-step':0.1
    })
    Background = document.body.style.background
    VideoPlayer.addEventListener('timeupdate', function (e) {
	// Work around for ended not firing
	//if (this.duration - this.currentTime < 0.2) {
	//    this.pause()
	//    this.currentTime = 0
	//    console.log("Work Around End")
	//    video_ended()
	//}
	var timecode = { timecode: Math.round((this.duration - this.currentTime)*100)/100 }
	ws.send(JSON.stringify(timecode))
    })

    VideoPlayer.addEventListener("ended", function () {
	video_ended()
    })
});

function StartWebSocket() {
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://192.168.99.91:9000/ws");

	ws.onmessage = function (evt) {
	    HandleEvent(evt.data);
        };

        ws.onclose = function() {
	    alert("Connection Closed");
        };

    } else {
        alert("WebSocket NOT supported by your Browser!");
    }
}
