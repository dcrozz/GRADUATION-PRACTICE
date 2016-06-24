$(document).ready(function(){
	$("#exFeature").click(function(){
		$("#table1").toggle();
		if($("#exFeature").hasClass('active')){
			$("#exFeature").removeClass('active');
		}else{
			$("#exFeature").addClass('active');
		}
	});

	$("#selDNAFeature").click(function(){
		$("#table2").toggle();
		if($("#selDNAFeature").hasClass('active')){
			$("#selDNAFeature").removeClass('active');
		}else{
			$("#selDNAFeature").addClass('active');
		}
	});
	$("#selRNAFeature").click(function(){
		$("#table3").toggle();
		if($("#selRNAFeature").hasClass('active')){
			$("#selRNAFeature").removeClass('active');
		}else{
			$("#selRNAFeature").addClass('active');
		}
	});
	$("#selcellFeature").click(function(){
		$("#table4").toggle();
		if($("#selcellFeature").hasClass('active')){
			$("#selcellFeature").removeClass('active');
		}else{
			$("#selcellFeature").addClass('active');
		}
	});
	$("#rnaresult").click(function(){
		$("#table6").toggle();
		if($("#rnaresult").hasClass('active')){
			$("#rnaresult").removeClass('active');
		}else{
			$("#rnaresult").addClass('active');
		}
	});
	$("#dnaresult").click(function(){
		$("#table5").toggle();
		if($("#dnaresult").hasClass('active')){
			$("#dnaresult").removeClass('active');
		}else{
			$("#dnaresult").addClass('active');
		}
	});
	$("#cellresult").click(function(){
		$("#table7").toggle();
		if($("#cellresult").hasClass('active')){
			$("#cellresult").removeClass('active');
		}else{
			$("#cellresult").addClass('active');
		}
	});
	$("#totalresult").click(function(){
		$("#table8").toggle();
		if($("#totalresult").hasClass('active')){
			$("#totalresult").removeClass('active');
		}else{
			$("#totalresult").addClass('active');
		}
	});
	$("#about").click(function(){
		alert('copyright by Alex Cao\n\n                  -Jun 2016');
	});





	$("#submit").click(function(){
		$("#output").show();
		var NERtext = $("#NERtext").val();
		$.getJSON("process/",{'NERtext2':NERtext},function(ret){
			//$('#addresult').html(ret)
			//alert(ret);
			content1='';
			$.each(ret['exFeature'],function(i,item){
				content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					if(j==0){
						content +="<td>"+itm+"</td>";
					}
					else{
						content +="<td width="+100/item.length+"%>"+itm+"</td>";
					}
				});
				content += "</tr>";
				content1 += content;
			});
			$("#exFeatureOut").replaceWith("<tbody id='exFeatureOut'>"+content1+"</tbody>");


			content2 = ''
			$.each(ret['selDNAFeature'],function(i,item){
				content = ''
				content +="<tr>";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</tr>";
				content2 += content;
			});
			$("#selDNAFeatureOut").replaceWith("<tbody id='selDNAFeatureOut'>"+content2+"</tbody>");


			content3=''
			$.each(ret['selRNAFeature'],function(i,item){
				content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</tr>";
				content3+=content;
			});
			$("#selRNAFeatureOut").replaceWith("<tbody id='selRNAFeatureOut'><tr>"+content3+"</tr></tbody>");



			content4=''
			$.each(ret['selcellFeature'],function(i,item){
				content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					content +="<td>"+itm+"</td>";
				});
				content += "</tr>";
				content4 += content;
			});
			$("#selcellFeatureOut").replaceWith("<tbody id='selcellFeatureOut'><tr>"+content4+"</tr></tbody>");


			content5=''
			$.each(ret['rnaresult'],function(i,item){
				var content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:yellow;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</tr>";
				content5 += content;
			});
				$("#rnaresultOut").replaceWith("<tbody id='rnaresultOut'><tr>"+content5+"</tr></tbody>");


			content6=''
			$.each(ret['dnaresult'],function(i,item){
				var content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:red;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</tr>";
				content6+= content;
			});
			$("#dnaresultOut").replaceWith("<tbody id='dnaresultOut'><tr>"+content6+"</tr></tbody>");


			content7=''
			$.each(ret['cellresult'],function(i,item){
				var content = '';
				content +="<tr>"
				$.each(item,function(j,itm){
					if (itm != '0' && j ==1){
						content +="<td style=\'color:green;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</tr>";
				content7+=content;
			});
			$("#cellresultOut").replaceWith("<tbody id='cellresultOut'><tr>"+content7+"</tr></tbody>");


			content8=''
			$.each(ret['totalresult'],function(i,item){
				var content = '';
				content +="<tr>";
				$.each(item,function(j,itm){
					if (itm == 'cell_line' && j ==1){
						content +="<td style=\'color:green;\'>"+itm+"</td>";
					}
					else if(itm == 'DNA' && j ==1){
						content +="<td style=\'color:red;\'>"+itm+"</td>";
					}
					else if(itm == 'RNA' && j ==1){
						content +="<td style=\'color:yellow;\'>"+itm+"</td>";
					}
					else{
						content +="<td>"+itm+"</td>";
					}
				});
				content += "</tr>";
				content8+=content;
			});
			$("#totalresultOut").replaceWith("<tbody id='totalresultOut'><tr>"+content8+"</tr></tbody>");

		});
	});
});
