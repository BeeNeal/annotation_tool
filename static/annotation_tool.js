
function alertMe(evt) {
    alert("Zamboni!");
};

function nextLine(evt) {
    let fileLines = $("#contentPkg").text();
    let lastLine = fileLines.split('/n');
    let l = lastLine.pop();
    console.log(typeof(lastLine));
}

$("#skip").click(alertMe);
$("#next").click(alertMe);

function displayLine(result) {
    let fileLines = result;
    // let lastLine = fileLines[fileLines.length - 1];
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

    console.log(fileName["title"])
    // upon selecting the filename, I am reaching this function, with json
    // alert(fileName['title'])
    // now the goal is to send the info up into the url and grab it with python from there
    $.post("/annotate_content", fileName, displayLine)
}

function grabFileName(evt) {
    let fname = document.getElementById('select2-mysel-container').title;
    alert(fname);
    sendFileName(evt, fname)

};

$('myselect').on('select2:change', grabFileName);




// Post request to server which will send back the file. Once JS has the whole
// file, can read it line by line once buttons are used