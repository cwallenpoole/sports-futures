(function($){
  $.get('/poll/result/user', function(data) {
    var $results = $('#your-results');
    
    var yourTotal = 0;
    for(var key in data) {
      var poll = data[key];

      const header = `<h3>Poll: ${poll.title}</h3>`;
      const choice = `<div>Your Choice: ${poll.choice}</div>`;
      const score = `<div>Score: ${poll.total_score}</div>`;

      $results.append(
        header + choice + score
      );

      yourTotal += poll.total_score;
    }
$results.append(
        `<h2>YOUR Total points across all polls: ${yourTotal}</h2>`
      );
    function updateGlobalResults() {
    $.get('/poll/result/overall', function(data) {
      var $results = $('#overall-results');
      $results.html('');
      var allPoints = 0;
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
        const score = `<div>Cumulative Score: ${poll.total_score}</div>`;

        allPoints += Number(poll.total_score) || 0;
        $results.append(
          header + correctChoice + numbers.join('\n') + score
        );
      }
      $results.append(
        `<h2>Total points across all polls: ${allPoints}</h2>`
      );
    });
    }
     updateGlobalResults();
    setInterval( updateGlobalResults, 500 )
  });
})(jQuery);
