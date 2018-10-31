
function alertMe(evt) {
    alert("Zamboni!");
};


function preview(result) {

    // FIXME -probs need to format the JSON
    let previewText = result
    alert(result)
    // this will display the text, need to parse it(although shouldn't replace button)
    $('#preview').text(previewText)


}

function writeToUserFile() {
    // FINISH ME

    let labeledText = 'placeholder text for now'
    $("labeledText").text(labeledText)
    // display labelled line in new div at bottom of page
    // then write THAT text to the new file
};

function stashColorSlotsObj(colorSlotsObject) {
    // potentially add functionality for when no slots - deal with it when it breaks, 
    // may handle on python side
    $("#storage").val(colorSlotsObject)
    console.log($("#storage").val)

    // QUESTION - why not defined when try to call it in displaySlots?

}


function displaySlots(result) {

    // deletes buttons when change labels so slot buttons don't stack
    let slotBtnNode = document.getElementById("slotOptions");
    while (slotBtnNode.firstChild) {
    slotBtnNode.removeChild(slotBtnNode.firstChild);
    }

    if (result !== 'null') {
        console.log(result)
        let slots = Function('"use strict";return (' + result + ')')();
//        let slots = eval('(' + result + ')');
        console.log(slots)
        // initializing object for slot to color processing in python
        let colorSlotsObject = {};
        // need to clean the results to take out "" and []
        let colorOptions = ['#ff4e00', '#8ea604', '#f5bb00', '#a23b72', '#2e86ab']
        let colorCounter = 0

        slots.forEach (( function(v) {
            colorSlotsObject[colorOptions[colorCounter]] = v;
            let button = document.createElement('button');
            button.type = 'button';
            button.id = v
            button.className = 'slotOptionBtn'
            button.addEventListener("click", changeColor)
            button.innerHTML = v;
            button.style.backgroundColor = colorOptions[colorCounter];
            colorCounter ++;
            $('#slotOptions').append(button);

        }));
        
    $("#storage").val(colorSlotsObject)
    } else {
        slotBtnNode.innerHTML = 'No Slots';
    }
};



function changeColor(){
    let slotColor = this.style.backgroundColor;
    let selObj = window.getSelection();
    let currentId = this.id
 
    if (selObj.rangeCount && selObj.getRangeAt) {
        range = selObj.getRangeAt(0);
      }
    // Set design mode to on
    document.designMode = "on";
      if (range) {
        selObj.removeAllRanges();
        selObj.addRange(range);
      }
    // Colorize text
    document.execCommand("ForeColor", false, slotColor);
    // Set design mode to off
    document.designMode = "off";

} 


function grabSlotOptions(evt) {

    selectedLabel = document.getElementById('select2-myselLabel-container').title
    let label = {
        "label": selectedLabel, 
    };

    $.post("/generate_slots", label, displaySlots)

};


function processAnnotatedText(evt) {

    let textWithHighlights = $('#contentLine').html();
    let colorSlots = $("#storage").val();
    colorSlots = JSON.stringify(colorSlots);
    let annotatedText = {
        "colorSlotsObj": colorSlots,
        "text": textWithHighlights,
    };
    console.log(annotatedText)

    $.post('/process_text', annotatedText, preview)

};


function nextLine(evt) {
    let fileLines = $("#contentPkg").text();
    let lastLine = fileLines.split("\n");
    lastLine.pop(); // jankily popping the unecessary "" at end of array
    // May be better to write another function to process the text that comes out
    // of the html - remove ',', remove ending ""
    let l = lastLine.pop();
    writeToUserFile()
    alert(l);
    // it's not appearing to actually pop b/c refreshing content with fileLines
    // text from html everytime. Need to send the package back down to hidden 
    // html as the popped array
    // let l = lastLine[lastLine.length - 2]
    // console.log(l)
    // need to take out "" from the end of the array
};

$("#skip").click(alertMe);
$("#next").click(alertMe);

function displayLine(result) {
    let fileLines = result;
    // let lastLine = fileLines[fileLines.length - 1];
    // need a function that pics up a line and writes it to file
    let lastLine = fileLines.pop();
    $("#contentLine").text(lastLine);
    // need the following line to be a placeholder so can pick it up in the next function
    $("#contentPkg").text(fileLines);  

}
function sendFileName(evt, fname) {
    // evt.preventDefault
    let fileName = {
        "title": fname, 
    };

    // upon selecting the filename, I am reaching this function, with json
    // alert(fileName['title'])
    // now the goal is to send the info up into the url and grab it with python from there
    $.post('/annotate_content', fileName, displayLine)
};

function grabFileName(evt) {
    let fname = document.getElementById('select2-mysel-container').title;
    sendFileName(evt, fname)
};



// below lines are grabbing the user selected file and labels
$('myselect').on('select2:change', grabFileName);
$('#myselLabel').on('select2:change', grabSlotOptions);

