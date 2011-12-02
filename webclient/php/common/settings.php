<?php
include_once("../config.php");
?>

<div class="form_section wrap">
	<h3>Datos de configuraci&oacute;n</h3>
	<p class="description">Completa los datos de la cuenta. Todos los datos de esta sección son obligatorios</p>
	<table>
		<tr>
			<td class="left">
				<label for="uid">Contrase&ntilde;a actual</label>
			</td>
			<td class="right">
				<input type="password" name="old_pwd" class="input" />
			</td>
		</tr>
		<tr>
			<td class="left">
				<label for="pwd">Contrase&ntilde;a nueva</label>
			</td>
			<td class="right">
				<input type="password" name="pwd" class="input" />
			</td>
		</tr>
		<tr>
			<td class="left">
				<label for="pwd">Repite la contrase&ntilde;a</label>
			</td>
			<td class="right">
				<input type="password" name="pwd2" class="input" />
			</td>
		</tr>
	</table>
</div>
<div class="form_line wrap"></div>
<div class="form_section wrap">
    <!--<input type="button" onclick="UserOperations.create_user();" value="Crear usuario/s" class="btn" />-->
    <input type="submit" name="edit_settings" value="Guardar" class="btn"/>
</div>