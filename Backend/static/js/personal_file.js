//Bio Edit

var btn = document.getElementById("edit")
var bio = document.getElementById("bio")
var done = document.getElementById("done")
var input = document.getElementById("bio_edit")
var div = document.getElementById("div_edit")

btn.addEventListener('click',function(){
    div.classList = "w-full h-full"
    btn.classList = "hidden"
})

done.addEventListener('click', function(){

    if(input.value != ""){
        bio.innerHTML = input.value
    }

    div.classList = "w-full h-full hidden"
    btn.classList = "text-lg"
})

//Image Edit

var btn_img = document.getElementById("img_edit")
var div_img = document.getElementById("div_img_edit")
var username = document.getElementById("username")
var username_change = document.getElementById("username_change")
var change =document.getElementById("img_change")
var img_done = document.getElementById("img_done")
var img = document.getElementById("profile_img")

btn_img.addEventListener('click', function(){
    div_img.classList = "w-full h-auto grid gap-2 text-center"
    btn_img.classList = "hidden"
})

img_done.addEventListener('click', function(){
    var file = img_edit.files[0]
    
    if(file){
        var reader = new FileReader()

        reader.onload = function(){
            img.src = event.target.result
        }
        reader.readAsDataURL(file)
    }

    if(username_change.value){
        username.textContent = username_change.value
    }


    div_img.classList = "w-full h-auto hidden"
    btn_img.classList = "text-lg"
})


