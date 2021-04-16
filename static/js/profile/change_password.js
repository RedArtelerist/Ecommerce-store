const new_password1 = document.querySelector('#id_new_password1');
const new_password2 = document.querySelector('#id_new_password2');
const form = document.querySelector('#changePasswordForm');

const checkPassword = () => {
    let valid = false;
    const password = new_password1.value.trim();

    if (!isRequired(password)) {
        showError(new_password1, 'Password cannot be blank.');
    } else if (!isPasswordSecure(password)) {
        showError(new_password1, 'Password must has at least 8 characters that include at least 1 lowercase character, 1 number');
    } else {
        showSuccess(new_password1);
        valid = true;
    }

    return valid;
};

const checkConfirmPassword = () => {
    let valid = false;

    const confirmPassword = new_password2.value.trim();
    const password = new_password1.value.trim();

    if (!isRequired(confirmPassword)) {
        showError(new_password2, 'Please enter the password again');
    } else if (password !== confirmPassword) {
        showError(new_password2, 'The password does not match');
    } else {
        showSuccess(new_password2);
        valid = true;
    }

    return valid;
};

const isPasswordSecure = (password) => {
    const re1 = /^[a-zA-Z0-9_./-]+$/
    const re2 = new RegExp("^(?=.*[a-z])(?=.*[0-9])(?=.{8,})");
    return re2.test(password) && re1.test(password);
};

const isRequired = value => value === '' ? false : true;


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

    let isPasswordValid = checkPassword(),
        isConfirmPasswordValid = checkConfirmPassword();

    let isFormValid = isPasswordValid &&  isConfirmPasswordValid;

    if (isFormValid) {
        $(this).unbind('submit').submit();
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
        case 'id_new_password1':
            checkPassword();
            if(new_password2.value !== "")
                checkConfirmPassword();
            break;
        case 'id_new_password2':
            checkConfirmPassword();
            break;
    }
}));