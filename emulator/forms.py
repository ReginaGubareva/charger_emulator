from django import forms


class ChargerForm(forms.Form):
    serial_number = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    # install_date = forms.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    address_gps_location = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    # charger_image = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    user = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))


class HeartbeatForm(forms.Form):
    serial_number = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    max_chargeKW = forms.IntegerField(label='max charge KW')
    max_amps = forms.IntegerField(label='max amps')
    max_voltage = forms.IntegerField(label='max voltage')
    public_ip_address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    private_ip_address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    mac_address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    dns = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    firmware_version = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    state = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))


class SerialNumberForm(forms.Form):
    serial_number = forms.CharField(max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))