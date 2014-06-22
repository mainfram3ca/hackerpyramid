laststatus = 0
Timer = null
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

function HandleEvent(data)
{
    data = JSON.parse(data)
    if (typeof data.timer != "undefined") {
	$(".dial").val(data.timer).trigger('change')
    } else if (data.scores) {
      update_score(data.scores)
    } else if (data.video) {
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
    } else {
      if (data.state == 0) {                                                                            
	document.body.style.background = Background
        document.getElementById("main").style.visibility='visible'                                  
        document.getElementById("penny").style.visibility='visible'                                  
        document.getElementById("catagories").style.visibility='hidden'                              
        document.getElementById("questions").style.visibility='hidden'                               
        document.getElementById("video").style.visibility='hidden'                               
	VideoPlayer = document.getElementById("VideoPlayer")
	VideoPlayer.pause()
	$(".dial").val(0).trigger('change')
//      } else if (data.state == 1) { // Video State

      } else if (data.state == 2) {                                                                     
	// Catagories
	document.body.style.background = Background
        document.getElementById("cata").innerHTML = ''                                               
        document.getElementById("main").style.visibility='visible'                                  
        document.getElementById("penny").style.visibility='hidden'                                   
        document.getElementById("catagories").style.visibility='visible'                             
        document.getElementById("questions").style.visibility='hidden'                               
        document.getElementById("video").style.visibility='hidden'                               
	$('#catagories').empty();
	$('#catagories').append("<span id='cata'></span>") //.attr('id', 'word')
        catagories = data.catagory[0].name                                                           
        for (var i=1; i < data.catagory.length; i++) { // >                                          
            catagories = catagories + "<BR>" + data.catagory[i].name                                 
        }                                                                                            
        document.getElementById("cata").innerHTML = catagories                                       
	$('#catagories').textfill( {debug: false, widthOnly: true, maxFontPixels: 150})
	$('#cata').center()
      } else if (data.state == 3) {
	// Game Running
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
      }
    
//      if (laststatus == 2 & data.state == 0) {
//	document.getElementById('buzzer').play();
//      }
//      laststatus = data.state
    }
};

function video_ended() {
	console.log("ended")
	// TODO: Send Video Ended WS event
}

$(function() {
    StartWebSocket()
    $(".dial").knob({
        'min':0,
        'max':30,
        'readOnly': 'True'
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
        ws = new WebSocket("ws://localhost:9000/ws");

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
