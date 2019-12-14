$(function(){

  $('#search').keyup(function() { //looks for the uparrow in the search id of the html page

    $.ajax({
      type: 'POST',
      url: "search/", //views file
      data: {
        'search_text' : $('#search').val(),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: searchSuccess,
      dataType: 'html'
    });
  });
});
  function searchSuccess(data, textStatus, jqXHR)
  {
      $('#search-results').html(data);  //references the id in the prduct_list.html page
  }
