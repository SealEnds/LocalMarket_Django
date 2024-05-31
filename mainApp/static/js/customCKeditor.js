// import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
// import Base64UploadAdapter from '@ckeditor/ckeditor5-upload/src/adapters/base64uploadadapter';

document.addEventListener('DOMContentLoaded', function () {
    ClassicEditor
        .create(document.querySelector('#id_content'), {
            // plugins: [Base64UploadAdapter, /* ... */ ],
            // Editor configuration.
        })
        .then(editor => {
            window.editor = editor;
        })
        .catch(error => {
            console.error(error);
        });
});