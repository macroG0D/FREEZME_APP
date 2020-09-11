const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList;
const SpeechRecognitionEvent = window.SpeechRecognitionEvent || window.webkitSpeechRecognitionEvent;



// select table elements
const tablerow = document.querySelectorAll('.table-row');

// search input object
const inputtext = document.querySelector('.search-input');

const voice_in = document.querySelectorAll('.voice-input');

// select remove button
const removebtn = document.querySelector('.btn-remove');
// select edit button
const ctrl_edit = document.querySelector('.btn-edit');

const donebtn = document.querySelector('.btn-done');

// SpeechRecognition object
const recognition = new SpeechRecognition();
// const voice_input = document.querySelector('.search-input');

// shows the results while i'm speaking, without waiting until finished
recognition.interimResults = true;

// checking user input language
const userlang = document.querySelector('#userlang').innerText;

try {

    let langselector = document.querySelectorAll('.langopt');
    for (let i = 0; i < langselector.length; i++) {
        if (langselector[i].value == userlang) {
            langselector[i].setAttribute('selected', 'selected');
        }
    }


} catch (e) { }

// Set voice recognition language  
recognition.lang = userlang;
// recognition.lang = 'en'; 
let input_field = '';
let transcript = '';
recognition.addEventListener('result', e => {
    let voice_input = '';
    transcript = '';
    console.log(e);
    transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');
    // console.log(transcript);
    // inputtext.value = transcript;
    // voice_input.value = transcript;
    input_field.value = transcript;
});


// Sounds for voice search query On and Off
let soundOk = new Audio('../static/sounds/Ok.mp3');
let sounBye = new Audio('../static/sounds/bye.mp3');


// Search by speech
let voice_search = function () {
    input_field = inputtext;
    soundOk.play();
    recognition.start();
    // call stop function when stop talking
    recognition.onspeechend = () => {
        sounBye.play();
        recognition.stop();
        stopsearch();
    };
};


// Stop search functions
let stopsearch = function () {
    sounBye.play();
    recognition.stop();
    filter();
};


// define var for selected item in table
let selected = '';

let selected_info = [];

let body = {};
body = {};

let selected_wishlistItems = new Set();
// selected_wishlistItems = [];

// selecting item in table
for (let i = 0; i < tablerow.length; i++) {
    tablerow[i].addEventListener("click", function () {

        if (this.classList.contains('table-active')) {
            this.classList.remove('table-active');
            selected = '';

            try {
                tablerow[i].querySelector('#checkbox_btn').checked = false;
                tablerow[i].classList.remove('selected-row');
                selected_wishlistItems.delete(tablerow[i].childNodes[1].innerText);

            } catch (e) { }

            try {
                removebtn.classList.add('disable');
            } catch (e) { }

            try {
                ctrl_edit.classList.add('disable');
            } catch (e) { }

            try {
                donebtn.classList.add('disable');
            } catch (e) { }

        } else {
            for (let i = 0; i < tablerow.length; i++) {
                if (tablerow[i].classList.contains('table-active')) {
                    tablerow[i].classList.remove('table-active');
                }
            }
            this.classList.add('table-active');
            selected = tablerow[i];
            try {
                selected.querySelector('#checkbox_btn').checked = true;
                selected.classList.add('selected-row');
                selected_id = selected.childNodes[1].innerText;
                // console.log(selected_id);
                selected_wishlistItems.add(selected_id);
                // console.log(selected_wishlistItems);

                selected_wishlistItems_array = Array.from(selected_wishlistItems);

            } catch (e) { }

            // console.log(selected.querySelector('#checkbox'))
            // item id
            selected_info[1] = selected.childNodes[1].innerText;
            // item name
            selected_info[2] = selected.childNodes[3].innerText;

            // split the table cell value to get seoerated values in the array [quantity, units]
            let quantity_units = selected.childNodes[5].innerText.split(' ');

            // item quantity
            selected_info[3] = quantity_units[0];
            // item units
            selected_info[4] = quantity_units[1];
            // descr
            selected_info[5] = selected.childNodes[7].innerText;

            try {
                removebtn.classList.remove('disable');
            } catch (e) { }

            try {
                ctrl_edit.classList.remove('disable');
            } catch (e) { }

            try {
                donebtn.classList.remove('disable');
            } catch (e) { }

        }
    });
}



// remove selected item
removeitem = function () {
    multiselect = document.querySelectorAll('.selected-row');
    for (let i = 0; i < multiselect.length; i++) {
        multiselect[i].remove();
    }
    try {
        selected.parentNode.removeChild(selected);
    } catch (e) { }

    try {
        removebtn.classList.add('disable');
    } catch (e) { }

    try {
        ctrl_edit.classList.add('disable');
    } catch (e) { }

    try {
        donebtn.classList.add('disable');
    } catch (e) { }
};


// live search filter function

// search input max length counter
let SearchInputMaxlength = 0;

let filter = function () {
    // selecting all the items names in the table
    let allItems = document.querySelectorAll('.item-row');

    // if input length is shorter then max length, then this is a max length
    if (SearchInputMaxlength < inputtext.value.length) {
        SearchInputMaxlength = inputtext.value.length;
    } else {
        // else if max length is greater then the input, then the user deleted one or more input characters and need to restore all the hidden elements
        for (let i = 0; i < tablerow.length; i++) {
            if (tablerow[i].classList.contains('hidden')) {
                tablerow[i].classList.remove('hidden');
            }
        }
    }

    // main search algorithm loop
    // 1 for is itterating throught all the rows names
    for (let i = 0; i < allItems.length; i++) {
        // 2 for if itterating throught the length of the input
        for (var k = 0; k < SearchInputMaxlength; k++) {
            // need try to prevent errors when nothing to compare with
            try {
                // if input value k index is the same as the k index of the name string in the row — we got match and don't need any action
                if (inputtext.value[k].toLowerCase() === allItems[i].innerText[k].toLowerCase()) {
                    // don't need an action, becouse match found and don't need to hide it
                } else {
                    // else if the world doesn't match, hide it
                    allItems[i].parentElement.classList.add('hidden');
                }
            } catch (e) { }
        }
    }
};


// calls the filter function when input changed
try {
    inputtext.addEventListener('input', filter);
} catch (e) { }

// remove selected table row on remove button click
try {
    removebtn.addEventListener('click', removeitem);
} catch (e) { }

try {
    donebtn.addEventListener('click', removeitem);
} catch (e) { }


function inputfocus() {
    document.querySelector('.item-input').focus();
}


// check the table quantity cells for floats with zeros (12.0 etc), and if after the dot is 0, doesn't show it
let qntval = document.querySelectorAll('.qntval');
// console.log(qntval);
for (let i = 0; i < qntval.length; i++) {
    let x = qntval[i].textContent.split('.');
    // need to split the x array again, becouse after the first split we got x[1] 0 + quantity unit devided by space. So split it by ' ' (space) to nested array like [0, unit] 
    x[1] = x[1].split(' ');
    // console.log(x);
    if (x[1][0] == '0') {
        qntval[i].textContent = `${x[0]} ${x[1][1]}`;
    }
}


// modal items
const modal = document.querySelector(".modal");
const modaladd = document.querySelector(".modal-pop");

// modal popup function
callModal = function (type) {
    document.querySelector('.button-placeholder').innerHTML = ` <button type="submit" name="${type}" value="${type}" class="btn-ctrl btn-${type} modal-btn"> ${type.toUpperCase()} </button>`;
    setTimeout(inputfocus, 100);


    // Prevent number input from e and E input
    document.querySelector(".qnt-input").addEventListener("keypress", function (e) {
        if (e.key == 'e' || e.key == 'E') {
            e.preventDefault();
        }
    });


    // voice input on add and edit fields
    for (let i = 0; i < voice_in.length; i++) {
        voice_in[i].addEventListener('click', function () {
            // console.log(this);
            input_field = this.previousSibling;
            soundOk.play();
            recognition.start();
            // call stop function when stop talking
            recognition.onspeechend = () => {
                sounBye.play();
                recognition.stop();
            };
        });
    }


    if (type == 'add') {
        // setting and updating form values and placeholders for add
        document.querySelector('.modal-pop h3').textContent = 'Add item';
        document.querySelector('.item-input').placeholder = 'Item name';
        document.querySelector('.qnt-input').placeholder = 'Quantity';
        document.querySelector('.item-input').value = '';
        document.querySelector('.qnt-input').value = '';
        document.querySelector('.item-input').required = true;
        document.querySelector('.qnt-input').required = true;
    }

    else if (type == 'edit') {
        // setting and updating form values and placeholders for edit
        document.querySelector('.modal-pop h3').textContent = 'Edit item';
        document.querySelector('.item-input').placeholder = `${selected_info[2]}`;
        document.querySelector('.qnt-input').placeholder = `${selected_info[3]}`;
        document.querySelector('.item-input').value = '';
        document.querySelector('.qnt-input').value = '';
        document.querySelector('.item-input').required = false;
        document.querySelector('.qnt-input').required = false;

        // set selected option like items qnt_units_old (selected_info[4]) 
        let myoption = document.querySelectorAll('option');
        for (let i = 0; i < myoption.length; i++) {
            if (myoption[i].value == selected_info[4].toLowerCase()) {
                myoption[i].selected = "selected";
            }
        }
        // hidden form inputs with defined values equals to selected row in a table — the values passed to the server on submit to check which item should be changed
        document.querySelector('.button-placeholder').innerHTML += `<input class="hidden" type="text" name="id_old" value="${selected_info[1]}">`;
        document.querySelector('.button-placeholder').innerHTML += `<input class="hidden" type="text" name="name_old" value="${selected_info[2]}">`;
        document.querySelector('.button-placeholder').innerHTML += `<input class="hidden" type="text" name="quantity_old" value="${selected_info[3]}">`;
        document.querySelector('.button-placeholder').innerHTML += `<input class="hidden" type="text" name="qnt_units_old" value="${selected_info[4]}">`;
        document.querySelector('.button-placeholder').innerHTML += `<input class="hidden" type="text" name="descr_old" value="${selected_info[5]}">`;
    }

    modal.classList.add('modal-active');
    modaladd.style = 'top: 50%;';
};

// modal hide function
window.onclick = function (event) {
    if (event.target == modal) {
        modal.classList.remove('modal-active');
        modaladd.style = 'top: 70%;';
    }
};


// const requestURL = 'http://127.0.0.1:5000/';
const requestURL = window.location.href;



function sendRequest(method, url, body = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    return fetch(url, {
        method: method,
        body: JSON.stringify(body),
        headers: headers
    }).then(response => {
        return response.json();
    });
}


let post = function (actiontype) {

    body = {
        action: actiontype,
        id: selected_info[1],
        name: selected_info[2],
        qantity: selected_info[3],
        units: selected_info[4],
        descr: selected_info[5]
    };
    // console.log(body);
    sendRequest('POST', requestURL, body)
        .then(data => console.log(data))
        .catch(err => console.log(err));
};

let remove_wishlist = function () {
    body = {
        action: 'remove_wishlist',
        id: selected_wishlistItems_array
    };
    sendRequest('POST', requestURL, body)
        .then(data => console.log(data))
        .catch(err => console.log(err));
};


let done_wish = function () {
    body = {
        action: 'done_wish',
        id: selected_wishlistItems_array
    };
    sendRequest('POST', requestURL, body)
        .then(data => console.log(data))
        .catch(err => console.log(err));
};


let clearHistory = function () {
    body = {
        action: 'clearHistory'
    };
    sendRequest('POST', '/history', body)
        .then(data => console.log(data))
        .catch(err => window.location.replace("history"));
};


let clearHistoryConfirm = function () {
    let conf = confirm('By this action you will delete all the fridge history. Are you sure?');
    console.log(conf);
    if (conf == true) {
        // event.preventDefault();
        console.log('ok');
        clearHistory();

    } else {
        event.preventDefault();
        return false;
    }
};



// active menu links style
const active_nav = function () {
    let mnu_items = document.querySelectorAll('.mnu_item');
    for (let i = 0; i < mnu_items.length; i++) {
        if (mnu_items[i].href == window.location.href) {
            mnu_items[i].classList.add('active_mnu_item');
        }
    }
};
active_nav();

// adaptive table height
let tableheight = function () {
    let y = window.innerHeight;
    if (y <= 770) {
        y -= y * 0.6;
    } else {
        y -= y * 0.45;
    }

    try {
        document.querySelector('tbody').style = `max-height: ${y}px`;
        tbody = document.querySelector('tbody');
    } catch (e) { }
};
tableheight();

// set history table rows colors
const history_colors = function () {
    if (window.location.pathname == '/history') {
        let rows = document.querySelectorAll('#event');

        for (let i = 0; i < rows.length; i++) {
            if (rows[i].textContent == 'Removed') {
                rows[i].parentElement.classList.add('removedItem');
            } else if (rows[i].textContent == 'Updated') {
                rows[i].parentElement.classList.add('updatadeItem');
            } else if (rows[i].textContent == 'Added') {
                rows[i].parentElement.classList.add('addedItem');
            }
        }
    }
};
history_colors();


// Google the items by name function
try {
    let itemNameInRow = document.querySelectorAll('.item-row');

    for (let i = 0; i < itemNameInRow.length; i++) {
        let googleit = `https://www.google.com/search?q=${itemNameInRow[i].querySelector('a').innerText}`;
        itemNameInRow[i].querySelector('a').href = googleit;
        itemNameInRow[i].querySelector('a').setAttribute('target', '_blank');
    }



} catch (e) { }


// burger menu function
let burger_mnu = function () {
    let nav_items = document.querySelector('.burger_mnu_items');
    if (nav_items.classList.contains('hidden')) {
        nav_items.classList.remove('hidden');
        nav_items.classList.add('active');
    } else {
        nav_items.classList.add('hidden');
        nav_items.classList.remove('active');
    }
};

// burger menu click
document.querySelector('.burger_mnu').addEventListener('click', burger_mnu);