function toggleMenu() {
    var menuBar = document.getElementById('menuBar');
    menuBar.classList.toggle('active');
  }
  
  function navigateToPage() {
    window.location.href = '/HTML/results.html';
  }
  
  function showRetractnav(){
    const retractbar = document.querySelector('.retractnav')
    retractbar.style.display = 'flex' 
  }
  
  function clossRetractnav(){
    const closemenu = document.querySelector('.retractnav')
    closemenu.style.display = 'none' 
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            window.location.href = 'user.html';
        });
    }
  });
  