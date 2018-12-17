# [START speech_transcribe_streaming_mic]
from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from pykakasi import kakasi     #漢字をひらがなに変換モジュール

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

rate = ""
close = ""
num_chars_printed = 0
num_words_spoken = 0
warn = "" 
voice_paused_list = ["えーと", "えっとー", "えっと", "あのー","えっと ","あー","あの"]
def listen_print_loop(responses):
    spoken = []
    global num_chars_printed
    global num_words_spoken
    global rate
    global close
    global warn

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        #認識された文字列中の漢字をひらがなに変換　例: きょうはいいてんき
        kakasis = kakasi()
        kakasis.setMode("J","H")
        conv = kakasis.getConverter()
        kana_script = result.alternatives[0].transcript
        transcript = (conv.do(kana_script.replace("\u3000","")))

        overwrite_chars = ' ' * (num_chars_printed - len(transcript))
        word_list = list(transcript)

        if not result.is_final:
            num_words_spoken = len(transcript) + num_chars_printed
            #print(num_words_spoken)
            #sys.stdout.write(transcript + overwrite_chars + '\r')
            #sys.stdout.flush()
            last_word = [''.join(word_list[-4::]),''.join(word_list[-3::]), ''.join(word_list[-2::])] 
            if any(word in voice_paused_list for word in last_word):    
                warn = True

        else:
            spoken.append(transcript + overwrite_chars)
            final_spoken = ''.join(spoken) #喋った単語を全部ひらがなに変換
            print(final_spoken)    
            num_chars_printed = num_words_spoken
            if close:
                print(final_spoken)  
                print('Exiting..')

                break
            if re.search(r'\b(おわり|quit)\b', transcript, re.I):
                print("ended forcefully")
                break

def count_words():
    global num_words_spoken
    global num_chars_printed
    num_words_spoken = num_chars_printed + num_words_spoken

def set_warn():
    global warn
    warn = ""

def main():
    language_code = 'ja-JP'  

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
