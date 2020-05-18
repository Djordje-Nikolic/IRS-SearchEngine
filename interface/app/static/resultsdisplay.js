function displayloading(url, appendnode = false) {
    var img = document.createElement("img");
    img.src = url;
    img.tagName = "img";
    if (appendnode)
    {
        $('#results_display').append(img);
    }
    else
    {
        $('#results_display').html(img);
    }
}

function clearloading() {
    var placetodisp = document.getElementById('results_display');
    var lastchild = placetodisp.childNodes[placetodisp.childNodes.length - 1];
    if (lastchild.tagName == "IMG")
        placetodisp.removeChild(lastchild);
}

function displayresults(results, urlforfileopen) {
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
	
	thead_row_col = thead_row_col.cloneNode(true);
	thead_row_col.innerHTML = "";
    thead_row.appendChild(thead_row_col);

    var table_body = document.createElement("tbody");
    table.appendChild(table_body);

    var lastRow = null;
    for (var i = 0; i < results.similarities.length; i++) {
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
        col.innerHTML = obj.filedesc;
        row.appendChild(col);
		
		col = document.createElement("td");
		var btn = document.createElement("a");
		btn.className = "btn btn-primary btn-sm";
		btn.href = urlforfileopen + '?fileid=' + obj.fileid; 
        btn.target = "_blank";
        btn.innerHTML = `<i class="fas fa-external-link-alt fa-lg"></i>` 
		col.appendChild(btn);
		row.appendChild(col);

        table_body.appendChild(row);
        lastRow = row;
    }

    if (window.observer != null && lastRow != null)
    {
        window.observer.observe(lastRow);
    }

    var timediv = document.createElement("div");
    var timep = document.createElement("p");
	var totalc = document.createElement("p");
    timediv.appendChild(timep);
	timediv.appendChild(totalc);
    timep.innerHTML = `Time taken: ${parseFloat(results.timetaken).toFixed(5)}s`;
	totalc.innerHTML = `Total results: ${results.totalcount}`

    var placetodisp = document.getElementById('results_display');
    clearloading();
    placetodisp.appendChild(timediv);
    placetodisp.appendChild(table);
}

function displaynextresults(results, urlforfileopen) {
    var count = results.similarities.length;
    if (count == 0)
        return false;

    var placetodisp = document.getElementById('results_display');
    var table = placetodisp.childNodes[1];
    if (table === null || table.tagName != "TABLE")
        throw "Can't locate table element.";

    var table_body = table.childNodes[1];
    if (table_body === null)
        throw "Can't locate table body.";

    var fragment = document.createDocumentFragment();
    
    var offset = null;
    try
    {
        var lastTableNum = table_body.lastChild.firstChild.innerHTML;
        offset = parseInt(lastTableNum);
    }
    catch (err)
    {
        offset = 0;
    }

    var lastRow = null;
    for (var i = 0; i < count; i++){
        var obj = results.similarities[i];

        var row = document.createElement("tr");

        var col = document.createElement("th");
        col.scope = "row";
        col.innerHTML = i + offset + 1;
        row.appendChild(col);

        col = document.createElement("td");
        col.innerHTML = parseFloat(obj.value).toFixed(5);
        row.appendChild(col);

        col = col.cloneNode(true);
        col.innerHTML = obj.filedesc;
        row.appendChild(col);
		
		col = document.createElement("td");
		var btn = document.createElement("a");
		btn.className = "btn btn-primary btn-sm";
		btn.href = urlforfileopen + '?fileid=' + obj.fileid; 
        btn.target = "_blank";
        btn.innerHTML = `<i class="fas fa-external-link-alt fa-lg"></i>` 
		col.appendChild(btn);
		row.appendChild(col);

        fragment.appendChild(row);
        lastRow = row;
    }

    if (window.observer != null)
    {
        window.observer.observe(lastRow);
    }

    clearloading();
    table_body.appendChild(fragment)

    return true;
}


function displayerror(status, errorThrown) {

    var errdisp = document.getElementById('err_display');
    if (status)
    {
       var errdiv = document.createElement('div');
       errdiv.className = "alert alert-info";
       errdiv.role = "alert";
       errdiv.innerHTML = status;
       errdisp.appendChild(errdiv);
    }
    if (errorThrown)
    {
        var errdiv = document.createElement('div');
        errdiv.className = "alert alert-info";
        errdiv.role = "alert";
        errdiv.innerHTML = errorThrown;
        errdisp.appendChild(errdiv);
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