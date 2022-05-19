
        $('input[type=radio][name=deliveryOption]').on('change', function (e) {
            
            let subtotalprice = document.getElementById('subtotal').getAttribute('price')
            let deliveryprice = document.querySelector('input[name="deliveryOption"]:checked').value
            document.getElementById('deliveryprice').innerHTML = 'Rs ' + deliveryprice
            updatedvalue = Number(subtotalprice) + Number(deliveryprice)
            document.getElementById('totalprice').innerHTML = 'Rs ' + updatedvalue
        })