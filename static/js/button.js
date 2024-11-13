// Change button to loading mode
function setLoadingButtonMode(button) {
    button.classList.remove('btn-success', 'btn-danger');
    button.classList.add('btn-primary');
    button.disabled = true;
    button.querySelector('span').classList.remove('hidden');
}

// Revert button to success mode
function setSuccessButtonMode(button) {
    button.classList.remove('btn-primary', 'btn-danger');
    button.classList.add('btn-success');
    button.disabled = false;
    button.querySelector('span').classList.add('hidden');
}

// Revert button to normal mode
function setNormalButtonMode(button) {
    button.classList.remove('btn-danger', 'btn-success');
    button.classList.add('btn-primary');
    button.disabled = false;
    button.querySelector('span').classList.add('hidden');
}

// Revert button to error mode
function setErrorButtonMode(button) {
    button.classList.remove('btn-primary', 'btn-success');
    button.classList.add('btn-danger');
    button.disabled = false;
    button.querySelector('span').classList.add('hidden');
}
