from django.shortcuts import render,HttpResponse,redirect
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # assign logged-in user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()

    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/home.html', {'form': form, 'notes': notes})


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


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'notes/delete_note.html', {'note': note})
