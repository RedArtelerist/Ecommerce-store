var username = document.getElementById('id_username');
const form = document.getElementById('changeUsername');

function showError(input, message) {
    let formControl = input.parentElement;

    if(formControl.className.includes("col-md-6"))
        formControl.className = "col-md-6 mb-3 order-form-control error";
    else
        formControl.className = "mb-3 order-form-control error";

    const small = formControl.querySelector('small');
    small.innerText = message;
}

function showSucces(input) {
    let formControl = input.parentElement;
    if(formControl.className.includes("col-md-6"))
        formControl.className = "col-md-6 mb-3 order-form-control success";
    else
        formControl.className = "mb-3 order-form-control success";
}

function checkUsername(input) {
    //const re = /^[a-zA-Z0-9_./-]+$/;
    // (/^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i)
    const re =/^[a-zA-Z0-9_]{5,}[a-zA-Z]+[0-9]*$/;
    if(re.test(input.value.trim())) {
        showSucces(input);
        return true;
    } else {
        showError(input,'Username must contains only letters, numbers and some character _');
    }
}


function checkLength(input, min ,max) {
    if(input.value.length < min) {
        showError(input, `Username must be at least ${min} characters`);
    }else if(input.value.length > max) {
        showError(input, `Username must be les than ${max} characters`);
    }else {
        showSucces(input);
        return true;
    }
}

function validate(){
    var a = checkLength(username, 3,20);
    if(!a) return false;
    var b = checkUsername(username);
    return a && b
}


//Event Listeners
form.addEventListener('submit',function(e) {
    e.preventDefault();
    if(validate()){
        $(this).unbind('submit').submit();
    }
});