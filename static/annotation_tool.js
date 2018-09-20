
function selectFileName() {
    let name = $("#select2-wk8q-container").title()
    console.log(fname)
}

$(".myselect").on("select2:select", function selectFileName(e) { 
  let fname = $(e.currentTarget).val();
  console.log('hurray')
  console.log(fname)
});

function alertMe(evt) {
    alert("Zamboni!");
};

$("#skip").click(alertMe);

function dewit(evt) {
    let fname = document.getElementById('select2-mysel-container').title
    alert(fname);

};

$('myselect').on('select2:change', dewit(evt));


    // var fname = document.getElementById('mysel').title
    // console.log(fname)


