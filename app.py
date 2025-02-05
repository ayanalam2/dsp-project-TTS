#LIBRARIES USEDC
import streamlit as st
from pydub import AudioSegment, effects
from pydub.silence import detect_nonsilent
import os

AUDIO_DIR = 'C:\\Users\\Abdul\\Desktop\\lab8\\wavs'

# Function to remove silence from audio TO MAKE OUR OUPUT CLEAN AND HEARABLE
def remove_silence(audio, silence_thresh=-40):
    non_silent_ranges = detect_nonsilent(audio, min_silence_len=400, silence_thresh=silence_thresh)
    if non_silent_ranges:
        start, end = non_silent_ranges[0][0], non_silent_ranges[-1][1]
        return audio[start:end]
    return audio  # Return original if no silence detected

# Function to apply a robotic AI effect with smoothne 
def apply_robotic_effect(audio):
    echo = audio - 10  # Reduce volume for echo
    delayed_echo = echo.overlay(audio, position=70)  # Overlay with slight delay
    smoothed_audio = effects.normalize(delayed_echo)  # Normalize for smooth volume
    return smoothed_audio

# Function to handle sentence-based audio with a 0.5-second gap
def text_to_audio_custom(text):
    final_audio = AudioSegment.silent(duration=300)  # Start with a short silence buffer
    sentences = text.lower().split('.')  # Split text into sentences

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        audio_path = os.path.join(AUDIO_DIR, f"{sentence}.wav")
        if os.path.exists(audio_path):
            word_audio = AudioSegment.from_wav(audio_path)
            word_audio = remove_silence(word_audio)  # Trim silence
            word_audio = apply_robotic_effect(word_audio)  # Apply AI voice effect

            final_audio += word_audio.fade_in(100).fade_out(100)  # Smooth transitions
            final_audio += AudioSegment.silent(duration=500)  # Add a 0.5-second pause
        else:
            st.warning(f"Audio for '{sentence}' not found in the dataset.")

    return final_audio

# Streamlit interface OR STREAMLIT INTERFACE
def main():
    st.title('DSP Project Text-to-Speech (TTS) by Ayan, Rayyan, Zain (Ayan Output)')

    input_text = st.text_area("Enter something", "")
    
    if st.button("Convert to Speech"):
        if input_text.strip():
            st.write("Converting text to speech...")
            final_audio = text_to_audio_custom(input_text)

            output_file = 'output_audio.wav'
            final_audio.export(output_file, format='wav')
            st.audio(output_file, format='audio/wav')
        else:
            st.warning("Please enter some text!")

if __name__ == "__main__":
    main()

# OUR DSP PROJECT WAS TTS BUT IN CUSTOM VOICE I.E IS OUR OWN VOICE. SO WE TRIED IT
#1 WE WII SEE OUR PROGRAMV CODE
#2 THEN WE WILL TRY SOME INPUTS 
# SO LETS START
