$("body").on("mark", ".list-item-container", function(event, type){
	var inp = "";
	if(type == "department"){
		$("input").each(function(){
			if($(this).attr('id') == 'union-lookup-input'){
				inp = $(this).val();
			};
		});
		var a = $(this).find(".department-name").find("a");
		a.html(a.text().replace(new RegExp('(' + inp + ')', 'gi'),'<span class="highlight">$1</span>'));
	};
	if(type == "group"){
		$("input").each(function(){
			if($(this).attr('id') == 'union-lookup-input'){
				inp = $(this).val();
			};
		});
		var a = $(this).find(".group-name").find("a");
		a.html(a.text().replace(new RegExp('(' + inp + ')', 'gi'),'<span class="highlight">$1</span>'));
	};
	if(type == "staff"){
		$("input").each(function(){
			if($(this).attr('id') == 'staff-lookup-input'){
				inp = $(this).val();
			};
		});
		$(this).parent().siblings().find(".bio-name").find("a").each(function(){
			$(this).html($(this).text().replace(new RegExp('(' + inp + ')', 'gi'),'<span class="highlight">$1</span>'));
		});
	};
});