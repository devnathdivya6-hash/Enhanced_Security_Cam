from django.shortcuts import render, redirect, get_object_or_404
import os
import io
import speech_recognition as sr
from django.http import JsonResponse
from pydub import AudioSegment
from .models import InterCom
from face.models import Register
from django.contrib.auth.models import User
from django.contrib import messages




# ✅ Manually Set FFmpeg & FFprobe Paths (Force Pydub to Use Them)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin\ffmpeg-master-latest-win64-gpl-shared\bin"
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
os.environ["FFPROBE_BINARY"] = r"C:\ffmpeg\bin\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"
# ✅ Force Pydub to use these paths
AudioSegment.converter = os.environ["FFMPEG_BINARY"]
AudioSegment.ffmpeg = os.environ["FFMPEG_BINARY"]
AudioSegment.ffprobe = os.environ["FFPROBE_BINARY"]

# ✅ Debugging: Check if Python now detects FFmpeg
print(f"🎯 FFmpeg Path in ENV: {os.environ['FFMPEG_BINARY']}")
print(f"🎯 FFprobe Path in ENV: {os.environ['FFPROBE_BINARY']}")

if not os.path.exists(os.environ["FFMPEG_BINARY"]):
    print(f"❌ FFmpeg is NOT FOUND at: {os.environ['FFMPEG_BINARY']}")
else:
    print(f"✅ FFmpeg FOUND at: {os.environ['FFMPEG_BINARY']}")

if not os.path.exists(os.environ["FFPROBE_BINARY"]):
    print(f"❌ FFprobe is NOT FOUND at: {os.environ['FFPROBE_BINARY']}")
else:
    print(f"✅ FFprobe FOUND at: {os.environ['FFPROBE_BINARY']}")


def convert_webm_to_wav(audio_blob):
    """Convert WebM audio to WAV format."""
    try:
        print("🟡 Step 1: Reading uploaded WebM file...")
        audio_data = audio_blob.read()
        webm_io = io.BytesIO(audio_data)

        print("🔄 Step 2: Converting WebM to WAV...")
        # Convert WebM to WAV using pydub
        audio = AudioSegment.from_file(webm_io, format="webm")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")

        wav_io.seek(0)
        print("✅ Step 3: WebM successfully converted to WAV!")
        return wav_io
    except Exception as e:
        print(f"🔥 Error converting WebM to WAV: {e}")
        return None

def send_message(request):
    """Process recorded audio, convert it to text, and return it."""
    print("🟢 Received a POST request at /send_message")

    if request.method == "POST":
        print("🟡 Step 1: Checking uploaded file...")
        audio_blob = request.FILES.get('audio_blob')

        if not audio_blob:
            print("❌ No audio file uploaded!")
            return JsonResponse({'status': 'error', 'message': 'No audio file uploaded'}, status=400)

        print("✅ Step 2: Audio file found. Converting to WAV...")
        wav_audio = convert_webm_to_wav(audio_blob)

        if not wav_audio:
            print("❌ Conversion failed!")
            return JsonResponse({'status': 'error', 'message': 'Failed to convert WebM to WAV'}, status=500)

        recognizer = sr.Recognizer()

        try:
            print("🎤 Step 3: Processing WAV file with SpeechRecognition...")
            with sr.AudioFile(wav_audio) as source:
                audio_data = recognizer.record(source)

            print("📝 Step 4: Converting speech to text...")
            text = recognizer.recognize_google(audio_data)

            print(f"✅ Speech Recognized: {text}")

            # Save message to the database
            InterCom.objects.create(user=Register.objects.get(id=request.user.id), message=text)
            print("✅ Step 5: Message saved to database!")
            return redirect("admin_messages")
            # return JsonResponse({'status': 'success', 'message': 'Message recorded and saved!', 'text': text})

        except sr.UnknownValueError:
            print("❌ Could not understand audio!")
            return JsonResponse({'status': 'error', 'message': 'Could not understand audio'}, status=400)
        except sr.RequestError as e:
            print(f"❌ Speech Recognition API Error: {e}")
            return JsonResponse({'status': 'error', 'message': f'Speech-to-text service error: {e}'}, status=500)

    print("❌ Invalid request method!")
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)







def admin_view_messages(request):
    messages_list = InterCom.objects.all().order_by('-date_taken')  # Show latest messages first

    if request.method == "POST":
        message_id = request.POST.get("message_id")
        response_text = request.POST.get("response_text")

        # ✅ Fetch message and update response
        message_instance = get_object_or_404(InterCom, id=message_id)
        message_instance.response = response_text
        message_instance.save()

        messages.success(request, "Response saved successfully!")
        return redirect("admin_messages")  # Redirect to refresh the page

    return render(request, "admin_messages.html", {"messages_list": messages_list})



def user_messages(request):
    """Display the logged-in user's messages and admin responses."""
    user_messages = InterCom.objects.filter(user=request.user).order_by('-date_taken')  # Show latest messages first
    return render(request, "play_voice.html", {"user_messages": user_messages})








def record_voice(request):
    """Render the interview page and show previous messages."""
    messages = InterCom.objects.all().order_by('-id')[:5]  # Get last 5 messages
    return render(request, 'record_voice.html', {'messages': messages})



