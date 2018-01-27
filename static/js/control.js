$(function(){
	$('#ledON').click(function(){
		$.ajax({
			url:'http://192.168.2.120:8000/led1',
			async:false
		});
	})
})