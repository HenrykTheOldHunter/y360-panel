window.addEventListener("load", (event) => {
	staff_search_init();
});
function staff_search_init(){
	$("#staff-lookup-button").on("click", function(){
		$("#union-lookup-input").val("");
		var inp = "";
		$("input").each(function(){
			if($(this).attr('id') == 'staff-lookup-input'){
				inp = $(this).val();
			};
		});
		let container = $(document).find(".list");
		container.html('');
		if (inp != ""){
			$.ajax({
				type: "POST",
				url : $("#staff-lookup-button").data("url"),
				data: {"value":inp},
				cache: false,
			}).done(function(data){
			   container.html(data);
			   document.querySelectorAll(".list-item-container").forEach(con => {
				  $(con).trigger("mark", "staff"); 
			   });
			});
		}
		else{

			$.ajax({
				type: "POST",
				url: $("#staff-lookup-button").data("return"),
				cache: false,
			}).done(function(data){
				var parser = new DOMParser();
				container.html(parser.parseFromString(data, "text/html").querySelector(".list"))
			});
		};
	});
}