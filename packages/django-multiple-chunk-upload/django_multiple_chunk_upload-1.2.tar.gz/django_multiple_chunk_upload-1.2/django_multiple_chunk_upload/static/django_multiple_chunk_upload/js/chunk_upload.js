function atualizar_progress_bar(percentual) {
    element = document.getElementById('progress-bar')
    element.style.width = parseInt(percentual) + '%'
    element.innerHTML = parseInt(percentual) + '%'
}

function toggleButton(isActive) {
    const button = document.getElementById('upload-button');
    if (isActive) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
}
function slice_file(chunk, file, chunkSize){
    let start = chunkSize  * chunk
    let end = Math.min(start + chunkSize, file.size)
    let chunk_file = file.slice(start, end)
    return chunk_file
}

function complete_upload(non_input_files_ids, total_size, token_upload, url_complete_upload, url_redirect) {
    const non_inputs_files = non_input_files_ids.map(id => document.getElementById(id));
    const form_data_complete = new FormData();
    form_data_complete.append('total_size', total_size);
    form_data_complete.append('token_upload', token_upload)
    non_inputs_files.forEach(input => {
        form_data_complete.append(input.name, input.value)
    });

    fetch(url_complete_upload, {
        method: 'POST',
        body: form_data_complete
    })
        .then(response => response.json())
        .then(data => {
            if(url_redirect != null){
                window.location.href = url_redirect
            }   
            atualizar_progress_bar(100)
            document.getElementById('message-upload').innerHTML = "Formulário enviado com sucesso."
           
            toggleButton(true)
        })

}

function calculate_total_size(inputs) {
    let total_size = 0
    for (let i = 0; i < inputs.length; i++) {
        total_size += inputs[i].files[0].size
    }
    return total_size
}

function get_files_extensions(inputs_files) {
    const file_extensions = inputs_files.map(input => {
        if (input && input.files.length > 0) {
            return Array.from(input.files).map(file => file.name.split('.').pop());
        }
        return [];
    }).flat();

    return file_extensions
}


function send_file(input_files_ids, non_input_files_ids, url_upload, url_complete_upload, url_redirect) {
    toggleButton(false)
    atualizar_progress_bar(1)  
    const chunkSize = 1024 * 1024 // 1mb
    const inputs_files = input_files_ids.map(id => document.getElementById(id));
    const all_files_upload = inputs_files.every(input => input.files && input.files.length > 0);

    if (!all_files_upload) {
        document.getElementById('message-upload').innerHTML = "Envie todos os arquivos"
        toggleButton(true)
        return null
    }

    let total_size = calculate_total_size(inputs_files)
    const file_extensions = get_files_extensions(inputs_files)
    
    let total_chunks_files = []
    // [2, 3]

    for (let i = 0; i < inputs_files.length; i++) {
        total_chunks_files.push(Math.ceil(inputs_files[i].files[0].size / chunkSize))

    }

    let total_chunks = Math.max(...total_chunks_files) // 3

    let token_upload = null
    let current_chunk = 0

    function upload_file(chunk) {

        // Adiciona um campo no formulário com o ID do input file com o valor sendo um pedaço dos bytes do arquivo ao respectivo Chunk
        const form_data = new FormData();
        for (let i = 0; i < inputs_files.length; i++) {
            if (chunk > total_chunks_files[i]) {
                form_data.append(inputs_files[i].id, null);
            } else {
                if (chunk + 1 == total_chunks_files[i]) {
                    console.log('última chunk de ' + inputs_files[i].id)
                    // Enviar como a last chunk para realizar a hash
                }
                form_data.append(inputs_files[i].id, slice_file(chunk, inputs_files[i].files[0], chunkSize))
            }
        }

        if (token_upload) {
            form_data.append('token_upload', token_upload)
        } else {
            form_data.append('file_extensions', JSON.stringify(file_extensions));
        }

        fetch(url_upload, {
            method: 'POST',
            body: form_data
        })
            .then(response => {
                if (!response.ok) {
                    throw response;
                }
                return response.json()
            })
            .then(data => {

                if (!token_upload) {
                    token_upload = data.token_upload
                }

                current_chunk++;

                atualizar_progress_bar((current_chunk * 100) / total_chunks)
                if (current_chunk < total_chunks) {
                    upload_file(current_chunk)
                }

                if (current_chunk == total_chunks) {
                    complete_upload(non_input_files_ids, total_size, token_upload, url_complete_upload, url_redirect)
                }

            })
            .catch(error => {
                const status = error.status
                switch (status) {
                    case 400:
                        document.getElementById('message-upload').innerHTML = "Ocorreu um erro em seu Upload, tente novamente."
                        toggleButton(true)
                        return null
                    case 413:
                        document.getElementById('message-upload').innerHTML = "Os arquivos são grandes demais."
                        toggleButton(true)
                        return null
                    case 408:
                        document.getElementById('message-upload').innerHTML = "Tempo de upload expirado, envie o formulário novamente"
                        toggleButton(true)
                        return null
                    case 422:
                        document.getElementById('message-upload').innerHTML = "Erro com a compatibilidade dos arquivos"
                        toggleButton(true)
                        return null
                    default:
                        setTimeout(() => upload_file(current_chunk), 3000);
                }

            });


    }
    upload_file(0)

}