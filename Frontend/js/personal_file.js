var btn = document.getElementById("edit")
var bio = document.getElementById("bio")
var done = document.getElementById("done")
var input = document.getElementById("bio_edit")
var div = document.getElementById("div_edit")

btn.addEventListener("click",function(){
    div.classList = "w-full h-full"
})

done.addEventListener("click", function(){
    bio.innerHTML = input.value
    div.classList = "w-full h-full hidden"
})