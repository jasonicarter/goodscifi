function upload(formData) {
    const photos = formData.getAll('photos');
    const promises = photos.map((x) => getImage(x)
        .then(img => ({
            id: img,
            fileName: x.name,
            predictions: { good: 0.90, not_good: 0.10 },
            url: img
        })));
    return Promise.all(promises);
}

// https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
function getImage(file) {
    return new Promise((resolve, reject) => {
        const fReader = new FileReader();
        const img = document.createElement('img');

        fReader.onload = () => {
            img.src = fReader.result;
            var json_data = {data: JSON.stringify(fReader.result)};
            // console.log(json_data['data'])
            // resolve(getBase64Image(img));
            resolve(img.src);

        }

        fReader.readAsDataURL(file);
    })
}

function getBase64Image(img) {
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);

    const dataURL = canvas.toDataURL('image/png');

    return dataURL;
}

export { upload }
