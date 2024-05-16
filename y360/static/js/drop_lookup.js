window.addEventListener("load", (event) => {
	$("#drop-lookup-button").on("click", function(){
		$("#staff-lookup-input").val("");
		$("#union-lookup-input").val("");
		let container = $(document).find(".list");
		container.html('');
		$.ajax({
			type: "POST",
			url: $("#drop-lookup-button").data("url"),
			cache: false,
		}).done(function(data){
			var parser = new DOMParser();
			container.html(parser.parseFromString(data, "text/html").querySelector(".list"))
		});
	});
});