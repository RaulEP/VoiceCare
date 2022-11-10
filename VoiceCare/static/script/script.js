var gumStream;
var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext

var recordButton = document.getElementById("voice");
var stopButton = document.getElementById("stopRecord");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
    console.log("record button clicked");

    var constraints = { audio: true }

    recordButton.disabled = true;
    // recordButton
    stopButton.disabled = false;

    navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
        audioContext = new AudioContext();

        gumStream = stream;

        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input, {numChannels:1})

        rec.record()

        console.log("Recording");

    }).catch(function(err) {
        recordButton.disabled = false;
        stopButton.disabled = true;
    });
}

function stopRecording() {
    console.log("stopRecording clicked");

    stopButton.disabled = true;
    recordButton.disabled = false;

    rec.stop();

    gumStream.getAudioTracks()[0].stop();

    rec.exportWAV(sendBlobToServer);
}

function sendBlobToServer(blob) {
    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    
    au.controls = true;
    au.src = url;

    li.appendChild(au);

    // recordingsList.appendChild(li);
    const msgChat = get('.msger-chat');
    msgChat.appendChild(li);
    msgChat.scrollTop += 500;

    let formData = new FormData();
    formData.append('file', blob);

    fetch('/voice', {
        method: 'POST',
        body: formData
    })
}