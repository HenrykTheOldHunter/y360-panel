$("#paste-from-department").on("click", function(){
    if($(this)[0].checked){
        $("#department-tab").css("display", "block");
        $("#group-tab").css("display", "none");
    }
    $(".error-text").html("");
})
$("#paste-from-group").on("click", function(){
    if($(this)[0].checked){
        $("#group-tab").css("display", "block");
        $("#department-tab").css("display", "none");
    }
    $(".error-text").html("");
})

$("#department").on("change", function(){
    if($(this)[0].value != "-1"){
        $.ajax({
            type: "POST",
            url : "/y360/paste-show-department/" + $(this)[0].value +"/",
            cache: false,
            data: {"type":$(this).data("type"),"for":$(this).data("for")},
            success: function(data){
                $("#department-container").html(data);
                $("#all-department-block").css("display", "block");
            },
        });
    }
    else{
        $("#department-container").html("");
        $("#all-department-block").css("display", "none");
    }
    $(".error-text").html("");
})
$("#group").on("change", function(){
    if($(this)[0].value != "-1"){
        $.ajax({
            type: "POST",
            url : "/y360/paste-show-group/" + $(this)[0].value +"/",
            cache: false,
            data: {"type":$(this).data("type"),"for":$(this).data("for")},
            success: function(data){
                $("#group-container").html(data);
                $("#all-group-block").css("display", "block");
            },
        });
    }
    else{
        $("#group-container").html("");
        $("#all-group-block").css("display", "none");
    }
    $(".error-text").html("");
})

$("#department-container")[0].addEventListener("click", event => {
    let bio = $("#department-container").find(".modal-bio").toArray()
    if(bio.includes(event.target)){
        event.target.classList.toggle("picked");
    }
    if(bio.includes(event.target.parentNode)){
        event.target.parentNode.classList.toggle("picked");
    }
    if(bio.includes(event.target.parentNode.parentNode)){
        event.target.parentNode.parentNode.classList.toggle("picked");
    }
    $("#all-department").prop('checked', true);
    bio.forEach(element => {
        if(!element.classList.contains("picked")){
            $("#all-department").prop('checked', false);
            return;
        }
    })
    $(".error-text").html("");
})
$("#group-container")[0].addEventListener("click", event => {
    let bio = $("#group-container").find(".modal-bio").toArray()
    if(bio.includes(event.target)){
        event.target.classList.toggle("picked");
    }
    if(bio.includes(event.target.parentNode)){
        event.target.parentNode.classList.toggle("picked");
    }
    if(bio.includes(event.target.parentNode.parentNode)){
        event.target.parentNode.parentNode.classList.toggle("picked");
    }
    $("#all-group").prop('checked', true);
    bio.forEach(element => {
        if(!element.classList.contains("picked")){
            $("#all-group").prop('checked', false);
            return;
        }
    })
    $(".error-text").html("");
})
$("#all-department").on("click", function(){
    if($(this).is(":checked")){
        $("#department-container").find(".modal-bio").toArray().forEach(element => {
            element.classList.add("picked");
        });
    }
    else{
        $("#department-container").find(".modal-bio").toArray().forEach(element => {
            element.classList.remove("picked");
        });
    }
    $(".error-text").html("");
})
$("#all-group").on("click", function(){
    if($(this).is(":checked")){
        $("#group-container").find(".modal-bio").toArray().forEach(element => {
            element.classList.add("picked");
        });
    }
    else{
        $("#group-container").find(".modal-bio").toArray().forEach(element => {
            element.classList.remove("picked");
        });
    }
    $(".error-text").html("");
})

$("#yes-button").on("click", function(){
    let users = [];
    if($("#paste-from-department").is(":checked")){
        $("#department-container").find(".modal-bio").toArray().forEach(element => {
            if(element.classList.contains("picked")){
                users.push(element.id);
            }
        })
    }
    if($("#paste-from-group").is(":checked")){
        $("#group-container").find(".modal-bio").toArray().forEach(element => {
            if(element.classList.contains("picked")){
                users.push(element.id);
            }
        })
    }
    $(".message").css("display", "block");
    $(this).prop("disabled", true);
    $("#return-button").prop("disabled", true);
    $(".error-text").html("");
    var data = JSON.parse($.ajax({
            type: "POST",
            url : $(this).data("url"),
            cache: false,
            async: false,
            data: {"users":JSON.stringify(users)},
            success: function(data){
                location.reload();
            },
        }).responseText);
    if("Error" in data){
        $(".message").css("display", "none");
        $(this).prop("disabled", false);
        $("#return-button").prop("disabled", false);
        var error = $("<a>"+data["Error"]+"</a>");
        error.css("color", "red");
        $(".error-text").html(error);
    }

})


$("#return-button").on("click", function(){
    location.reload();
})