$(document).ready(function(){
	$("#submit").click(function(){
		var NERtext = $("#NERtext").val();
		$.getJSON("process/",{'NERtext2':NERtext},function(ret){
			//$('#addresult').html(ret)
			//alert(ret);
			$.each(ret,function(i,item){
				$("#output").append("<tr><th scope=\"row\">3</th><td>"+i+"</td><td>"+item+"</td></tr>");	
			});
		})
	});
});
