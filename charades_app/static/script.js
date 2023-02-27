var currentCategoryId = null;
var currentWordIndex = 0;
var currentWords = [];

function getWords(categoryId) {
  fetch(`/category/${categoryId}/words`)
    .then(response => response.json())
    .then(words => {
      currentWords = words;
      currentWordIndex = 0;
      updateWordDisplay();
    });
}

function updateWordDisplay() {
  var word = currentWords[currentWordIndex];
  document.getElementById('word_name').innerHTML = word.name;
  document.getElementById('hint-header').innerHTML = 'Hint';
  document.getElementById('hint').innerHTML = word.hint;
}

document.getElementById('category_select').addEventListener('change', event => {
  currentCategoryId = event.target.value;
  getWords(currentCategoryId);
});

document.getElementById('next_button').addEventListener('click', event => {
  currentWordIndex++;
  if (currentWordIndex >= currentWords.length) {
    currentWordIndex = 0;
  }
  updateWordDisplay();
});

document.getElementById('prev_button').addEventListener('click', event => {
  currentWordIndex--;
  if (currentWordIndex < 0) {
    currentWordIndex = currentWords.length - 1;
  }
  updateWordDisplay();
});