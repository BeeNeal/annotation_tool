
function alertMe(evt) {
    alert("Zamboni!");
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
        //  let slots = eval('(' + result + ')'); <-worse way to do the above line

        // initializing object for slot to color processing in python
        let colorSlotsObject = {};
        let colorOptions = ['#ff4e00', '#8ea604', '#f5bb00', '#a23b72', '#2e86ab'];
        let colorCounter = 0;

        slots.forEach (( function(v) {
            colorSlotsObject[colorOptions[colorCounter]] = v;
            let button = document.createElement('button');
            button.type = 'button';
            button.id = v;
            button.className = 'slotOptionBtn noselect';
            button.addEventListener("click", changeColor);
            button.innerHTML = v;
            button.style.backgroundColor = colorOptions[colorCounter];
            colorCounter ++;
            $('#slotOptions').append(button);

        }));

        let clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.id = 'clearBtn';
        clearBtn.className = 'slotOptionBtn';
        clearBtn.addEventListener("click", removeColor);
        clearBtn.innerHTML = 'clear selection';
        clearBtn.style.backgroundColor = 'blue';
        $('#slotOptions').append(clearBtn);

    $("#storage").val(colorSlotsObject);
    } else {
        slotBtnNode.innerHTML = 'No Slots';
    }
};



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
    // Set design mode to off
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
    // Set design mode to off
    document.designMode = "off";

}


function grabSlotOptions(evt) {

    selectedLabel = $('#select2-myselLabel-container').attr('title')
    let label = {
        "label": selectedLabel, 
    };

    $.post("/generate_slots", label, displaySlots)

}

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
    let textWithHighlights = $('#contentLine').html();
    let colorSlots = $("#storage").val();
    colorSlots = JSON.stringify(colorSlots);
    let annotatedText = {
        "colorSlotsObj": colorSlots,
        "text": textWithHighlights,
    };

    $.post('/process_text', annotatedText, preview)

};


function writeToUserFile() {

    toggleToPreview()
    let fileName = $('#select2-mysel-container').attr('title');
    let annotated_text = $('#previewText').text();

    let annotated_pkg = {
        'annotated': annotated_text,
        'fileName': fileName
    }

    $.post('/write_to_file', annotated_pkg, nextLine)
};


function stashColorSlotsObj(colorSlotsObject) {
    //  add functionality for when no slots - deal with it when it breaks,
    // may handle on python side
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

//    let lastLine = fileLines.split("\n");

};

$("#skip").click(alertMe);
$("#next").click(alertMe);

function displayLine(result) {
    // this function takes the result and pops lines off, storing the shortened
    // array each time
    let fileLines = result;
    // let lastLine = fileLines[fileLines.length - 1];
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