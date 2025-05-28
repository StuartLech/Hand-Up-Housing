(function() {
  function applyTheme(mode) {
    var btn = document.getElementById('theme-toggle');
    if (mode === 'light') {
      document.body.classList.add('light-mode');
      if (btn) btn.textContent = 'Dark Mode';
    } else {
      document.body.classList.remove('light-mode');
      if (btn) btn.textContent = 'Light Mode';
    }
  }

  var stored = localStorage.getItem('theme');
  applyTheme(stored === 'light' ? 'light' : 'dark');

  window.toggleTheme = function() {
    var isLight = document.body.classList.contains('light-mode');
    var newMode = isLight ? 'dark' : 'light';
    localStorage.setItem('theme', newMode);
    applyTheme(newMode);
  };
})();
