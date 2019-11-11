# Generated by Django 2.2.6 on 2019-11-11 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountExtension',
            fields=[
                ('Account_Number', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=60)),
                ('Phone_Number', models.CharField(max_length=20)),
                ('Balance', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='AtMachine',
            fields=[
                ('At_Machine_UID', models.AutoField(primary_key=True, serialize=False)),
                ('Current_Balance', models.DecimalField(decimal_places=0, default=0, max_digits=25)),
                ('Location', models.CharField(max_length=100)),
                ('MinimumBalance', models.DecimalField(decimal_places=0, default=0, max_digits=25)),
                ('Status', models.CharField(max_length=50)),
                ('Last_Refill_Date', models.DateField()),
                ('Next_Maintenance_Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AtmCard',
            fields=[
                ('Atm_Card_Number', models.AutoField(primary_key=True, serialize=False)),
                ('PIN', models.IntegerField()),
                ('Name', models.CharField(max_length=60)),
                ('Date_Of_Issue', models.DateField(auto_now_add=True)),
                ('Expiry_Date', models.DateField(auto_now_add=True)),
                ('Address', models.CharField(max_length=100)),
                ('Two_Factor_Authentication_Status', models.BooleanField()),
                ('Phone_Number', models.CharField(max_length=20)),
                ('Card_Status', models.CharField(max_length=50)),
                ('Account_Number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ATM.AccountExtension')),
            ],
        ),
        migrations.CreateModel(
            name='Balance_Enquiry',
            fields=[
                ('Transaction_ID', models.OneToOneField(db_column='Transaction_ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ATM.Transaction')),
                ('Balance_Amount', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Cash_Transfer',
            fields=[
                ('Transaction_ID', models.OneToOneField(db_column='Transaction_ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ATM.Transaction')),
                ('Beneficiary_Account_Number', models.IntegerField()),
                ('Beneficiary_Name', models.CharField(max_length=60)),
                ('Amout_Transferred', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
            ],
        ),
        migrations.CreateModel(
            name='Cash_Withdrawal',
            fields=[
                ('Transaction_ID', models.OneToOneField(db_column='Transaction_ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ATM.Transaction')),
                ('Amount_Transferred', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Denomination', models.CharField(default='USD', max_length=20)),
                ('Current_Balance', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Phone_Change',
            fields=[
                ('Transaction_ID', models.OneToOneField(db_column='Transaction_ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ATM.Transaction')),
                ('New_Phone_Number', models.CharField(default='0', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pin_Change',
            fields=[
                ('Transaction_ID', models.OneToOneField(db_column='Transaction_ID', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ATM.Transaction')),
                ('Previous_Pin', models.IntegerField()),
                ('New_Pin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('Account_Number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ATM.AccountExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('Transaction_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Status', models.CharField(max_length=50)),
                ('Response_Code', models.CharField(max_length=256)),
                ('Type_Of_Transaction', models.CharField(max_length=50)),
                ('ATM_Card_Number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ATM.AtmCard')),
                ('At_Machine_UID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ATM.AtMachine')),
            ],
        ),
        migrations.CreateModel(
            name='ATMachineRefill',
            fields=[
                ('Refill_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Amount', models.DecimalField(decimal_places=0, default=0, max_digits=25)),
                ('ATM_Branch', models.CharField(max_length=100)),
                ('Refill_Date', models.DateField()),
                ('Previous_Balance', models.DecimalField(decimal_places=0, default=0, max_digits=25)),
                ('At_Machine_UID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ATM.AtMachine')),
            ],
        ),
    ]
