# Generated by Django 3.1.5 on 2021-04-15 03:19

import DB.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountEmailaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=254, unique=True)),
                ('verified', models.IntegerField()),
                ('primary', models.IntegerField()),
            ],
            options={
                'db_table': 'account_emailaddress',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountEmailconfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('sent', models.DateTimeField(blank=True, null=True)),
                ('key', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'db_table': 'account_emailconfirmation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('alarm_no', models.AutoField(db_column='ALARM_NO', primary_key=True, serialize=False)),
                ('alarm_cont', models.CharField(db_column='ALARM_CONT', max_length=150)),
                ('alarm_link', models.CharField(db_column='ALARM_LINK', max_length=150, null=True)),
                ('alarm_ischecked', models.IntegerField(db_column='ALARM_ISCHECKED', default=0)),
                ('alarm_date', models.DateTimeField(auto_now_add=True, db_column='ALARM_DATE')),
            ],
            options={
                'db_table': 'ALARM',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(db_column='ANSWER_ID', primary_key=True, serialize=False)),
                ('answer_cont', models.CharField(db_column='ANSWER_CONT', max_length=5000)),
                ('answer_created', models.DateTimeField(auto_now_add=True, db_column='ANSWER_CREATED')),
            ],
            options={
                'db_table': 'ANSWER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank_no', models.AutoField(db_column='BANK_NO', primary_key=True, serialize=False)),
                ('bank_plus', models.IntegerField(blank=True, db_column='BANK_PLUS', default=0)),
                ('bank_minus', models.IntegerField(blank=True, db_column='BANK_MINUS', default=0)),
                ('bank_title', models.CharField(blank=True, db_column='BANK_TITLE', max_length=100, null=True)),
                ('bank_used', models.DateTimeField(blank=True, db_column='BANK_USED')),
                ('bank_created', models.DateTimeField(auto_now_add=True, db_column='BANK_CREATED')),
                ('bank_updated', models.DateTimeField(auto_now=True, db_column='BANK_UPDATED', null=True)),
                ('bank_checked', models.DateTimeField(db_column='BANK_CHECKED', null=True)),
                ('bank_allowed', models.DateTimeField(db_column='BANK_ALLOWED', null=True)),
                ('bank_reason', models.CharField(blank=True, db_column='BANK_REASON', max_length=300, null=True)),
                ('bank_reject_reason', models.CharField(blank=True, db_column='BANK_REJECT_REASON', max_length=200, null=True)),
                ('bank_account', models.CharField(blank=True, db_column='BANK_ACCOUNT', max_length=100, null=True)),
            ],
            options={
                'db_table': 'BANK',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BankApplyInfo',
            fields=[
                ('bank_apply_no', models.AutoField(db_column='BANK_APPLY_NO', primary_key=True, serialize=False)),
                ('bank_apply_name', models.CharField(db_column='BANK_APPLY_NAME', max_length=20)),
            ],
            options={
                'db_table': 'BANK_APPLY_INFO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BankFile',
            fields=[
                ('bank_file_id', models.AutoField(db_column='BANK_FILE_ID', primary_key=True, serialize=False)),
                ('bank_file_path', models.FileField(db_column='BANK_FILE_PATH', max_length=1000, upload_to=DB.models.bank_file_upload_to)),
                ('bank_file_name', models.CharField(db_column='BANK_FILE_NAME', max_length=500)),
            ],
            options={
                'db_table': 'BANK_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('board_no', models.AutoField(db_column='BOARD_NO', primary_key=True, serialize=False)),
                ('board_title', models.CharField(db_column='BOARD_TITLE', max_length=100)),
                ('board_cont', models.CharField(db_column='BOARD_CONT', max_length=5000)),
                ('board_created', models.DateTimeField(auto_now_add=True, db_column='BOARD_CREATED')),
            ],
            options={
                'db_table': 'BOARD',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BoardFile',
            fields=[
                ('file_id', models.AutoField(db_column='FILE_ID', primary_key=True, serialize=False)),
                ('file_name', models.CharField(db_column='FILE_NAME', max_length=300)),
                ('file_path', models.ImageField(blank=True, db_column='FILE_PATH', null=True, upload_to=DB.models.board_file_upload_to)),
            ],
            options={
                'db_table': 'BOARD_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BoardType',
            fields=[
                ('board_type_no', models.AutoField(db_column='BOARD_TYPE_NO', primary_key=True, serialize=False)),
                ('board_type_name', models.CharField(db_column='BOARD_TYPE_NAME', max_length=50)),
                ('board_type_exp', models.CharField(db_column='BOARD_TYPE_EXP', max_length=100)),
            ],
            options={
                'db_table': 'BOARD_TYPE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChiefCarrier',
            fields=[
                ('carrier_no', models.AutoField(db_column='CARRIER_NO', primary_key=True, serialize=False)),
                ('carrier_content', models.CharField(blank=True, db_column='CARRIER_CONTENT', max_length=300, null=True)),
            ],
            options={
                'db_table': 'CHIEF_CARRIER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(db_column='COMMENT_ID', primary_key=True, serialize=False)),
                ('comment_cont', models.CharField(db_column='COMMENT_CONT', max_length=5000)),
                ('comment_created', models.DateTimeField(auto_now_add=True, db_column='COMMENT_CREATED')),
            ],
            options={
                'db_table': 'COMMENT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContestBoard',
            fields=[
                ('contest_no', models.AutoField(db_column='CONTEST_NO', primary_key=True, serialize=False)),
                ('contest_title', models.CharField(db_column='CONTEST_TITLE', max_length=100)),
                ('contest_cont', models.CharField(db_column='CONTEST_CONT', max_length=5000)),
                ('contest_created', models.DateTimeField(auto_now_add=True, db_column='CONTEST_CREATED')),
                ('contest_topic', models.CharField(db_column='CONTEST_TOPIC', max_length=500)),
                ('contest_asso', models.CharField(db_column='CONTEST_ASSO', max_length=100)),
                ('contest_deadline', models.DateTimeField(db_column='CONTEST_DEADLINE')),
                ('contest_start', models.DateTimeField(db_column='CONTEST_START')),
            ],
            options={
                'db_table': 'CONTEST_BOARD',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContestComment',
            fields=[
                ('comment_id', models.AutoField(db_column='COMMENT_ID', primary_key=True, serialize=False)),
                ('comment_cont', models.CharField(db_column='COMMENT_CONT', max_length=500)),
                ('comment_created', models.DateTimeField(auto_now_add=True, db_column='COMMENT_CREATED')),
            ],
            options={
                'db_table': 'CONTEST_COMMENT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContestFile',
            fields=[
                ('file_id', models.AutoField(db_column='FILE_ID', primary_key=True, serialize=False)),
                ('file_name', models.CharField(db_column='FILE_NAME', max_length=300)),
                ('file_path', models.ImageField(db_column='FILE_PATH', upload_to=DB.models.contest_file_upload_to)),
            ],
            options={
                'db_table': 'CONTEST_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'django_site',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('history_no', models.AutoField(db_column='HISTORY_NO', primary_key=True, serialize=False)),
                ('history_cont', models.CharField(db_column='HISTORY_CONT', max_length=500)),
                ('history_date', models.DateTimeField(db_column='HISTORY_DATE')),
            ],
            options={
                'db_table': 'HISTORY',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lect',
            fields=[
                ('lect_no', models.AutoField(db_column='LECT_NO', primary_key=True, serialize=False)),
                ('lect_title', models.CharField(db_column='LECT_TITLE', max_length=100)),
                ('lect_pic', models.ImageField(db_column='LECT_PIC', max_length=1000, upload_to='lect/')),
                ('lect_created', models.DateTimeField(auto_now_add=True, db_column='LECT_CREATED')),
                ('lect_intro', models.CharField(db_column='LECT_INTRO', max_length=300)),
                ('lect_curri', models.TextField(db_column='LECT_CURRI')),
                ('lect_limit_num', models.IntegerField(db_column='LECT_LIMIT_NUM')),
                ('lect_place_or_link', models.CharField(db_column='LECT_PLACE_OR_LINK', max_length=1000)),
                ('lect_deadline', models.DateTimeField(db_column='LECT_DEADLINE')),
            ],
            options={
                'db_table': 'LECT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoard',
            fields=[
                ('lect_board_no', models.AutoField(db_column='LECT_BOARD_NO', primary_key=True, serialize=False)),
                ('lect_board_title', models.CharField(db_column='LECT_BOARD_TITLE', max_length=100)),
                ('lect_board_created', models.DateTimeField(auto_now_add=True, db_column='LECT_BOARD_CREATED')),
                ('lect_board_cont', models.TextField(db_column='LECT_BOARD_CONT')),
                ('lect_board_deadline', models.DateTimeField(db_column='LECT_BOARD_DEADLINE')),
            ],
            options={
                'db_table': 'LECT_BOARD',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardAnswer',
            fields=[
                ('lect_ans_no', models.AutoField(db_column='LECT_ANS_NO', primary_key=True, serialize=False)),
                ('lect_ans_cont', models.CharField(blank=True, db_column='LECT_ANS_CONT', max_length=5000, null=True)),
                ('lect_ans_created', models.DateTimeField(auto_now_add=True, db_column='LECT_ANS_CREATED')),
            ],
            options={
                'db_table': 'LECT_BOARD_ANSWER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardAnswerFile',
            fields=[
                ('lect_ans_file_id', models.AutoField(db_column='LECT_ANS_FILE_ID', primary_key=True, serialize=False)),
                ('lect_ans_file_path', models.CharField(db_column='LECT_ANS_FILE_PATH', max_length=1000)),
            ],
            options={
                'db_table': 'LECT_BOARD_ANSWER_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardComment',
            fields=[
                ('lect_board_comment_id', models.AutoField(db_column='LECT_BOARD_COMMENT_ID', primary_key=True, serialize=False)),
                ('lect_board_comment_cont', models.TextField(db_column='LECT_BOARD_COMMENT_CONT')),
                ('lect_board_comment_date', models.DateTimeField(db_column='LECT_BOARD_COMMENT_DATE')),
            ],
            options={
                'db_table': 'LECT_BOARD_COMMENT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardEx',
            fields=[
                ('lect_board_ex_no', models.AutoField(db_column='LECT_BOARD_EX_NO', primary_key=True, serialize=False)),
                ('lect_board_ex_content', models.TextField(blank=True, db_column='LECT_BOARD_EX_CONTENT', null=True)),
            ],
            options={
                'db_table': 'LECT_BOARD_EX',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardExFile',
            fields=[
                ('lect_board_ex_file_id', models.AutoField(db_column='LECT_BOARD_EX_FILE_ID', primary_key=True, serialize=False)),
                ('lect_board_ex_file_path', models.CharField(db_column='LECT_BOARD_EX_FILE_PATH', max_length=1000)),
            ],
            options={
                'db_table': 'LECT_BOARD_EX_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectBoardFile',
            fields=[
                ('lect_board_file_id', models.AutoField(db_column='LECT_BOARD_FILE_ID', primary_key=True, serialize=False)),
                ('lect_board_file_path', models.CharField(db_column='LECT_BOARD_FILE_PATH', max_length=1000)),
            ],
            options={
                'db_table': 'LECT_BOARD_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectCheck',
            fields=[
                ('check_id', models.AutoField(db_column='CHECK_ID', primary_key=True, serialize=False)),
                ('check_date', models.DateTimeField(db_column='CHECK_DATE')),
            ],
            options={
                'db_table': 'LECT_CHECK',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectType',
            fields=[
                ('type_no', models.AutoField(db_column='TYPE_NO', primary_key=True, serialize=False)),
                ('type_name', models.IntegerField(db_column='TYPE_NAME')),
            ],
            options={
                'db_table': 'LECT_TYPE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectUser',
            fields=[
                ('lect_user_stu', models.AutoField(db_column='LECT_USER_STU', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'LECT_USER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MajorInfo',
            fields=[
                ('major_no', models.AutoField(db_column='MAJOR_NO', primary_key=True, serialize=False)),
                ('major_colleage', models.CharField(db_column='MAJOR_COLLEAGE', max_length=10)),
                ('major_name', models.CharField(db_column='MAJOR_NAME', max_length=20, unique=True)),
            ],
            options={
                'db_table': 'MAJOR_INFO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MethodInfo',
            fields=[
                ('method_no', models.AutoField(db_column='METHOD_NO', primary_key=True, serialize=False)),
                ('method_name', models.CharField(db_column='METHOD_NAME', max_length=100)),
            ],
            options={
                'db_table': 'METHOD_INFO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuestForm',
            fields=[
                ('quest_no', models.AutoField(db_column='QUEST_NO', primary_key=True, serialize=False)),
                ('quest_name', models.CharField(db_column='QUEST_NAME', max_length=500)),
            ],
            options={
                'db_table': 'QUEST_FORM',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialaccountSocialaccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=30)),
                ('uid', models.CharField(max_length=191)),
                ('last_login', models.DateTimeField()),
                ('date_joined', models.DateTimeField()),
                ('extra_data', models.TextField()),
            ],
            options={
                'db_table': 'socialaccount_socialaccount',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialaccountSocialapp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=40)),
                ('client_id', models.CharField(max_length=191)),
                ('secret', models.CharField(max_length=191)),
                ('key', models.CharField(max_length=191)),
            ],
            options={
                'db_table': 'socialaccount_socialapp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialaccountSocialappSites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'socialaccount_socialapp_sites',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialaccountSocialtoken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('token_secret', models.TextField()),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'socialaccount_socialtoken',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialLoginBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'social_login_blog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StateInfo',
            fields=[
                ('state_no', models.AutoField(db_column='STATE_NO', primary_key=True, serialize=False)),
                ('state_name', models.CharField(db_column='STATE_NAME', max_length=50)),
            ],
            options={
                'db_table': 'STATE_INFO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_no', models.AutoField(primary_key=True, serialize=False)),
                ('test_name', models.TextField()),
            ],
            options={
                'db_table': 'test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_email', models.CharField(db_column='USER_EMAIL', max_length=100)),
                ('user_stu', models.IntegerField(db_column='USER_STU', primary_key=True, serialize=False)),
                ('user_name', models.CharField(db_column='USER_NAME', max_length=50)),
                ('user_pic', models.ImageField(blank=True, db_column='USER_PIC', null=True, upload_to=DB.models.user_pic_upload_to)),
                ('user_joined', models.DateTimeField(auto_now_add=True, db_column='USER_JOINED')),
                ('user_grade', models.IntegerField(db_column='USER_GRADE')),
                ('user_gen', models.IntegerField(db_column='USER_GEN')),
                ('user_phone', models.CharField(db_column='USER_PHONE', max_length=15, unique=True)),
            ],
            options={
                'db_table': 'USER',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('auth_no', models.AutoField(db_column='AUTH_NO', primary_key=True, serialize=False)),
                ('auth_name', models.CharField(db_column='AUTH_NAME', max_length=50)),
            ],
            options={
                'db_table': 'USER_AUTH',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserDeleteFile',
            fields=[
                ('user_delete_id', models.AutoField(db_column='USER_DELETE_ID', primary_key=True, serialize=False)),
                ('user_delete_file_path', models.CharField(db_column='USER_DELETE_FILE_PATH', max_length=1000)),
            ],
            options={
                'db_table': 'USER_DELETE_FILE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('email_no', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'USER_EMAIL',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('role_no', models.AutoField(db_column='ROLE_NO', primary_key=True, serialize=False)),
                ('role_name', models.CharField(db_column='ROLE_NAME', max_length=50)),
            ],
            options={
                'db_table': 'USER_ROLE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserUpdateRequest',
            fields=[
                ('updated_no', models.AutoField(db_column='UPDATED_NO', primary_key=True, serialize=False)),
                ('updated_user_name', models.CharField(db_column='UPDATED_USER_NAME', max_length=50)),
                ('updated_reject_reason', models.CharField(db_column='UPDATED_REJECT_REASON', max_length=200, null=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True, db_column='UPDATED_DATE')),
            ],
            options={
                'db_table': 'USER_UPDATE_REQUEST',
                'managed': False,
            },
        ),
    ]
