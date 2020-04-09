
function generate_table(k) {
	  // get the reference for the body
	  var body = document.getElementsByTagName("body")[0];

	  // creates a <table> element and a <tbody> element
	  var tbl = document.createElement("table");
	  var tblBody = document.createElement("tbody");

	  var count = 0;
	  // creating all cells
	  for (var i = 1; i < 6; i++) {
	    // creates a table row
	    var row = document.createElement("tr");
	    
	    for (var j = 1; j < 5; j++) {
	      // Create a <td> element and a text node, make the text
	      // node the contents of the <td>, and put the <td> at
	      // the end of the table row
	      count += 1
	      var num = k*count
	      var cell = document.createElement("td");
	      var cellText = document.createTextNode(""+ num);
	      cell.appendChild(cellText);
	      row.appendChild(cell);
	    }

	    // add the row to the end of the table body
	    tblBody.appendChild(row);
	  }

	  // put the <tbody> in the <table>
	  tbl.appendChild(tblBody);
	  // appends <table> into <body>
	  body.appendChild(tbl);
	  // sets the border attribute of tbl to 2;
	  tbl.setAttribute("border", "2");

}

	