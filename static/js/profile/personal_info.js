$(document).ready(function() {
    $('#id_city').select2();
});

function readURL(input) {
    console.log('load');
    if (input.files && input.files[0]) {
        console.log(input.files);
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#imagePreview").css(
                "background-image",
                "url(" + e.target.result + ")"
            );
            $("#imagePreview").hide();
            $("#imagePreview").fadeIn(650);
        };
        reader.readAsDataURL(input.files[0]);
    }
    else {
        $("#imagePreview").css(
            "background-image",
            "url(/images/" + userImage + ")"
        );
        $("#imagePreview").hide();
        $("#imagePreview").fadeIn(650);
    }
}
$("#imageUpload").change(function () {
    readURL(this);
});

const form = document.getElementById('profileForm');
const first_name = document.getElementById('id_first_name');
const last_name = document.getElementById('id_last_name');
const middle_name = document.getElementById('id_middle_name');
const phone = document.getElementById('id_phone');
const city = document.getElementById('id_city');
const birthdate = document.getElementById('id_birthdate');
const submit = document.getElementById('submit-btn');

// mask for mobile phone
$(window).load(function() {
    var phones = [{ "mask": "+38(###) ###-##-##"}];
    $('#id_phone').inputmask({
        mask: phones,
        greedy: false,
        definitions: { '#': { validator: "[0-9]", cardinality: 1}} });
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


function checkPhone(input) {
    if(input.value === "") {
        input.parentElement.classList.remove("error");
        return true;
    }
    const re = /^[+]?[\s./0-9]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]{9,14}$/g;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    }else {
        showError(input,'Mobile phone is not invalid');
    }
}

function checkName(input) {
    if(input.value === "") {
        input.parentElement.classList.remove("error");
        return true;
    }
    const re = /^[a-zA-Z]+$/;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    }else {
        showError(input,`${input.dataset.name} must contains only letters`);
    }
}

function checkDate(input){
    console.log(input.value.trim());
    if(input.value === "") {
        input.parentElement.classList.remove("error");
        return true;
    }
    var parts = input.value.split("-");
    if(parts[0] >= 1930 && parts[0] <= 2020){
        showSucces(input);
        return true;
    }else {
        showError(input,"birthdate is incorrect");
    }
}


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
    if(!checkLength(input, 3, 10))
        return false;
    else
        return checkName(input);
}

function validate(){
    let a = validateName(first_name);
    let b = validateName(last_name);
    var e = checkName(middle_name);
    var c = checkPhone(phone);
    var d = checkDate(birthdate);

    return a && b && c && d && e;
}


//Event Listeners
form.addEventListener('submit',function(e) {
    e.preventDefault();
    if(validate()){
        $(this).unbind('submit').submit();
    }
});