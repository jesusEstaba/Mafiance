const imagePreview = document.getElementById('img-preview');
const imageUploader = document.getElementById('img-uploader');
const imageUploadbar = document.getElementById('img-upload-bar');

var cl = new cloudinary.Cloudinary({ cloud_name: "dpwaxzhnx", secure: true });
const CLOUDINARY_URL = "https://686827445281429:BEP9W9XdP_emQJb8PL7fhqP8czc@dpwaxzhnx";
const CLOUDINARY_UPLOAD_PRESET = 'tkxeggub';

imageUploader.addEventListener('change', async (e) => {
    // console.log(e);
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

    // Usamos axios.post para acceder al cloudinary remplazando la función fetch para usar la api.
    const res = await axios.post(
        CLOUDINARY_URL,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            },

            // Función de axios para controlar el progreso de las barras de carga con onUploadProgress(e) AKA evento
            //verificar documentación.

            onUploadProgress(e) {
                let progress = Math.round((e.loaded * 100.0) / e.total); //Math.round es para redondear valores numéricos en consola
                console.log(progress);                                   // Así podremos ver cuando cargue la imagen con números menos extensos
                imageUploadbar.setAttribute('value', progress);
            }
        }
    );
    console.log(res);
    imagePreview.src = res.data.secure_url;
});