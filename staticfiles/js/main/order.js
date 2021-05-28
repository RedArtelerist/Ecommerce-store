$(document).ready(function() {
    $('#id_city').select2();
});

const form = document.getElementById('orderForm');
const customer_first_name = document.getElementById('id_customer_first_name');
const customer_last_name = document.getElementById('id_customer_last_name');
const customer_email = document.getElementById('id_customer_email');
const customer_phone = document.getElementById('id_customer_phone');
const city = document.getElementById('id_city');
const address = document.getElementById('id_address');
const recipient_first_name = document.getElementById('id_recipient_first_name');
const recipient_last_name = document.getElementById('id_recipient_last_name');
const recipient_email = document.getElementById('id_recipient_email');
const submit = document.getElementById('order-submit-btn');
var customer_fields = [customer_first_name, customer_last_name, customer_email];
var recipient_fields = [recipient_first_name, recipient_last_name, recipient_email];

for(let i = 0; i < customer_fields.length; i++){
    customer_fields[i].addEventListener('input', function (e){
        recipient_fields[i].value = e.target.value;
    });
}

// mask for mobile phone
$(window).load(function() {
    var phones = [{ "mask": "+38(###) ###-##-##"}];
    $('#id_customer_phone').inputmask({
        mask: phones,
        greedy: false,
        definitions: { '#': { validator: "[0-9]", cardinality: 1}} });
});

// if recipient
$('#shipto').change(function () {
    if($(this).is(':checked')) {
        $('.recipient').slideUp();
    } else {
        $('.recipient').slideDown();
    }
});

/*---------------------------------------------- Form Validation-------------------------------------------*/

//Show input error messages
function showError(input, message) {
    let formControl = input.parentElement;

    if(formControl.className.includes("col-md-6"))
        formControl.className = "col-md-6 mb-3 order-form-control error";
    else
        formControl.className = "mb-3 order-form-control error";

    const small = formControl.querySelector('small');
    small.innerText = message;
}

//show success colour
function showSucces(input) {
    let formControl = input.parentElement;
    if(formControl.className.includes("col-md-6"))
        formControl.className = "col-md-6 mb-3 order-form-control success";
    else
        formControl.className = "mb-3 order-form-control success";
}

function checkName(input) {
    const re = /^[a-zA-Z]+$/;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    }else {
        showError(input,`${input.dataset.name} must contains only letters`);
    }
}

function checkEmail(input) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    }else {
        showError(input,'Email is not invalid');
    }
}

function checkPhone(input) {
    const re = /^[+]?[\s./0-9]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]{9,14}$/g;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    }else {
        showError(input,'Mobile phone is not invalid');
    }
}

//checkRequired fields
function checkRequired(inputArr) {
    inputArr.forEach(function(input){
        if(input.value.trim() === ''){
            showError(input,`${input.dataset.name} is required`)
        }else {
            showSucces(input);
            return true;
        }
    });
}


function checkLength(input, min ,max) {
    if(input.value.length < min) {
        showError(input, `${input.dataset.name} must be at least ${min} characters`);
    }else if(input.value.length > max) {
        showError(input, `${input.dataset.name} must be les than ${max} characters`);
    }else {
        showSucces(input);
        return true;
    }
}

function validateName(input){
     if(!checkLength(input, 3, 20))
        return false;
    else
        return checkName(input);
}

function validate(){
    var a = validateName(customer_first_name);
    var b = validateName(customer_last_name);
    var c = checkLength(city, 3,50);
    var d = checkLength(address, 5,100);
    var e = validateName(recipient_first_name);
    var f = validateName(recipient_last_name);

    var m = checkEmail(customer_email);
    var l = checkEmail(recipient_email);
    var k = checkPhone(customer_phone);
    return a && b && c && d && e && f && m && l && k;
}


//Event Listeners
form.addEventListener('submit',function(e) {
    e.preventDefault();
    if(validate())
        $(this).unbind('submit').submit();
});