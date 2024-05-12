document.addEventListener("DOMContentLoaded", function() {
    var rec = document.getElementById("recipies")
    var more = document.getElementById("btn")

    var recipie="<div class=\"w-full md:h-48 h-40 p-2 bg-french-white rounded-xl flex\"><img class=\"md:w-1/5 w-1/3 md:h-full h-36 rounded-full\" src=\"../css/pictures/images.png\" alt=\"\"><table><tr class=\"h-1/5 w-full p-5\"><td class=\"text-xl font-serif\"><h1>Title</h1></td></tr><tr class=\"h-4/5 w-full\"><td class=\"text-lg font-serif p-5 break-words\"><p>hasdglsajkdhlkAJSj</p></td></tr></table></div>"

    var number_of_items = 7

    while(number_of_items >= 0){
        rec.innerHTML += recipie
        number_of_items--
    }

    function addDiv(){
        while(number_of_items >= 0){
            rec.innerHTML += recipie
            number_of_items--
        }
    }

    more.addEventListener("click", function(){
        number_of_items += 7;
        
        addDiv()
        
    })
     
    
    });