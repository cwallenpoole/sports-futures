(function($){
  var id = false;
  var form = false;
  $(
    function() {
      form = $('#submit-form');
setInterval(function(){
      $.get(
        '/poll/current',
        function(data) {
          if(id && data.id !== id) {
            form.submit();
          }
          if(!form.find('.question').length) {
            id = data.id;
            for(var i = data.options.length - 1; i >= 0; i--) {
              form.prepend(
                '<div class="form-group">'
                +'<button name="option" class="question form-control" value="'+i+'" >' + data.options[i] + '</button></div>'
                
              );
            }
            $('<h3>' + data.title + '</h3>').insertBefore(
              form
            );
            form.append(
              '<input type="hidden" name="poll_id" value="' + id + '" />'
            );
          }
        }
      );
    }, 500);
    }
  );
})(jQuery);
