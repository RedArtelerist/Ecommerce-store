var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        console.log('Click')
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        updateCartItem(productId, action)
    })
}

function updateCartItem(productId, action){
    var url = '/cart_update/'
    console.log(csrftoken)
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applications/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    });
}