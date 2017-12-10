from django import forms

class SearchRoomForm(forms.Form):
    room_name = forms.CharField(label='Room', max_length=255)