from django.forms.widgets import ChoiceWidget

class FlatRadioSelect(ChoiceWidget):
    input_type = 'radio'
    template_name = 'widgets/flat_radio.html'
    option_template_name = 'widgets/flat_radio_option.html'