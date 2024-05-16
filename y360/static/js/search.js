$("#search-input").on("keyup", function(){
	search();
});
function search(){
	var inp="";
	$("input").each(function(){
		if($(this).attr('id') == 'search-input'){
			inp = $(this).val();
		};
	});
	var filter = inp.toUpperCase();
	let item = document.querySelectorAll('#staff-block');
	for (i = 0; i < item.length; i++){
		let li = item[i].querySelectorAll('.modal-bio-name');
		for (l = 0; l < li.length; l++){
			var a = li[l].getElementsByTagName('a')[0];
			var txt = a.textContent || a.innerText;
			if (txt.toUpperCase().indexOf(filter) > -1) {
				item[i].style.display = "";
				break;
			}
			else {
				item[i].style.display = "none";
				item[i].classList.remove("picked");
			};
		};
	};
};