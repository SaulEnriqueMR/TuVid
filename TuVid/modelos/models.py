# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Comentario(models.Model):
    idcomentario = models.AutoField(db_column='idComentario', primary_key=True)  # Field name made lowercase.
    contenido = models.TextField()
    fechacomentario = models.DateField(db_column='fechaComentario')  # Field name made lowercase.
    idcuenta = models.IntegerField(db_column='idCuenta')  # Field name made lowercase.
    idvideo = models.IntegerField(db_column='idVideo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comentario'


class Cuenta(models.Model):
    idcuenta = models.AutoField(db_column='idCuenta', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(unique=True, max_length=255)
    contrasenia = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Cuenta'


class Interaccion(models.Model):
    idinteraccion = models.AutoField(db_column='idInteraccion', primary_key=True)  # Field name made lowercase.
    idcuenta = models.IntegerField(blank=True, null=True)
    idvideo = models.IntegerField(db_column='idVideo')  # Field name made lowercase.
    idtipointeraccion = models.IntegerField(db_column='idTipoInteraccion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Interaccion'


class Notificacion(models.Model):
    idnotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)  # Field name made lowercase.
    contenido = models.CharField(max_length=255)
    idcuenta = models.IntegerField(db_column='idCuenta')  # Field name made lowercase.
    fechanotificacion = models.DateTimeField(db_column='fechaNotificacion')  # Field name made lowercase.
    visto = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Notificacion'


class Tipointeraccion(models.Model):
    idtipointeraccion = models.AutoField(db_column='idTipoInteraccion', primary_key=True)  # Field name made lowercase.
    nombreinteraccion = models.CharField(db_column='nombreInteraccion', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoInteraccion'


class Video(models.Model):
    idvideo = models.AutoField(db_column='idVideo', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=255)
    ubicacionvideo = models.CharField(db_column='ubicacionVideo', max_length=255)  # Field name made lowercase.
    ubicacionthumbnail = models.CharField(db_column='ubicacionThumbnail', max_length=255)  # Field name made lowercase.
    descripcion = models.TextField(blank=True, null=True)
    fechasubida = models.DateTimeField(db_column='fechaSubida')  # Field name made lowercase.
    idcuenta = models.IntegerField(db_column='idCuenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Video'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
