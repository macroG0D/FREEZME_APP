document.querySelector('.pic-overlay').onclick = function() {
    document.querySelector('#pic-change').click();
};


document.querySelector("#pic-change").onchange = function() {
    document.querySelector("#user-pic_form").submit();
};