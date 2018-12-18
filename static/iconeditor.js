/**
 * Created by Tobias on 14.05.2015.
 */



//////////////////////////
// Änderungen ////////////                                                                                              // ------------------------------
//////////////////////////


//Variablen
var selected_tool;

//mouse event wenn gezeichnet werden soll
function move_over_pixel(event) {
    if(event.buttons == 1) { // Mit gedrückter Maustaste soll gezeichnet werden können,
                            //d.h. es soll nicht nötig sein, für jedes einzelne Pixel einzeln zu klicken. (5%)
        setPixelDependingOnTool(event.target); //tue so, als sei ein Pixel berührt worden
    }
}

//Set Pixel methode, die Aufgerufen wird, wenn ein Pixel berührt wird
function setpixel(event) {
    setPixelDependingOnTool(this); //könnte direkt beim erstellen der Pixel Zelle hinzugefügt werden, jedoch
    //kann an dieser Stelle das Event noch weiter befragt werden
}

//führe an einem Pixel das Werkzeug aus
function setPixelDependingOnTool(pixel){
    if(isEraserSelected()){ //Radieren
        onPixelUseEraser(pixel);
    }
    if(isPencilSelected()){ //Zeichnen
        onPixelUsePencil(pixel);
    }
    if(isFillSelected()){ //Füllen
        onPixelUseFill(pixel);
    }
    preview(); //zeige ergebnis in preview
}

function onPixelUseEraser(pixel){
    pixel.style.backgroundColor = "rgb(255,255,255)";
}

function onPixelUsePencil(pixel){
    var currentColor=document.getElementById("current-color").style.backgroundColor;
    pixel.style.backgroundColor = currentColor;
}

//Benutze die Füll Methode an einen Pixel
function onPixelUseFill(pixel){
    var coord = pixel.id.split("-"); //splitte die id um coordinaten zu erhalten
    var selectedColor = document.getElementById("current-color").style.backgroundColor; //merke farbe zum einzeichnen
    var colorToReplace = pixel.style.backgroundColor; //merke farbe die der erste Pixel hat
    floodFill(coord[1],coord[2],selectedColor,colorToReplace); //rufe floodfill auf
}

//FloodFill an einer Pixel Position, wobei colorToReplace ersetzt wird mit selectedColor
function floodFill(x,y,selectedColor,colorToReplace){
    if(x==undefined || y == undefined || selectedColor==undefined){ //keine farbe gesetzt
        return;
    }

    if(x<0 || x >= 16 || y<0 || y >= 16){ //wenn out of bounds
        return;
    }

    var pixel = document.getElementById("pixel-"+x+"-"+y); //den pixel wo es hin soll
    if(pixel.style.backgroundColor==colorToReplace){ //wenn selbe farbe wie der erste gewählte Pixel
        pixel.style.backgroundColor = selectedColor;   //setze die farbe
        //und nun rekursive aufrufe
        floodFill(x-1,y,selectedColor,colorToReplace); //links
        floodFill(x+1,y,selectedColor,colorToReplace); //rechts
        floodFill(x,y-1,selectedColor,colorToReplace); //unten
        floodFill(x,y+1,selectedColor,colorToReplace); //oben
    }
}



//füge allen tools ein event listener an
function create_click_event_for_tools() {

    var tools = document.getElementsByClassName("tool-list-item"); //hole items aus der definierten icon Liste
    for (var tool_item of tools) { //hier nicht in, da wir die werte wollen https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Statements/for...of
        const tool = tool_item.childNodes[0]; //in dem listen element, befindet sich nur ein Bild //hier ggf. mehr sicherheit durch check
        tool_selected(tool);
        //hier ist const notwendig, da sonst das zuletzt genommene Object übergeben wird, wir wollen die "Referenz" uns merken
        tool.addEventListener("click", function() {
            tool_selected(tool);
        });
    }
}

//Setze ein Gewähltes Tool, soll ein Bild sein, da hier der Rahmen gesetzt wird //Nicht so sicher
function tool_selected(tool){
    if(selected_tool != undefined){
        selected_tool.border = 0; //remove border from old
    }
    selected_tool = tool; //save new tool
    selected_tool.border=2; //make border

    //Setze entsprechenden Cursor für alle Pixel/Zellen
    if(isEraserSelected()){
        set_cursor_on_pixels("no-drop");
    }
    if(isPencilSelected()){
        set_cursor_on_pixels("cell");
    }
    if(isFillSelected()){
        set_cursor_on_pixels("move");
    }

}

//Prüfen welches Tool verwendet wird
function isPencilSelected(){
    return selected_tool.title == "pencil";
}
function isEraserSelected(){
    return selected_tool.title == "eraser";
}
function isFillSelected(){
    return selected_tool.title == "fill";
}

//Setze für alle Pixel Zellen einen Cursor Typ
function set_cursor_on_pixels(cursor_type) {
    var pixel_cells = document.getElementsByClassName("icon-pixel"); //hole alle Pixel

    for(var pixel_cell of pixel_cells){ //für jede Zelle/Pixel
        pixel_cell.style.cursor = cursor_type; //Setze Cursor Type
    }
}




//füge allen icons ein event listener an
function create_click_event_for_icons() {
    var icons = document.getElementsByClassName("icon-list-item"); //hole items aus der definierten icon Liste
    for (var icon_item of icons) { //hier nicht in, da wir die werte wollen https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Statements/for...of
        const icon = icon_item.childNodes[0]; //in dem listen element, befindet sich nur ein Bild //hier ggf. mehr sicherheit durch check
        //hier ist const notwendig, da sonst das zuletzt genommene Object übergeben wird, wir wollen die "Referenz" uns merken
        icon.addEventListener("click", function() {
            load_icon_into_canvas(icon);
        });
    }
}

//function, welche beim auswählen eines icons aufgerufen wird
//parameter icon, das icon element im HTML
function load_icon_into_canvas(icon){
    var canvas = document.createElement('canvas'); //hole canvas
    var ctx = canvas.getContext('2d');
    ctx.drawImage(icon, 0, 0); //lade icon in canvas, damit wir die pixel daten erhalten können

    //fülle nun die pixel mit dem image daten aus dem icon
    for (var i = 0; i < 16; i++) {
        for (var j = 0; j < 16; j++) {
            var imgData = ctx.getImageData(j, i, 1, 1); //hole image daten
            var pixel = document.getElementById("pixel-"+i+"-"+j); //den pixel wo es hin soll
            pixel.style.backgroundColor = "rgb("+imgData.data[0]+","+imgData.data[1]+","+imgData.data[2]+")"; //setze farbe
        }
    }

    preview(); //fülle das kleine preview bild
}

//////////////////////////
// Änderungen Ende ///////
//////////////////////////




function create_table() {
    var tablediv=document.getElementById('icon-table');
    var table = document.createElement("table");
    table.className = "icon-table";
    tablediv.appendChild(table);
    for (var i = 0; i < 16; i++) {
        var tr = document.createElement("tr");
        table.appendChild(tr);
        for (var j = 0; j < 16; j++) {
            var td = document.createElement("td");
            td.className = "icon-pixel";
            td.id="pixel-"+ i + "-" + j;
            td.style.backgroundColor = "rgb(255,255,255)"; // no dash - css attribute name becomes camelCase
            td.addEventListener("click", setpixel);
            td.addEventListener("mousemove", move_over_pixel);                                                          // ------------------------------
            tr.appendChild(td);
        }
    }
}





function create_color_picker() {
    var tablediv = document.getElementById('color-picker');
    var table = document.createElement("table");
    table.className = "color-picker-table";
    tablediv.appendChild(table);
    var tr;
    var count = 0;
    var step = 63;
    for (var r=0; r < 256; r += step) {
        for (var g=0; g < 256; g += step) {
            for (var b = 0; b < 256; b += step) {
                if (count++ % 24 === 0) {  // new row
                    tr = document.createElement("tr");
                    table.appendChild(tr);
                }
                var td = document.createElement("td");
                td.className = "picker-pixel";
                td.style.backgroundColor = "rgb("+r+","+g+","+b+")";
                td.addEventListener("click", choosecolor);
                tr.appendChild(td);
            }
        }
    }
}

function choosecolor(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.style.backgroundColor = this.style.backgroundColor;
}

function preview() {
    var canvas = document.getElementById('preview-canvas');
    var ctx = canvas.getContext("2d");
    for (var i=0; i<16; i++) {
        for (var j=0; j<16; j++) {
            ctx.fillStyle = document.getElementById("pixel-"+i+"-"+j).style.backgroundColor;
            ctx.fillRect(j,i,1,1);
        }
    }
    document.getElementById("save-icon").value = canvas.toDataURL();
}


window.addEventListener("DOMContentLoaded", function () {
    validate_init();  // fieser Hack!
    create_table();
    create_color_picker();
    create_click_event_for_icons();                                                                                     // ------------------------------
    create_click_event_for_tools();                                                                                     // ------------------------------
    preview();
});

