from flask import Flask, render_template, request, jsonify
import assemblyai as aai

app = Flask(__name__)

# Replace with your AssemblyAI API key
aai.settings.api_key = "6330aaa0be3f4007a286ec393dfc7f7c"

@app.route('/')
def index():
    return render_template('speaker.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the file temporarily
        audio_path = 'user_audio.wav'
        file.save(audio_path)

        # Perform transcription
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path, config=config)

        # Prepare response data
        output = [{'speaker': utterance.speaker, 'text': utterance.text} for utterance in transcript.utterances]

        return jsonify({'transcript': output})

if __name__ == '__main__':
    app.run(debug=True)
