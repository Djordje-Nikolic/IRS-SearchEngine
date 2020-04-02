function displayloading(url) {
    var img = document.createElement("img");
    img.src = url;
    $('#results_display').html(img);
}

function clearloading() {
    placetodisp = document.getElementById('results_display');
    placetodisp.removeChild(placetodisp.childNodes[0]);
}

function displayresults(results, count) {
    var table = document.createElement("table");
    table.className = "table table-stripped table-hover";

    var table_head = document.createElement("thead");
    table_head.className = "thead-dark";
    table.appendChild(table_head);

    var thead_row = document.createElement("tr");
    table_head.appendChild(thead_row);

    var thead_row_col = document.createElement("th");
    thead_row_col.scope = "col";
    thead_row_col.innerHTML = "#";
    thead_row.appendChild(thead_row_col);

    thead_row_col = thead_row_col.cloneNode(true);
    thead_row_col.innerHTML = "Similarity";
    thead_row.appendChild(thead_row_col);

    thead_row_col = thead_row_col.cloneNode(true);
    thead_row_col.innerHTML = "File";
    thead_row.appendChild(thead_row_col);

    var table_body = document.createElement("tbody");
    table.appendChild(table_body);

    for (var i = 0; i < count; i++) {
        var obj = results.similarities[i];

        var row = document.createElement("tr");

        var col = document.createElement("th");
        col.scope = "row";
        col.innerHTML = i + 1;
        row.appendChild(col);

        col = document.createElement("td");
        col.innerHTML = parseFloat(obj.value).toFixed(5);
        row.appendChild(col);

        col = col.cloneNode(true);
        col.innerHTML = obj.file;
        row.appendChild(col);

        table_body.appendChild(row);
    }

    var timediv = document.createElement("div");
    var timep = document.createElement("p");
    timediv.appendChild(timep);
    timep.innerHTML = `Time taken: ${parseFloat(results.timetaken).toFixed(5)}s`;

    placetodisp = document.getElementById('results_display');
    clearloading();
    placetodisp.appendChild(table);
    placetodisp.appendChild(timediv);
}

function displayerror(status, errorThrown) {

    var errdisp = document.getElementById('err_display');
    if (status)
    {
       var errdiv = document.createElement('div');
       errdiv.className = "alert alert-info";
       errdiv.role = "alert";
       errdiv.innerHTML = status;
       errdisp.appendChild(errdisp);
    }
    if (errorThrown)
    {
        var errdiv = document.createElement('div');
        errdiv.className = "alert alert-info";
        errdiv.role = "alert";
        errdiv.innerHTML = errorThrown;
        errdisp.appendChild(errdisp);
    }
}

function displayerrors(errorList) {
    var frag = document.createDocumentFragment();
    errorList.forEach(function(error){       
        var errdiv = document.createElement('div');
        errdiv.className = "alert alert-info";
        errdiv.role = "alert";
        errdiv.innerHTML = error.toString();
        frag.appendChild(errdiv); 
      });
    document.getElementById('err_display').appendChild(frag);
}

function clearerrors() {

    $('#err_display').empty();
}