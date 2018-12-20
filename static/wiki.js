/**
  * adds click Listener for icons add the wikipage
  */
function addListenersForIcons(){
    var icons = document.getElementsByClassName("wikiicons-items"); //hole items aus der definierten icon Liste
    for (var icon_item of icons) { //hier nicht in, da wir die werte wollen https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Statements/for...of
        const icon = icon_item.childNodes[0]; //in dem listen element, befindet sich nur ein Bild //hier ggf. mehr sicherheit durch check
        //hier ist const notwendig, da sonst das zuletzt genommene Object übergeben wird, wir wollen die "Referenz" uns merken
        icon.addEventListener("click", function() {
            setIconTextArea(icon.title); //if clicked on icon, set iconname in textarea
        });
    }
}

/**
  * sets the iconname in the textare
  */
function setIconTextArea(text){
    var textArea = document.getElementsByClassName("wikiicon"); //get the textarea
    textArea[0].value = text; //sets the value
}


window.addEventListener("DOMContentLoaded", function () {
    validate_init();  // fieser Hack!
    addListenersForIcons(); //acitvate click listeners
});

