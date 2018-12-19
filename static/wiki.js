function addListenersForIcons(){
    var icons = document.getElementsByClassName("icon-list-item"); //hole items aus der definierten icon Liste
    for (var icon_item of icons) { //hier nicht in, da wir die werte wollen https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Statements/for...of

        const icon = icon_item.childNodes[0]; //in dem listen element, befindet sich nur ein Bild //hier ggf. mehr sicherheit durch check
        //console.log(icon.title);
        //hier ist const notwendig, da sonst das zuletzt genommene Object übergeben wird, wir wollen die "Referenz" uns merken
        icon.addEventListener("click", function() {
            load_icon_into_canvas(icon);
        });
    }
}


window.addEventListener("DOMContentLoaded", function () {
    validate_init();  // fieser Hack!
    addListenersForIcons();
});

