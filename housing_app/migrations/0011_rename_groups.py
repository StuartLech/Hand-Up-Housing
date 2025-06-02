from django.db import migrations


def rename_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Volunteer").update(name="Manager")
    Group.objects.filter(name="Social Worker").update(name="Client Services")


class Migration(migrations.Migration):
    dependencies = [
        ("housing_app", "0010_userprofile_activitylog"),
    ]

    operations = [
        migrations.RunPython(rename_groups, migrations.RunPython.noop),
    ]
