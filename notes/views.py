from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteForm

# 🏠 Home View: Create + List + Search + Pinned
@login_required
def home(request):
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')

    query = request.GET.get('q')  # 🔍 Search input
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(title__icontains=query) | notes.filter(content__icontains=query)

    notes = notes.order_by('-is_pinned', '-created_at')  # 📌 Pinned notes first

    return render(request, 'notes/home.html', {'form': form, 'notes': notes})


# ✏️ Edit Note
@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/edit_note.html', {'form': form})


# 🗑️ Delete Note
@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'notes/delete_note.html', {'note': note})


# 📌 Toggle Pin/Unpin
@login_required
def toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('home')



from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject='Contact Form Message',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['youremail@example.com'],  # Replace with your real email
        )
        return render(request, 'notes/contact_success.html')

    return render(request, 'notes/contact.html')


def about(request):
    return render(request, 'notes/about.html')
