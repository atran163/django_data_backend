from django import forms

#age_choices = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
sex_choices = ["Male", "Female", "Other"]
sex_choices = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
num_employ  = [('1-5','1-5'), ('6-25', '6-25'), ('26-100', '26-100'), ('100-500','100-500'),('500-1000','500-1000'), ('>1000','>1000')]
mh_famhist  = [('Yes','Yes'), ('No','No')]
mh_resourc  = [('Yes','Yes'), ('No','No'), ("I don't know", "I don't know")]
mh_coverag  = [('Yes', 'Yes'), ('No', 'No'), ('Not eligible for coverage / N/A', 'Not eligible for coverage / N/A'), ("I don't know", "I don't know")]
mh_discuss  = [('Yes', 'Yes'), ('No','No'), ("I don't know", "I don't know")]
mh_negativ  = [('Maybe','Maybe'), ('Yes, I think they would','Yes, I think they would'), ("No, I don't think they would", "No, I don't think they would"),('Yes they do','Yes they do'),("No, they don't", "No they don't")]


class ModelForm(forms.Form):
   age = forms.IntegerField(label='What is your age?')
   #age = forms.CharField(label='What is your age?', widget=forms.Select(choices=age_choices))
   sex = forms.CharField(label='Gender?',required=False, widget=forms.Select(choices=sex_choices))
   num_emply = forms.CharField(label='How many employees are at your company?', widget=forms.Select(choices=num_employ))
   mh_famhist = forms.CharField(label='Does your family have a history of mental health disorders?', widget=forms.Select(choices=mh_famhist))
   mh_resourc = forms.CharField(label='Does your company provide mental health resources?', widget=forms.Select(choices=mh_resourc))
   mh_coverag = forms.CharField(label='Has your employer ever discussed mental health as part of an employee wellness program?', widget=forms.Select(choices=mh_coverag))
   mh_discuss = forms.CharField(label='Do you think that discussing a mental health issue with your employer would have negative consequences?', widget=forms.Select(choices=mh_discuss))
   mh_negativ = forms.CharField(label='Do you think that discussing a mental health issue with your coworkers would have negative consequences?', widget=forms.Select(choices=mh_negativ))



