
function alertMe(evt) {
    alert("Zamboni!");
};

$("#skip").click(alertMe);

function displayLine(result) {
    alert(result)
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