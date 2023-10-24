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