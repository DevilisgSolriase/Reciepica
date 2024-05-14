var side = document.getElementById("more_recipes")
var more = "<tr class=\"w-full h-1/5 hover:bg-french-very-dark-blue hover:text-white active:bg-frencg-light-blue\"><td class=\"w-1/4 h-full rounded-bl-xl p-2\"><img src=\"../css/pictures/images.png\" alt=\"\" class=\"rounded-full\"></td><td class=\"rounded-br-xl p-3\"><p id=\"reciepe_name_5\">Reciepe Name in here</p></td></tr>"

for(var num = 5; num > 0; num--){
    side.innerHTML += more
}
