(function($){
  var id = false;
  var form = false;
  $(
    function() {
      form = $('#submit-form');
      id = $('#poll-id').val();
setInterval(function(){
      var query = id ?('?poll_id=' + id): '';
      $.get(
        '/poll/current' + query,
        function(data) {
          if(id && data.id != id || data.expired) {
            form.submit();
          }
          if(!form.find('.question').length) {
            id = data.id;
            for(var i = data.options.length - 1; i >= 0; i--) {
              form.prepend(
                '<div class="form-group">'
                +'<button name="option" class="question form-control" value="'+(i + 1)+'" >' + data.options[i] + '</button></div>'
                
              );
            }
            $('<h3>' + data.title + '</h3>').insertBefore(
              form
            );
            $('#poll-id').val(id);
          }
        }
      );
    }, 500);
    }
  );
})(jQuery);
