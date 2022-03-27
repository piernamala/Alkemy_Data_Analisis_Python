from decouple import config

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 
'septiembre', 'octubre', 'noviembre', 'diciembre']

category = {
  'museo' : config('URL_museo'), 
  'cine' : config('URL_cine'),
  'biblioteca' : config('URL_biblioteca')
}

nombres_columnas=['cod_localidad', 'id_provincia', 'id_departamento', 'categoría', 'provincia', 'localidad', 'nombre', 'domicilio', 'código postal', 'número de teléfono', 'mail', 'web', 'fuente']

museos_drop = ['Observaciones', 'subcategoria', 'piso', 'cod_area', 'Latitud', 'Longitud','TipoLatitudLongitud', 'Info_adicional', 'jurisdiccion', 'año_inauguracion', 'actualizacion']
museos_newname = {'Cod_Loc': 'cod_localidad', 'IdProvincia': 'id_provincia', 'IdDepartamento': 'id_departamento', 'categoria': 'categoría', 'provincia':'provincia', 'localidad': 'localidad', 'nombre':'nombre', 'direccion':'domicilio', 'CP':'código postal', 'telefono':'número de teléfono', 'Mail':'mail', 'Web':'web', 'fuente':'fuente'}



cine_drop = ['Observaciones','Departamento','Piso', 'cod_area', 'Información adicional', 'Latitud', 'Longitud', 'TipoLatitudLongitud','tipo_gestion', 'Pantallas', 'Butacas', 'espacio_INCAA', 'año_actualizacion']
cine_newname = {'Cod_Loc': 'cod_localidad', 'IdProvincia': 'id_provincia', 'IdDepartamento': 'id_departamento', 'Categoría': 'categoría', 'Provincia':'provincia', 'Localidad':'localidad', 'Nombre' : 'nombre', 'Dirección':'domicilio', 'CP':'código postal', 'Teléfono':'número de teléfono', 'Mail':'mail', 'Web':'web', 'Fuente':'fuente'}

biblioteca_drop = ['Observacion','Subcategoria','Departamento', 'Piso', 'Cod_tel', 'Información adicional', 'Latitud', 'Longitud', 'TipoLatitudLongitud', 'Tipo_gestion', 'año_inicio', 'Año_actualizacion']
biblioteca_newname = {'Cod_Loc': 'cod_localidad', 'IdProvincia': 'id_provincia', 'IdDepartamento': 'id_departamento', 'Categoría': 'categoría', 'Provincia':'provincia', 'Localidad':'localidad', 'Nombre' : 'nombre', 'Domicilio':'domicilio', 'CP':'código postal', 'Teléfono':'número de teléfono', 'Mail':'mail', 'Web':'web','Fuente':'fuente'}

DBsettings = {'pguser':config('pguser'),
              'pgpasswd':config('pgpasswd'),
              'pghost':config('pghost'),
              'pgport':config('pgport'),
              'pgdb':config('pgdb')
             }

