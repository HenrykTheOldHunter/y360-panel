window.addEventListener("load", (event) => {
	search_init();
});
function search_init(){
	$("#union-lookup-button").on("click", function(){
		$("#staff-lookup-input").val("");
		var inp = "";
		$("input").each(function(){
			if($(this).attr('id') == 'union-lookup-input'){
				inp = $(this).val();
			};
		});
		let container = $(document).find(".list");
		container.html('');
		if (inp != ""){
			$.ajax({
				type: "POST",
				url : $("#union-lookup-button").data("url"),
				data: {"value":inp},
				cache: false,
			}).done(function(data){
			   container.html(data);
			   document.querySelectorAll(".list-item-container").forEach(con => {
					if($("#union-lookup-button").data("url").indexOf("department")>=0){
						$(con).trigger("mark", "department");
					};
					if($("#union-lookup-button").data("url").indexOf("group")>=0){
						$(con).trigger("mark", "group");
					};
			   });
			});
		}
		else{

			$.ajax({
				type: "POST",
				url: $("#union-lookup-button").data("return"),
				cache: false,
			}).done(function(data){
				var parser = new DOMParser();
				container.html(parser.parseFromString(data, "text/html").querySelector(".list"))
			});
		};
	});
}