var count = 0
var countEl = document.getElementById("count-el")
var saveEl = document.getElementById("count-pe")

function increase(){
    count +=1
    countEl.innerText = count
    
}


function save(){
    var savestr = count + " - "
    saveEl.textContent += savestr
    countEl.textContent = 0
    count = 0
    
    

}