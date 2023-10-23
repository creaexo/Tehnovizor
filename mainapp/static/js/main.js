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