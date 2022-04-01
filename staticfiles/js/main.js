/*------------------------------------
JQUERY PAGE LOADING
------------------------------------ */
(function($) {
    "use strict";

    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: ['animation-duration', '-webkit-animation-duration'],
        overlay: false,
        overlayClass: 'animsition-overlay-slide',
        overlayParentElement: 'html',
        transition: function(url) {
            window.location.href = url;
        }
    });


})(jQuery);


/*--------------------
CSRF_TOKEN
----------------------*/

const getToken =(name) =>{
    var cookieValue = null;
    if(document.cookie && document.cookie !==''){
        var cookies = document.cookie.split(';');
        for(var i=0; i< cookies.length; i++){
            var cookie = cookies[i].trim();
            if(cookie.substring(0,name.length + 1)===(name+'='))
                {
                cookieValue = decodeURIComponent(cookie.substring(
                name.length +=1));
                break;
                }
            }
        }
        return cookieValue;
    }
let csrftoken =getToken('csrftoken');

    //Function Prototype    
    const sendSearchData = (keyword) => {
        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                'csrfmiddlewaretoken': csrftoken,  //const csrf_token ==...
                'keyword': keyword,
            },
            beforeSend:function(){
                //user can't click the button by the time
                $("#loading").addClass('spinner-border');
                $("#spinner").addClass('visually-hidden');
			},
            success: function (response) {
                console.log(response)
                const data = response.queryset
                if (Array.isArray(data)) {

                    searchquery.innerHTML = " "  //start with empty
                    data.forEach(keyword => {
                        searchquery.innerHTML +=
                            `<li class="mb-2 search-obj pt-3 pb-3 px-4"><a class="text-black" href="${keyword.url}" style="text-decoration:none;"><b>${keyword.title}</b></a></li> `
                    })
                } else {
                    if (searchinput.value.length > 0) {
                        searchquery.innerHTML = `<p  class="text-black pt-3 pb-3 px-4">${data}</p> `
                    } else {
                        searchquery.classList.add("invisible");
                    }
                }
            },
            error: function (error) {
                console.log(error.data)
            }
           

        })
    }


    const searchform = document.getElementById("search-form")
    const searchinput = document.getElementById("search-input")
    const searchquery = document.getElementById("search-query")

    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    console.log(csrf_token)
    searchinput.addEventListener("keyup", e => {
        console.log("printing", e.target.value)
        if (searchquery.classList.contains('invisible')) {
            searchquery.classList.remove('invisible')
        }
        sendSearchData(e.target.value);
    })

/*--------------------
NUM INCR/DECR
----------------------*/
const minValue = 0
const maxValue = 10
const inputField = document.getElementById("product-quantity")
const incrementBtn = document.getElementsByClassName("btn-num-product-up")
const decrementBtn = document.getElementsByClassName("btn-num-product-down")
for (let i = minValue; i < incrementBtn.length; i++) {
    let thisButton = incrementBtn[i];
    console.log(thisButton)
    thisButton.onclick = (event) => {
        let buttonClicked = event.target;
        console.log(buttonClicked)
        console.log(buttonClicked.parentElement)
        let input1 = buttonClicked.parentElement.children[1];
        console.log(input1)

        let inputValue = input1.value;

        let newValue = parseInt(inputValue) + 1;
        console.log(newValue)
        if (newValue <= maxValue) {
            input1.setAttribute('value', newValue);
        }
    }
}

for (let i = minValue; i < decrementBtn.length; i++) {
    let thisButton = decrementBtn[i];
    console.log(thisButton)
    thisButton.onclick = (event) => {
        let buttonClicked = event.target;
        console.log(buttonClicked)
        let input1 = buttonClicked.parentElement.children[1];

        let inputValue = input1.value;

        let newValue = parseInt(inputValue) - 1;
        console.log(newValue)
        if (newValue > minValue) {
            input1.setAttribute('value', newValue);
        } else {
            input1.setAttribute('value', 0);
        }

    }
}




    
/*--------------------
PRODUCT DETAIL VIEW
----------------------*/
const modalDetailContainer = document.getElementById('modal-detail-container')
const modalBtns = [ ...document.getElementsByClassName('product-modal-btn')] //Array
const imgGalleryDiv = document.getElementById('img-gallery')
const wrapSlickDiv = document.getElementById('featured')
const prodcut_title =document.getElementById('product-title')

modalBtns.forEach((modalELement) => modalELement.addEventListener('click',()=>{
    const prod_code = modalELement.getAttribute('prod-code')
    const prod_id = modalELement.getAttribute('prod-id')
        
    const url="product_json_view/";
    const data= {
        "prod_id":prod_id,
        "prod_code":prod_code} 
    fetch(url,{
            method:'post',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify(data)//We dont need to stringify when data is a string.

        },)
    .then((response)=>{
        return response.json(); 
    })

    //success
    .then((elem)=>{
        imageArray=elem['images']
        wrapSlickDiv.setAttribute('src',String(elem['thumbnail']))
        console.log('ImageArrayLength:',imageArray.length)
        if (imageArray.length != 0){
            imageArray.forEach((image)=>{
                console.log("yes")
                imgGalleryDiv.innerHTML +=`
                            <img class="thumbnail" src="${image['image']}" alt="IMG-PRODUCT">
                `
            })
        }else {
            imgGalleryDiv.innerHTML +=`
                            <img class="thumbnail" src="${String(elem['thumbnail'])}" alt="IMG-PRODUCT">
                `
        }

        const productAddBtn = document.getElementById("product-add-btn")
        productAddBtn.setAttribute('prod-code', prod_code)
        productAddBtn.setAttribute('prod-id', prod_id)

        const prodcut_title =document.getElementById('product-title')
        prodcut_title.innerHTML = elem.name
        const prodcut_price =document.getElementById('product-price')
        prodcut_price.innerHTML = '$'+ elem.price
        const product_description =document.getElementById('product-description')
        product_description.innerHTML = elem.description  

       //Dump Image Album
        let thumbnails = document.getElementsByClassName('thumbnail')
        let activeImages = document.getElementsByClassName('active')

        for (var i = 0; i < thumbnails.length; i++) {
            thumbnails[i].addEventListener('click', function () {
                console.log(activeImages)

                if (activeImages.length > 0) {
                    activeImages[0].classList.remove('active')
                }
                this.classList.add('active')
                document.getElementById('featured').src = this.src
            })
        }

        //Image Slider and Controller
        let buttonRight = document.getElementById('slideRight');
        let buttonLeft = document.getElementById('slideLeft');
        buttonLeft.addEventListener('click', function () {
            document.getElementById('img-gallery').scrollLeft -= 180
        })

        buttonRight.addEventListener('click', function () {
            document.getElementById('img-gallery').scrollLeft += 180
        })

        //Reset Gallery on Close Button Click 
        const close_button = document.getElementById("btn-close")
        close_button.addEventListener('click', ()=>{
            imgGalleryDiv.innerHTML=''
        })
    })


}) );
    
    
    
/*---------------------------------
ADD/UPDATE PRODUCT IN MODAL FORM 
----------------------------------*/
const productAddBtn = document.getElementById("product-add-btn")
productAddBtn.addEventListener("click", (e)=>{
    outputhtml = ''
    e.preventDefault()
    prod_id = productAddBtn.getAttribute('prod-id')
    prod_code =productAddBtn.getAttribute('prod-code')

    const productQuantity = document.getElementById("product-quantity")
    let prod_quantity = productQuantity.getAttribute('value')
    const url='add/'
    const data= {
        "prod_id":prod_id,
        "prod_code":prod_code,
        "prod_quantity":prod_quantity
    } 
    console.log("data:", data)
  fetch(url,{
      method: 'post',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken,
      },
      body:JSON.stringify(data)

  })
  .then((response)=>{
      return response.json();
  })
  .then((response)=>{
    let elements = response.products
    console.log(elements)
    let cartDiv = document.getElementsByClassName("your-cart")
    for (let i =0; i<cartDiv.length;i++){
        cartDiv[i].setAttribute('data-notify',response.basketqty)
    }
    const headerCartTotal = document.getElementById('header-cart-total')
    headerCartTotal.innerHTML="Total: $"+response.basketsubtotal
    
    const headerCart = document.getElementById('header-cart')
    let outputhtml =''
    elements.forEach((elem) => {
        console.log('elem',':',elem)
        outputhtml += `
        <li id="cart-${elem['prod-id']}" class="header-cart-item flex-w flex-t m-b-12">
            <div class="header-cart-item-img">
                <img src="${elem['thumbnail']}" alt="IMG">
            </div>

            <div class="header-cart-item-txt p-t-8">
                <a href="#" class="header-cart-item-name m-b-18 hov-cl1 trans-04">
                ${elem['title']}
                </a>

                <span class="header-cart-item-info">
                ${elem['qty']} x ${elem['price']}
                </span>
            </div>
        </li>
    `
    });
    headerCart.innerHTML = outputhtml
    

  })
})
