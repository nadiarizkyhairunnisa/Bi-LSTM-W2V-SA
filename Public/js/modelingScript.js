function showTables(button_value, data_table) {
  data = { data_option: button_value };
  console.log(data);
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/modeling",
    data: data,
    dataType: "json",
    success: function (data) {
      console.log("data_option after 1st ajax:", data);
      // use the response to from get request (path of csv file) as url
      $.ajax({
        type: "GET",
        url: data.data_path,
        dataType: "text",
        success: function (data) {
          var evaluation_data = data.split(/\r?\n|\r/);
          var table_data =
            '<table class="table table-bordered evaluation" id="dataTable">';
          table_data += "<br>";
          for (var count = 0; count < evaluation_data.length; count++) {
            var cell_data = evaluation_data[count].split(",");
            table_data += "<tr>";
            for (
              var cell_count = 0;
              cell_count < cell_data.length;
              cell_count++
            ) {
              if (count === 0) {
                table_data += "<th>" + cell_data[cell_count] + "</th>";
              } else {
                table_data += "<td>" + cell_data[cell_count] + "</td>";
              }
            }
            table_data += "</tr>";
          }
          table_data += "</table>";
          $(data_table).html(table_data);
        },
      });
    },
  });
}

$(document).ready(function () {
  $("button").click(function (e) {
    if (e.target.name == "hide") {
      $("#" + e.target.value).empty();
      console.log(e.target.value);
    } else {
      var valueButton = e.target.value;
      const valueButtonArray = valueButton.split(",");
      showTables(
        (button_value = valueButtonArray[0]),
        (data_table = "#" + valueButtonArray[1])
      );
    }
  });
});

// $(document).ready(function(){
//     $("#load_data").click(function(e){
//         e.preventDefault();
//         data = {data_option: $(this).val()}
//         console.log("data_option before ajax:", data)
//         $.ajax({
//             type: "POST",
//             url:"http://127.0.0.1:5000/modeling",
//             data:data,
//             dataType:"json",
//             success: function(data) {
//                 console.log("data_option after 1st ajax:", data);
//                 // use the response to from get request (path of csv file) as url
//                 $.ajax({
//                     type: "GET",
//                     url: data.data_path ,
//                     dataType:"text",
//                     success:function(data){
//                         var evaluation_data = data.split(/\r?\n|\r/);
//                         var table_data = '<table class="table table-bordered evaluation" id="dataTable">';

//                         for(var count = 0; count<evaluation_data.length; count++){
//                             var cell_data = evaluation_data[count].split(",");
//                             table_data += '<tr>';
//                             for(var cell_count=0; cell_count<cell_data.length; cell_count++){
//                                 if(count === 0) {
//                                 table_data += '<th>'+cell_data[cell_count]+'</th>';
//                                 } else {
//                                 table_data += '<td>'+cell_data[cell_count]+'</td>';
//                                 }
//                             }
//                             table_data += '</tr>';
//                         }
//                         table_data += '</table>';
//                         $('#data_table').html(table_data);
//                     }
//                 });
//             }
//         })
//     });
// });

// $("#hide").click(function (e) {
//     e.preventDefault();
//     $("#data_table").empty()
// });
