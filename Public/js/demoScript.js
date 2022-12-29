$("#submit").click(function (e) {
  e.preventDefault();
  const ulasan = $("#ulasan").val(), //save ulasan value to variable
    data = {
      ulasan: ulasan,
      preproc: $("input[name='radioPreproc']:checked").val(),
      model: $("input[name='radioModel']:checked").val(),
    };
  //save ulasan, preproc and model option to JSON object, mirip dictionary di Python
  console.log("1st", data); //check data in console
  const regex = "[a-zA-Z]+"; //check whether ulasan contains at least one word after preprocessing
  const found = ulasan.toLowerCase().match(regex); //match regex to ulasan
  if (found == null) {
    alert(
      "Teks ulasan setidaknya harus memuat satu kata \n Silakan masukan ulang teks!"
    );
  } else {
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "http://127.0.0.1:5000",
      data: data,
      success: function (data, status, xhr) {
        console.log("2nd", data);
        $("#result").append('<br/>Processed text: "');
        $("#result").append(data.ulasan + '"<br/>');
        $("#result").append('Preprocessing option: "');
        $("#result").append(data.preproc + ", ");
        $("#result").append('model option: "');
        $("#result").append(data.model + '"<br/>');
        $("#result").append(data.result + "<br/>");
      },
    });
  }
  console.log(found);
});

$("#reset").click(function (e) {
  e.preventDefault();
  $("#ulasan").val("");
  $("#defaultCheck1").prop("checked", false);
  $("#defaultCheck2").prop("checked", false);
  $("#defaultCheck3").prop("checked", false);
  $("#result").empty();
});
