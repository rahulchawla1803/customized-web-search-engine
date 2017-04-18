 $( function() {
      var availableTags_text
      var availableTags
      $.ajax({
             //url: "http://127.0.0.1:5000/autocomplete"

            url: "http://192.168.0.105:5000/autocomplete",
             type: "GET",
             dataType: "text",
             success: function(response) {
                 console.log("Reached index.htm")
                 console.log("db data"+availableTags_text)
                availableTags_text=response
                availableTags=availableTags_text.split(',')

                $( "#tags" ).autocomplete({
                    minLength: 1,
                    source: function (request, response) {
                        console.log("reached autocomplete")
                        var results = $.ui.autocomplete.filter(availableTags, request.term)
                        response(results.slice(0, 8))

                    }
                });
             },
             error: function (xhr, status){
                 print(xhr)
                 print(status)
             }
         });

  });