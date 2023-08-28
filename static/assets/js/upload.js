const uploadForm = document.getElementById('uploadForm')
const inputFile = document.getElementById('formFile')

const progressBox = document.getElementById('progressBox')
const cancelBox = document.getElementById('cancelBox')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

inputFile.addEventListener('change', () => {
    progressBox.classList.remove('invisible')
    cancelBox.classList.remove('invisible')

    const file_data = inputFile.files[0]
    console.log(file_data)

    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('spreadsheet', file_data)

    $.ajax({
        type:'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: formData,
        beforeSend: function(){

        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100
                    console.log(e)
                    progressBox.innerHTML=`<div id="progress" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100" style="width: ${percent}"></div>`
                }
            })
            return xhr
        },
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})