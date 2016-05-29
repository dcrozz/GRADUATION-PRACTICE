$(document).ready(function(){
	$("#submit").click(function(){
		$("#output").show();
		var NERtext = $("#NERtext").val();
		$.getJSON("process/",{'NERtext2':NERtext},function(ret){
			//$('#addresult').html(ret)
			//alert(ret);
			$.each(ret['exFeature'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					if(j==0){
						content +="<td>"+itm+"</td>";
					}
					else{
						content +="<td width="+100/item.length+"%>"+itm+"</td>";
					}
				});
				content += "</th>";
				$("#exFeature").append("<tr>"+content+"</tr>");
			});
			$.each(ret['selDNAFeature'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</th>";
				$("#selDNAFeature").append("<tr>"+content+"</tr>");
			});
			$.each(ret['selRNAFeature'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</th>";
				$("#selRNAFeature").append("<tr>"+content+"</tr>");
			});
			$.each(ret['selcellFeature'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</th>";
				$("#selcellFeature").append("<tr>"+content+"</tr>");
			});
			$.each(ret['rnaresult'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:yellow;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</th>";
				$("#rnaresult").append("<tr>"+content+"</tr>");
			});
			$.each(ret['dnaresult'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:red;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</th>";
				$("#dnaresult").append("<tr>"+content+"</tr>");
			});
			$.each(ret['cellresult'],function(i,item){
				var content = '';
				content +="<th scope=\"row\">";
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:green;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</th>";
				$("#cellresult").append("<tr>"+content+"</tr>");
			});
		});
	});
});
