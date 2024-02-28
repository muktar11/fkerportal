# Generated by Django 4.2.3 on 2023-11-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_webcustomer_webcustomerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.CharField(choices=[('CSO', 'CSO'), ('SDM', 'SDM'), ('FM', 'FM'), ('FINANCE', 'FINANCE'), ('LOGISTIC', 'LOGISTIC'), ('GM', 'GM'), ('Clerk', 'Clerk'), ('Inventory', 'Inventory'), ('Supervisior', 'Supervisior'), ('superAdmin', 'superAdmin')], max_length=100),
        ),
    ]
