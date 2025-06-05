document.addEventListener('DOMContentLoaded', function () {
  const forms = document.querySelectorAll('.delete-form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!confirm('Are you sure you want to delete this post?')) {
        e.preventDefault();
      }
    });
  });
});
