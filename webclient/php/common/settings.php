<?php
include_once("../config.php");
?>

<div class="form_section wrap">
	<h3>Datos de configuraci&oacute;n</h3>
	<p>Completa los datos de la cuenta. Todos los datos de esta sección son obligatorios</p>
	<table>
		<tr>
			<td>
				<label for="uid">Contrase&ntilde;a actual</label>
			</td>
			<td>
				<input type="password" name="old_pwd" class="input" />
			</td>
		</tr>
		<tr>
			<td>
				<label for="pwd">Contrase&ntilde;a nueva</label>
			</td>
			<td>
				<input type="password" name="pwd" class="input" />
			</td>
		</tr>
		<tr>
			<td>
				<label for="pwd">Repite la contrase&ntilde;a</label>
			</td>
			<td>
				<input type="password" name="pwd_" class="input" />
			</td>
		</tr>
	</table>
</div>
<div class="form_line wrap"></div>
<input type="submit" name="edit_settings" value="Guardar" class="btn"/>