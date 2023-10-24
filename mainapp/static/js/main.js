var qty_items = document.querySelectorAll('.qty_items');
var final_price_items = document.querySelectorAll('.final_price_items');

var qty = 0;
qty_items.forEach(function(element) {
        qty += parseInt(element.innerHTML);
      });
document.querySelector('.total_qty').innerHTML = qty;
var price = 0;
final_price_items.forEach(function(element) {
        console.log(parseFloat(element.textContent.replace(',', '.')));
        price += parseFloat(element.textContent.replace(',', '.'));
        console.log(price);
      });
document.querySelector('.total_price').innerHTML = price+' руб.';

document.querySelectorAll('.count .plus').forEach(item => {

    item.addEventListener('click', function () {

        ++item.parentElement.querySelector('input').value;

        if (item.parentElement.querySelector('input').value > 1) {

            item.parentElement.querySelector('.minus').classList.remove('min');

        }

    });

});

document.querySelectorAll('.count .minus').forEach(item => {

    item.addEventListener('click', function () {

        --item.parentElement.querySelector('input').value;

        if (item.parentElement.querySelector('input').value < 2) {

            item.parentElement.querySelector('input').value = 1

            item.classList.add('min');

        }

    });

});

document.getElementById('validationFormCheck1').onchange = function() {
    document.getElementById('startDate').disabled = !this.checked;
    document.getElementById('startTime').disabled = !this.checked;
};