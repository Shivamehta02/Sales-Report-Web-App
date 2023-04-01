const reportBtn = document.getElementById('report-Btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box') 

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrf= document.getElementsByName('csrfmiddlewaretoken')[0].value

const handleAlrts = (type,msg)=>{
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>`
}

if (img){
    reportBtn.classList.remove('not-visible')   //for removing the not-visible class 
}


reportBtn.addEventListener('click',()=>{  //to add chart in model we created
    console.log('clicked')
    img.setAttribute('class','w-100')
    modalBody.prepend(img)

    console.log(img.src)
    
    reportForm.addEventListener('submit', e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({

            type:'POST',
            url:'/reports/save/',
            data: formData,
            success: function(response){
                handleAlrts('success','report ceated')
            },
            error: function (error) {
                handleAlrts('danger','ooops! something went wrong ')
            },

            processData: false,
            contentType: false,
    
        })

    })
})

