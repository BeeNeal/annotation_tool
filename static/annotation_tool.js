
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
    // let range = selObj.getRangeAt(0);

    alert(typeof(range))

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

} // changeColor function closing bracket




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

// $(function() {
//     if (selectedRange) {
//             $('#preview').text(selectedRange.toString());
//             // selectedRange.style.backgroundColor = 'blue';
//             clearInterval(timer);
//         }

//     timer = setInterval(getSelectedRange, 150);
// });
// var timer = null;

// var selectedRange = null;

// var getSelectedRange = function() {
//     try {
//         if (window.getSelection) {
//             selectedRange = window.getSelection().getRangeAt(0);
//         } else {
//             selectedRange = document.getSelection().getRangeAt(0);
//             console.log(selectedRange)
//         }
//     } catch (err) {

//     }

// };


// below lines are grabbing the user selected file and labels
$('myselect').on('select2:change', grabFileName);
$('#myselLabel').on('select2:change', grabSlotOptions);

