function loadXMLDoc()
{
    $.ajax({
	url: 'ajax_info.php',
	type: 'GET',
	dataType: 'json',
	cache: false,	
	success: function(data) {
	    console.log(data);
    	    document.getElementById("timer").innerHTML=data.left;
	    if (data.left == 0) {
		console.log("Redirecting")
		window.location.href="?command=refresh"
	    }
	},
	error: function(data) { // Debug the error!!
	    debugger;
	    alert("Error");
	}
    }); // End of .error
};

$(function() {
    setInterval(loadXMLDoc, 1000);
});
