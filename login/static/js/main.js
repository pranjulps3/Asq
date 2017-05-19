// $('#follow').click(function(){
//       $.ajax({
//                type: "POST",
//                url: "{{{ url 'follow_request'}}",
//                data: {'user_id': $(this).attr('data'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//                dataType: "json",
//                success: function(response) {
//                       alert(response.message);
//                 },
//                 error: function(rs, e) {
//                        alert(rs.responseText);
//                 }
//           }); 
//     })