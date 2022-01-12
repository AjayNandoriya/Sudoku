
const N = 9; 
var current_state = new Array(N);

for (var i = 0; i < current_state.length; i++) {
  current_state[i] = new Array(N);
  for(var j = 0; j < current_state[i].length; j++) {
      current_state[i][j] = (i+j)%9 + 1;
  }
}

function reset_sudoku(){
    var doc = document;
    for (i = 0; i < 9; i++) {
        for (j = 0; j < 9; j++) {
            var id="r" + (i+1).toString() + "c" + (1+j).toString();
            console.log(id);
            var d = doc.getElementById(id);
            if(current_state[i][j] != 0) {
            d.innerHTML = current_state[i][j].toString();
            }
        }
    }
}

document.ready = reset_sudoku();