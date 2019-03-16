from django import forms

from ..api import team as Team
from ..api import criteria as Criteria
from ..api import criteria_label as CriteriaLabel
from ..widgets.flat_radio_select import FlatRadioSelect

class EvaluationForm(forms.Form):
    team = forms.ModelChoiceField(Team.search().order_by('table', 'name'))

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        criteria = Criteria.search()
        for criterion in criteria:
            # Define field ID
            criteria_field_name = 'criteria-{}'.format(criterion.id)
            # Define range of scores
            scores = list(range(criterion.min_score, criterion.max_score + 1))
            score_strs = [str(score) for score in scores]
            choices = list(zip(scores, score_strs))
            # Get labels for each score in the range
            score_labels = []
            for score in scores:
                labels = CriteriaLabel.search(criteria_id=criterion.id, score=score)
                if len(labels) == 0:
                    score_labels.append(str(score))
                else:
                    score_labels.append('{}. {}'.format(score, labels[0].label))

            self.fields[criteria_field_name] = forms.ChoiceField(choices=choices,
                                                                 widget=FlatRadioSelect(attrs={'labels': score_labels}),
                                                                 label=criterion.name)