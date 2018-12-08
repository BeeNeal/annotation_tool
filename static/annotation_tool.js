
function alertMe(evt) {
    alert("This is working");
};

function sameFileAlert() {
    const warning = 'A completed or in progress file for this user already exists - overwrite?';
    alert(warning)
};

function preview(result) {

    let previewText = result;
    let label = $('#select2-myselLabel-container').attr('title');
    //    currently the below tab is not showing up on the page, but is present
    let annotated = label + '\t' + result;
    $('#previewText').text(annotated);

}


function displaySlots(result) {

    // deletes buttons when change labels so slot buttons don't stack
    let slotBtnNode = document.getElementById("slotOptions");
    while (slotBtnNode.firstChild) {
    slotBtnNode.removeChild(slotBtnNode.firstChild);
    }

    // remove highlighting from div in case change label halfway through
    $('#contentLine').text($('#contentLine').text());

    if (result !== 'null') {
        let slots = Function('"use strict";return (' + result + ')')();

        // initializing object for slot to color processing in python
        let colorSlotsObject = {};
        const numToLabels = {};

        let colorOptions = ['#ff4e00', '#8ea604', '#f5bb00', '#a23b72', '#2e86ab'];
        let colorCounter = 0;

        let num_code = 49

        slots.forEach (( function(v) {
            colorSlotsObject[colorOptions[colorCounter]] = v;
            numToLabels[num_code] = v;
            let button = document.createElement('button');
            button.type = 'button';
            button.id = v;
            button.className = 'slotOptionBtn noselect';
            button.addEventListener("click", changeColor);
            button.addEventListener("keypress", checkKey);
            button.innerHTML = '[' + (colorCounter + 1) + '] ' + v;
            button.style.backgroundColor = colorOptions[colorCounter];
            colorCounter ++;
            num_code ++;
            $('#slotOptions').append(button);

        }));

        let clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.id = 'clearBtn';
        clearBtn.className = 'slotOptionBtn';
        clearBtn.addEventListener("click", removeColor);
        clearBtn.innerHTML = '[' + (colorCounter + 1) + '] '+ 'clear selection';
        clearBtn.style.backgroundColor = 'blue';
        $('#slotOptions').append(clearBtn);
        numToLabels[num_code] = 'clearBtn';

    $("#storage").val(colorSlotsObject);
    $("#storage2").val(numToLabels);
    } else {
        slotBtnNode.innerHTML = 'No Slots';
    }
};


// this is how to keytrigger based on number, now need to tie button to key
// can try to tie to the button which has the characteristics used in change colro
// or can write whole new function which ties those attributes to the key
function checkKey(evt) {

    const numToLabelsObj = $("#storage2").val();
    var key = evt.which || evt.keyCode;
    if (key in numToLabelsObj){
        $('#' + numToLabelsObj[key]).trigger('click');
    }
}


document.addEventListener("keypress", checkKey);

function changeColor(){

    let slotColor = this.style.backgroundColor;
    let selObj = window.getSelection();
    let currentId = this.id;
 
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
    document.designMode = "off";

} 

function removeColor(){

    let selObj = window.getSelection();

    if (selObj.rangeCount && selObj.getRangeAt) {
        range = selObj.getRangeAt(0);
      }
    // Set design mode to on
    document.designMode = "on";
      if (range) {
        selObj.removeAllRanges();
        selObj.addRange(range);
      }

    // remove text color
    document.execCommand("removeFormat", false, "foreColor");
    document.designMode = "off";

}

// If user changes label after doing work - previewed text will reset
function resetTextSelection(){
    if($("#previewText").text()){
    $("#previewText").text('')      
    };
    toggleToPreview();
}

function grabSlotOptions(evt) {

    resetTextSelection();
    selectedLabel = $('#select2-myselLabel-container').attr('title')
    let label = {
        "label": selectedLabel, 
    };

    $.post("/generate_slots", label, displaySlots)

}

// toggles next-preview button and removes preview text
function toggleToNext(){
    $("#next").attr('onclick', 'writeToUserFile()');
    $("#next").text("Next");
    document.getElementById("preview").style.backgroundColor = "#1A95CE";
}

function toggleToPreview() {
    $("#next").attr('onclick', 'processAnnotatedText()');
    $("#next").text("Preview");
    document.getElementById("preview").style.backgroundColor = "";


}

function processAnnotatedText(evt) {

    toggleToNext();
    const textWithHighlights = $('#contentLine').html();
    const colorSlots = $("#storage").val();
    const entities = extractEntities();

    colorSlots = JSON.stringify(colorSlots);
    const annotatedText = {
        "colorSlotsObj": colorSlots,
        "text": textWithHighlights,
        "entities": entities,
    };

    $.post('/process_text', annotatedText, preview)

};

// Instead of sending text to python to process in the above func, keep in JS here:
function extractLabeledEntities(highlightedText){
    let startPos = highlightedText.indexOf("<")
}


function writeToUserFile() {

    toggleToPreview();
    let fileName = $('#select2-mysel-container').attr('title');
    let annotated_text = $('#previewText').text();

    let annotated_pkg = {
        'annotated': annotated_text,
        'fileName': fileName
    }

    $.post('/write_to_file', annotated_pkg, nextLine)
};


function stashColorSlotsObj(colorSlotsObject) {
    //  may need to add functionality for when no slots 
    $("#storage").val(colorSlotsObject)

}


function nextLine(evt) {
    // remove previous text preview from page
    $('#previewText').text('');
    let fileLines = $("#contentPkg").text();
    // Have string, but need an array to do what we want - this comma split
    // doesn't work if there are commas in the data
    let allLines = fileLines.split(",");
    displayLine(allLines);

};

$("#skip").click(alertMe);
$("#next").click(alertMe);

function extractEntities(){
    const rePattern = /">.+?</g;
    const entities = $('#contentLine').html().match(rePattern);
    const cleanEntities = [];
    for (const e of entities) {
        cleanEntities.push(e.slice(2, e.length-1));
    };
    return(cleanEntities);
}

function displayLine(result) {
    // this function takes the result and pops lines off, storing the shortened
    // array each time
    let fileLines = result;
    let lastLine = fileLines.pop();

    // when get to last line, activate modal to indicate choose another file
    if(lastLine.trim().length === 0 ){
        $('.modal').addClass('is-active');
    }

    $("#contentLine").text(lastLine);
    // need the following line to be storage, pick it up in nextLine function
    $("#contentPkg").text(fileLines);  

}
function sendFileName(evt, fname) {

    let fileName = {
        "title": fname, 
    };

    $.post('/annotate_content', fileName, displayLine)
};

function grabFileName(evt) {
    let fname = document.getElementById('select2-mysel-container').title;
    sendFileName(evt, fname)
};


$(".modal-close").click(function() {
   $(".modal").removeClass("is-active");
});

// all code below gets executed
$(document).ready(function() {
    $(".modal-close").click( ()=> {$(".modal").removeClass("is-active")});

   $(".modal").removeClass("is-active");

// below lines are grabbing the user selected file and labels
    $('myselect').on('select2:change', grabFileName);
    $('#myselLabel').on('select2:change', grabSlotOptions);

})