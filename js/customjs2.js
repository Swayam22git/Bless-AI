
let mediaRecorder;
let audioChunks = [];

const startRecordingButton = document.getElementById("startRecording");
const stopRecordingButton = document.getElementById("stopRecording");
const uploadAudioButton = document.getElementById("uploadAudio");
const audioPlayer = document.getElementById("audioPlayer");
const Blessitext = document.getElementById("Blessitext");

startRecordingButton.addEventListener("click", startRecording);
stopRecordingButton.addEventListener("click", stopRecording);
uploadAudioButton.addEventListener("click", uploadAudio);

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: { sampleRate: 16000 } });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = function (event) {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = function () {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;
            stopRecordingButton.style.display = "none";
            uploadAudioButton.click()
        };

        mediaRecorder.start();
        startRecordingButton.style.display = "none";
        stopRecordingButton.style.display = "block";
    } catch (error) {
        console.error("Error accessing microphone:", error);
    }
}

function stopRecording() {
    mediaRecorder.stop();
}

async function uploadAudio() {
    if (audioChunks.length === 0) {
        alert("No audio to upload. Please record some audio first.");
        return;
    }

    const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
    const formData = new FormData();
    formData.append('file', audioBlob, 'recorded_audio.mp3');

    const response = await fetch(`https://blessi-api.allserieshub.fun/audio/Bless_audio_input`, {
        method: 'POST',
        body: formData,
    });

    const responses = await fetch(`https://blessi-api.allserieshub.fun/audio/Bless_audio_output`, {
        method: 'GET'
    });

    const blob = await responses.blob();
    const url = URL.createObjectURL(blob);
    audioPlayer.style.display = "block";
    audioPlayer.src = url; 
    audioPlayer.play();
    Blessitext.style.display = "block";


    // Add an event listener to refresh the page when the audio has ended
    audioPlayer.onended = function () {
        location.reload();
    };
    startRecordingButton.style.display = "none";
    stopRecordingButton.style.display = "none";
    audioPlayer.style.display = "none";
    uploadAudioButton.style.display = "none";

}