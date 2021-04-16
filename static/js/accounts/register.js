const usernameEl = document.querySelector('#id_username');
const emailEl = document.querySelector('#id_email');
const first_nameEl = document.querySelector('#id_first_name');
const last_nameEl = document.querySelector('#id_last_name');
const passwordEl = document.querySelector('#id_password1');
const confirmPasswordEl = document.querySelector('#id_password2');
const form = document.querySelector('#sign_up');


const checkUsername = () => {
    let valid = false;

    const min = 3,
        max = 25;

    const username = usernameEl.value.trim();

    if (!isRequired(username)) {
        showError(usernameEl, 'Username cannot be blank.');
    } else if (!isBetween(username.length, min, max)) {
        showError(usernameEl, `Username must be between ${min} and ${max} characters.`)
    }else if(!isUserNameValid(username)){
        showError(usernameEl, 'Username must contain letters, numbers and some special character _')
    } else {
        showSuccess(usernameEl);
        valid = true;
    }
    return valid;
};


const checkEmail = () => {
    let valid = false;
    const email = emailEl.value.trim();
    if (!isRequired(email)) {
        showError(emailEl, 'Email cannot be blank.');
    } else if (!isEmailValid(email)) {
        showError(emailEl, 'Email is not valid.')
    } else {
        showSuccess(emailEl);
        valid = true;
    }
    return valid;
};

const checkName = (str) => {
    let valid = false;

    let min, max = 25, elem, name, field_name;
    if(str === 'first') {
        name = first_nameEl.value.trim();
        field_name = 'First name';
        elem = first_nameEl;
        min = 3;
    }
    else if(str === 'last') {
        name = last_nameEl.value.trim();
        field_name = 'Last name';
        elem = last_nameEl;
        min = 5;
    }

    if (!isRequired(name)) {
        showError(elem, `${field_name} cannot be blank.`);
    } else if (!isBetween(name.length, min, max)) {
        showError(elem, `${field_name} must be between ${min} and ${max} characters.`)
    } else if (!isNameValid(name)) {
        showError(elem, `${field_name} must contain only letters.`);
    }  else {
        showSuccess(elem);
        valid = true;
    }
    return valid;
};

const checkPassword = () => {
    let valid = false;
    const password = passwordEl.value.trim();

    if (!isRequired(password)) {
        showError(passwordEl, 'Password cannot be blank.');
    } else if (!isPasswordSecure(password)) {
        showError(passwordEl, 'Password must has at least 8 characters that include at least 1 lowercase character, 1 number');
    } else {
        showSuccess(passwordEl);
        valid = true;
    }

    return valid;
};

const checkConfirmPassword = () => {
    let valid = false;
    // check confirm password
    const confirmPassword = confirmPasswordEl.value.trim();
    const password = passwordEl.value.trim();

    if (!isRequired(confirmPassword)) {
        showError(confirmPasswordEl, 'Please enter the password again');
    } else if (password !== confirmPassword) {
        showError(confirmPasswordEl, 'The password does not match');
    } else {
        showSuccess(confirmPasswordEl);
        valid = true;
    }

    return valid;
};

const isUserNameValid = (username) => {
    //const re = /^[a-zA-Z0-9_./-]+$/;
    const re =/^[a-zA-Z0-9_]{2,}[a-zA-Z]+[0-9]*$/;
    return re.test(username);
}

const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};

const isNameValid = (name) => {
    const re = /^[a-zA-Z]+$/;
    return re.test(name);
};

const isPasswordSecure = (password) => {
    const re1 = /^[a-zA-Z0-9_./-]+$/
    const re2 = new RegExp("^(?=.*[a-z])(?=.*[0-9])(?=.{8,})");
    return re2.test(password) && re1.test(password);
};

const isRequired = value => value === '' ? false : true;
const isBetween = (length, min, max) => length < min || length > max ? false : true;


const showError = (input, message) => {
    const formField = input.parentElement;
    formField.classList.remove('success');
    formField.classList.add('error');

    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
    const formField = input.parentElement;
    formField.classList.remove('error');
    formField.classList.add('success');

    const error = formField.querySelector('small');
    error.textContent = '';
}


form.addEventListener('submit', function (e) {
    e.preventDefault();

    let isUsernameValid = checkUsername(),
        isEmailValid = checkEmail(),
        isFirstNameValid = checkName('first'),
        isLastNameValid = checkName('last'),
        isPasswordValid = checkPassword(),
        isConfirmPasswordValid = checkConfirmPassword();

    let isFormValid = isUsernameValid &&
        isEmailValid &&
        isFirstNameValid &&
        isLastNameValid &&
        isPasswordValid &&
        isConfirmPasswordValid;

    // submit to the server if the form is valid
    if (isFormValid) {
        $(this).off('submit').submit();
    }
});


const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        // cancel the previous timer
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        // setup a new timer
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};

form.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'id_username':
            checkUsername();
            break;
        case 'id_email':
            checkEmail();
            break;
        case 'id_first_name':
            checkName('first');
            break;
        case 'id_last_name':
            checkName('last');
            break;
        case 'id_password1':
            checkPassword();
            if(confirmPasswordEl.value !== "")
                checkConfirmPassword();
            break;
        case 'id_password2':
            checkConfirmPassword();
            break;
    }
}));