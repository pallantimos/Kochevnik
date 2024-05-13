document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with class 'Rectangleleft' and 'plus'
    var minusButtons = document.querySelectorAll('.Rectangleleft');
    var plusButtons = document.querySelectorAll('.plus');

    // Iterate over all minus buttons and add click event listener
    minusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Get the corresponding 'kols' element
            var kolsElement = button.parentElement.querySelector('.kols p');
            
            // Get the current value of 'kols'
            var currentValue = parseInt(kolsElement.textContent);
            
            // Decrease the value by 1 but not below 0
            var newValue = Math.max(currentValue - 1, 0);
            
            // Update the 'kols' element with the new value
            kolsElement.textContent = newValue;
        });
    });

    // Iterate over all plus buttons and add click event listener
    plusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Get the corresponding 'kols' element
            var kolsElement = button.parentElement.querySelector('.kols p');
            
            // Get the current value of 'kols'
            var currentValue = parseInt(kolsElement.textContent);
            
            // Increase the value by 1
            var newValue = currentValue + 1;
            
            // Update the 'kols' element with the new value
            kolsElement.textContent = newValue;
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('scroll', handleScroll);

    function handleScroll() {
        var footer = document.querySelector('footer');
        var scrollStopper = document.getElementById('scrollStopper');

        var footerPosition = footer.getBoundingClientRect().top;
        var windowHeight = window.innerHeight;

        // Adjust the value as needed to control when scrolling is disabled
        if (footerPosition < windowHeight / 2) {
            scrollStopper.style.height = '0';
        } else {
            scrollStopper.style.height = '50px'; // Adjust as needed to match your footer height
        }
    }
});

const $next = document.querySelector('.next');
const $prev = document.querySelector('.prev');

$next.addEventListener(
  'click',
  () => {
    const items = document.querySelectorAll('.item');
    document.querySelector('.slide').appendChild(items[0]);
  },
);

$prev.addEventListener(
  'click',
  () => {
    const items = document.querySelectorAll('.item');
    document.querySelector('.slide').prepend(items[items.length - 1]);
  },
);

const $nexts = document.querySelector('.next-hotel');
const $prevs = document.querySelector('.prev-hotel');

$next.addEventListener(
  'click',
  () => {
    const items = document.querySelectorAll('.item-hotel');
    document.querySelector('.slide-hotel').appendChild(items[0]);
  },
);

$prev.addEventListener(
  'click',
  () => {
    const items = document.querySelectorAll('.item-hotel');
    document.querySelector('.slide-hotel').prepend(items[items.length - 1]);
  },
);