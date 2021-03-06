<?php
/**
 *	Este script se llama de forma asíncrona mediante GET pasándole los datos de un usuario
 *	y crea el html que se utilizará en la GUI para mostrar al usuario
 */
    if (isset ($_POST['data'])) {
        $data = $_POST['data'];
        /*$json = array();
        $json['user_html'] = '<tr>';
        $json['user_html'] .= '	<td>'.$data[0]['uid'].'</td>';
        $json['user_html'] .= ' </td>';
        $json['user_html'] .= '</tr>';
        echo json_encode($json);*/
        /*$uid = $_GET['uid'];
        $gecos = $_GET['gecos'];
        $quota = $_GET['quota'];
        $course = $_GET['course'];
        $group = $_GET['group'];
        $profile = $_GET['profile'];
        $pair = $_GET['pair'];*/

        $json = array();
        foreach ($data as $d) {
            try{
                if ($d['pair'] == "true") {
                    $class = 'pair';
                } else {
                    $class = 'odd';
                }
                //$class = ($pair)?'pair':'odd';
                $json['user_html'] .= '<tr class="'.$class.'" id="user-'.$d['uid'].'">';
                $json['user_html'] .= '	<td id="element-'.$d['uid'].'"><input type="checkbox" name="element_sel" class="el_sel"/></td>';
                $json['user_html'] .= '	<td>'.$d['uid'].'</td>';
                $json['user_html'] .= '	<td id="gecos-'.$d['uid'].'">'.$d['gecos'].'</td>';
                $json['user_html'] .= '	<td id="group-'.$d['uid'].'">'.$d['group'].'</td>';
                $json['user_html'] .= '	<td id="profile-'.$d['uid'].'">'.$d['profile'].'</td>';
                $json['user_html'] .= '	<td id="quota-'.$d['uid'].'">'.$d['quota'].'</td>';
                $json['user_html'] .= '	<td id="course-'.$d['uid'].'">'.$d['course'].'</td>';
                $json['user_html'] .= ' <td>';
                $json['user_html'] .= ' 	<a name="edit" href="edit" title="editar usuario" uid="'.$d['uid'].'" class="icon action edit user_edit_icon"></a>';
                $json['user_html'] .= ' 	<a name="del" href="del" title="eliminar usuario" uid="'.$d['uid'].'" class="icon action del user_del_icon"></a>';
                $json['user_html'] .= ' </td>';
                $json['user_html'] .= '</tr>';

            }catch(Exception $e){
                $json['error'] = $e->getMessage();
            }
        }
    } else {
        $json['user_html'] .= '<tr class="odd">';
        $json['user_html'] .= '	<td></td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= '	<td> - </td>';
        $json['user_html'] .= ' <td> - </td>';
        $json['user_html'] .= '</tr>';
    }

	echo json_encode($json);
?>