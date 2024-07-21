from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin
import urllib.parse as urlparse
import re
import logging

app = Flask(__name__)
CORS(app)

# Load pre-trained T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

@app.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        # Get the video URL from the request body
        data = request.get_json()
        video_url = data.get('videoUrl')

        # Parse the URL and extract video ID
        url_data = urlparse.urlparse(video_url)
        if re.search(r'youtu\.be', url_data.netloc):
            # Shortened URL
            video_id = url_data.path.split('/')[1]
        else:
            # Standard URL
            video_id = urlparse.parse_qs(url_data.query)['v'][0]

        # Fetch the transcript of the YouTube video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        if not transcript:
            return jsonify({'error': 'Unable to fetch transcripts'})

        # Extract text from transcript
        transcript_text = ' '.join([line['text'] for line in transcript])

        # Tokenize the input text
        input_ids = tokenizer.encode(transcript_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate summary
        summary_ids = model.generate(input_ids, num_beams=4, length_penalty=2.0, max_length=150, early_stopping=True)

        # Decode the summary
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Return the summary as a JSON response
        return jsonify({'summary': summary_text})

    except Exception as e:
        # Handle any errors
        error_message = str(e)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)