$(document).ready(() => {
  Webcam.set({
    width: 320,
    height: 240,
    dest_width: 720,
    dest_height: 576,
    image_format: 'jpeg',
    jpeg_quality: 100,
  });

  Webcam.set('constraints', { facingMode: 'environment' });
  Webcam.attach('#video');

  setInterval(() => {
    let base64Img;

    Webcam.snap(function (data_uri) {
      base64Img = data_uri;
    });

    $.ajax({
      url: 'http://localhost:5000/image',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      success: (response) => $('#plate').text(response),
      data: JSON.stringify(base64Img),
    });
  }, 5000);
});
