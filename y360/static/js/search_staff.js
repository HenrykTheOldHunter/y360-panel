function search(){
    var input = document.getElementById('search-input');
    var filter = input.value.toUpperCase();
    let item = document.querySelectorAll('.list-item');
    for (i = 0; i < item.length; i++){
        let li = item[i].querySelectorAll('.list-item-li');
        for (l = 0; l < li.length; l++){
            var a = li[l].getElementsByTagName('a')[0];
            var txt = a.textContent || a.innerText;
            if (txt.toUpperCase().indexOf(filter) > -1) {
                item[i].style.display = "";
                break;
            }
            else {
                item[i].style.display = "none";
            }
        }
    }
}
