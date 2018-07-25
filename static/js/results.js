(function($){
  $.get('/poll/result/user', function(data) {
    var $results = $('#your-results')
    for(var key in data) {
      var poll = data[key];

      const header = `<h3>Poll: ${poll.title}</h3>`;
      const choice = `<div>Your Choice: ${poll.choice}</div>`;
      const score = `<div>Score: ${poll.total_score}</div>`;

      $results.append(
        header + choice + score
      );
    }
    $.get('/poll/result/overall', function(data) {
      var $results = $('#overall-results')
      for(var key in data) {
        var poll = data[key];

        const header = `<h3>Poll: ${poll.title}</h3>`;
        var numbers = [`<h5>Choice by value</h5>`];
        for(var choice in poll.choices){
          numbers.push(
            `<div><strong>${choice}</strong>&nbsp;${poll.choices[choice]}</div>`  
          )
        }
        
        const correctChoice = `<div>The correct choice: ${poll.choice}</div>`;
        const score = `<div>Cumulative, overall Score: ${poll.total_score}</div>`;

        $results.append(
          header + correctChoice + numbers.join('\n') + score
        );
      }
    });
  });
})(jQuery);
