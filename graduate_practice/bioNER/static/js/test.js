$(document).ready(function(){
	$("#submit").click(function(){
		var NERtext = $("#NERtext").val();
		$.getJSON("process/",{'NERtext2':NERtext},function(ret){
			//$('#addresult').html(ret)
			//alert(ret);
			$.each(ret,function(i,item){
				$("#output").append("<tr><th scope=\"row\"></th><td>"+item[0]+"</td><td>"+item[1]+"</td></tr>");	
			});
		})
	});
});
