
function alertMe(evt) {
    alert("Zamboni!");
};

function textParse(annotatedText){
    // gives me text with font colors which delineate on which words tags go
    let originalText = $('#contentLine').html()   
    alert(originalText)
    // need to make an object which maps the font colors to the slot text/ids 
    // add to this empty string
    let annoTextForPreview = ''


    // FINISH ME - need to insert the slots into the proper text from the content line
    // HAVE: original text, text object containing keys as slots with val as selected text
    // remember, need to be able to select diff text for same slot? actually will that ever be the case?
}

function preview(evt) {
    console.log('getting to preview function');
    let annotatedText = $('#storage').data('key');
    console.log(annotatedText)
    let previewText = textParse(annotatedText)
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

function displaySlots(result) {

    // deletes buttons when change labels so slot buttons don't stack
    let slotBtnNode = document.getElementById("slotOptions");
    while (slotBtnNode.firstChild) {
    slotBtnNode.removeChild(slotBtnNode.firstChild);
    }

    if (result !== 'null') {

        let slots = result.split(',');
        // need to clean the results to take out "" and []
        let colorOptions = ['#FF4E00', '#8EA604', '#F5BB00', '#A23B72', '#2E86AB']
        let colorCounter = 0

        slots.forEach (( function(v) {
            let button = document.createElement('button');
            button.type = 'button';
            button.id = v
            button.className = 'slotOptionBtn'
            button.addEventListener("click", changeColor)
            button.innerHTML = v;
            button.style.backgroundColor = colorOptions[colorCounter];
            colorCounter ++;
            document.getElementById("slotOptions").appendChild(button);
        }));

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

