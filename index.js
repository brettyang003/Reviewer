const GOOGLE_APPLICATION_CREDENTIALS = 'D:\Users\kevle\Downloads\true-ion-340503-3c72797fda35.json'
const speech = require('@google-cloud/speech');
const fs = require('fs');

async function main() {
    const client = new speech.SpeechClient();
    const filename = './resources/audio.raw';

    const file = fs.readFileSync(filename);
    const audioBytes = file.toString('base64');

    const audio = {
        content: audioBytes
    };
    const config = {
        encoding: 'LINEAR16',
        sampleRateHertz: 16000,
        langaugeCode: 'en-US'
    };

    const request = {
        audio: audio,
        config: config
    }

    const [response] = await client.recognize(request);
    const transcription = response.results.map(result =>
        result.alternatives[0].transcript).join('\n');
        console.log('Transcription: ${transcription}');
}

main().catch(console.error);