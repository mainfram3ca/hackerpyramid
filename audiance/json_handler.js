laststatus = 0
Timer = null

function loadXMLDoc()
{
    $.ajax({
	url: 'ajax_info.php',
	type: 'GET',
	dataType: 'json',
	cache: false,	
	success: function(data) {
	    console.log(data);
            if (data.view == 0) {                                                                            
                document.getElementById("penny").style.visibility='visible'                                  
                document.getElementById("catagories").style.visibility='hidden'                              
                document.getElementById("questions").style.visibility='hidden'                               
                document.getElementById("Video").style.visibility='hidden'                               
            } else if (data.view == 1) {                                                                     
                document.getElementById("cata").innerHTML = ''                                               
                document.getElementById("penny").style.visibility='hidden'                                   
                document.getElementById("catagories").style.visibility='visible'                             
                document.getElementById("questions").style.visibility='hidden'                               
                document.getElementById("Video").style.visibility='hidden'                               
                catagories = data.catagory[0].name                                                           
                for (var i=1; i < data.catagory.length; i++) { // >                                          
                    catagories = catagories + "<BR>" + data.catagory[i].name                                 
                }                                                                                            
                document.getElementById("cata").innerHTML = catagories                                       
            } else if (data.view == 2) {
                document.getElementById("penny").style.visibility='hidden'                                   
                document.getElementById("catagories").style.visibility='hidden'                              
                document.getElementById("Video").style.visibility='hidden'                               
                document.getElementById("questions").style.visibility='visible'                              
                document.getElementById("word").innerHTML=data.word                                          
                document.getElementById("score").innerHTML=data.score                                        
                document.getElementById("time").innerHTML=data.time                                       
            } else if (data.view == 5) {
		// Video Handler
                document.getElementById("penny").style.visibility='hidden'                                  
                document.getElementById("catagories").style.visibility='hidden'                              
                document.getElementById("questions").style.visibility='hidden'                               
                document.getElementById("Video").style.visibility='visible'                               
		window.clearInterval(Timer)
		VideoPlayer = document.getElementById("VideoPlayer")
		VideoPlayer.src = data.video
		VideoPlayer.play()
		VideoPlayer.addEventListener("ended", function () {
		    Timer = setInterval(loadXMLDoc, 1000)
		})
	    }

	    if (laststatus == 2 & data.view == 0) {
		document.getElementById('buzzer').play();
	    }
	    laststatus = data.view
    	},
	error: function(data) { // Debug the error!!
	    debugger;
	    alert("Error");
	}
    }); // End of .error
};

$(function() {
    Timer=setInterval(loadXMLDoc, 1000);
});
