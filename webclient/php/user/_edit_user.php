<?php
include_once("../config.php");
?>
<form method="POST" action="" id="user_edit_form">
    <div class="form_section wrap">
        <h3>Datos del usuario</h3>
        <p class="description">Completa los datos referentes a la identificaci&oacute;n del usuario. Todos los datos de esta secci&oacute;n son obligatorios</p>
        <table>
            <tr>
                <td class="left">
                    <label for="uid">Nombre de usuario</label>
                </td>
                <td class="right">
                    <input type="text" id="uid" name="uid" class="input" required="required" value="<?php echo $_POST['user']['uid'];?>" filtered="filtered" readonly />
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="pwd">Contrase&ntilde;a</label>
                </td>
                <td class="right">
                    <input type="password" id="pwd" name="pwd" class="input" filtered="filtered" />
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="pwd2">Repite la contrase&ntilde;a</label>
                </td>
                <td class="right">
                    <input type="password" id="pwd2" name="pwd2" class="input"/>
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="gecos">Nombre completo</label>
                </td>
                <td class="right">
                    <input type="text" id="gecos" name="gecos" class="input" required="required" value="<?php echo $_POST['user']['gecos'];?>"/>
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
        </table>
    </div>
    <div class="form_section wrap">
        <h3>Propiedades de la cuenta</h3>
        <p class="description">Completa los datos referentes a las propiedades de la cuenta del usuario.</p>
        <table>
            <tr>
                <td class="left">
                    <label for="quota">Cuota</label>
                </td>
                <td class="right">
                    <input type="text" id="quota" name="quota" class="input" required="required" integer="integer" value="<?php echo $_POST['user']['quota'];?>"/>
                    <img alt="Cuota" title="Espacio para el usuario en MB" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_quota_edit"/>
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="course">Curso</label>
                </td>
                <td class="right">
                    <input type="text" id="course" name="course" class="input" required="required" value="<?php echo $_POST['user']['course'];?>" lessfiltered="lessfiltered" />
                    <img alt="Curso" title="Curso del usuario" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_course_edit"/>
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="profile">Perfil</label>
                </td>
                <td class="right">
                    <select id="profile" name="profile">
                        <? if ($_POST['user']['profile'] == 1) {?>
                        <option selected value="1">Fijo</option>
                        <option value="2">M&oacute;vil</option>
                        <? } else { ?>
                        <option value="1">Fijo</option>
                        <option selected value="2">M&oacute;vil</option>
                        <? } ?>
                    </select>
                    <img alt="Perfil" title="Tipo de perfil" src="http://<?php echo SERVER_NAME.APP_DIR;?>/img/common/info_icon.png" width="16" height="16" class="user_img_profile_edit"/>
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
            <tr>
                <td class="left">
                    <label for="group">Grupo</label>
                </td>
                <td class="right">
                    <select id=group" name="group">
                        <? if ($_POST['user']['group'] == 1) {?>
                        <option selected value="1">Alumno</option>
                        <option value="2">Gesti&oacute;n</option>
                        <option value="3">Profesor</option>
                        <? } else if ($_POST['user']['group'] == 2){ ?>
                        <option value="1">Alumno</option>
                        <option selected value="2">Gesti&oacute;n</option>
                        <option value="3">Profesor</option>
                        <? } else { ?>
                        <option value="1">Alumno</option>
                        <option value="2">Gesti&oacute;n</option>
                        <option selected value="3">Profesor</option>
                        <? } ?>
                    </select>
                    <!--<span class="error"></span>-->
                </td>
                <td class="form_error">
                    <span class="error"></span>
                </td>
            </tr>
        </table>
        <!--<a class="note reset" href="#" onclick="$(GUI.main_frm).reset();return false;">resetear</a>-->
    </div>
    <!--<div class="form_line wrap"></div>
    <div class="form_section wrap">
        <input type="button" onclick="Common.create_user();" value="Crear usuario" class="btn" />
    </div>-->
</form>
