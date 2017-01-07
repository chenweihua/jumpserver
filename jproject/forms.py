# coding:utf-8
from django import forms

from jproject.models import Project,ProjectGroup,PublishConfig,Publish,SCMSetting,SCMToken,Schedule,Config,Env


class ProjectForm(forms.ModelForm):
    def __init__(self, scm_project_choices, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['scm_project'].choices = scm_project_choices

    scm_project = forms.ChoiceField(choices=(), required=True)

    class Meta:
        model = Project

        fields = [
            "name", "code", "scm_url","scm_project", "scm","scm_model_type", "scm_type", "owner", "dept", "group",
            "dependent", "manage", "phone", "work", "web_work","backup"
        ]

class ScmSettingForm(forms.ModelForm):
    class Meta:
        model = SCMSetting
        fields = []

class ScmTokenForm(forms.ModelForm):
    class Meta:
        model = SCMToken
        fields = []

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = []


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = []


class ProjectGroupForm(forms.ModelForm):
    class Meta:
        model = ProjectGroup
        fields = [
            "name", "code"
        ]


class PublishConfigForm(forms.ModelForm):
    class Meta:
        model = PublishConfig
        fields = ['project', "env", "file", 'item', 'confvalue', 'filetype']
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Name'}),
        #     'network': forms.Textarea(
        #         attrs={'placeholder': '192.168.1.0/24\n192.168.2.0/24'})
        # }


class EnvForm(forms.ModelForm):
    class Meta:
        model = Env
        fields = ['name', "code", "precode"]

class PublishForm(forms.ModelForm):
    class Meta:
        model = Publish
        fields = ['project','projectgroup','env','commits',
                  'branch','asset','assetgroup','schedule','user','before',
                  'after','model','status'
        ]
