
function alertMe(evt) {
    alert("Zamboni!");
};

function previewText(evt) {
    // FINISH ME

}

function writeToUserFile() {
    // FINISH ME

    let labeledText = 'placeholder text for now'
    $("labeledText").text(labeledText)
    // display labelled line in new div at bottom of page
    // then write THAT text to the new file
};

function displaySlots(result) {
    let slots = result.split(' ');
    // need to clean the results to take out "" and []
    let colorOptions = ['#FF4E00', '#8EA604', '#F5BB00', '#A23B72', '#2E86AB']
    let colorCounter = 0
    slots.forEach (( function(v) {
        let button = document.createElement('button');
        button.type = 'button';
        button.setAttribute('onClick', v.press);
        button.innerHTML = v;
        button.style.backgroundColor = colorOptions[colorCounter];
        colorCounter ++;
        console.log(colorCounter);
        document.getElementById("slotOptions").appendChild(button);
    }));

};

function grabSlotOptions(evt) {

    selectedLabel = document.getElementById('select2-myselLabel-container').title
    let label = {
        "label": selectedLabel, 
    };

    $.post("/generate_slots", label, displaySlots)

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

$('myselect').on('select2:change', grabFileName);

$('#myselLabel').on('select2:change', grabSlotOptions);



// Post request to server which will send back the file. Once JS has the whole
// file, can read it line by line once buttons are used