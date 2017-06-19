console.log("js code");

$('#cropEndBtn').on('click',function(){
    console.log("hello");
    var imageData = $image.cropper('getData');
    console.log(imageData);
    /* 结果如下 Object {x: 212.36363636363637, y: 76, width: 338.90909090909093, height: 256.3636363636364} */
});

// window.addEventListener('DOMContentLoaded', function () {
//       var image = document.querySelector('#eyeImage');
//       var cropper = new Cropper(image, {
//         movable: false,
//         zoomable: false,
//         rotatable: false,
//         scalable: false,
//         autoCropArea:0.5,
//         minCropBoxWidth:100,
//         minCropBoxHeight:100,
//         crop: function (e) {
//             var cropper = this.cropper;
//             var imageData = cropper.getData();
//             //console.log(imageData);
//             document.getElementById("x_value").value = imageData.x;
//             document.getElementById("y_value").value = imageData.y;
//             document.getElementById("width_value").value = imageData.width;
//             document.getElementById("height_value").value = imageData.height;
//         }
//       });
//     });