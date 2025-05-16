const constraints = {
 "video": true
};

navigator.mediaDevices.getUserMedia(constraints).then(gotMedia).catch(error => console.error('getUserMedia() error:', error));

function gotMedia(mediaStream) {
  const mediaStreamTrack = mediaStream.getVideoTracks()[0];
  const imageCapture = new ImageCapture(mediaStreamTrack);
  //console.log(imageCapture);

  var ready_to_send = true
  var count = 0
  function capture() {
    imageCapture.takePhoto().then(blob => {
    img = document.getElementById("img")
    img.src = URL.createObjectURL(blob);
    $("#counter").html(count)
    count ++

    if(ready_to_send) {
            ready_to_send = false
            var fd = new FormData();
            fd.append('file', blob, 'screenshot.png');
            $.ajax({
                type: 'POST',
                url: 'https://europe-west8-pcloud2025.cloudfunctions.net/main_describe_photo',
                data: fd,
                processData: false,
                contentType: false,
            }).done(function(data) {
                data = JSON.parse(data)
                $('#txt').html('ok')
                var audio = new Audio();
                audio.src = audio.src = "data:audio/mp3;base64," + data.audio_base64
                audio.play()
                audio.addEventListener("ended", function(){
                    myAudio.currentTime = 0;
                    console.log("ended");
                    ready_to_send = true
                });
                img.onload = () => { URL.revokeObjectURL(this.src); }
            });
        }

      }).catch(error => console.error('takePhoto() error:', error));
      window.setTimeout(capture,50)
  }
  capture()
}