<?php
	include_once('../../config.php');
	
	session_name(SESSION_NAME);
	session_start();

	$json_res = array();	
	try{
		switch ($_POST['action']){
			case 'start':
				$_SESSION['user'] = $_POST['user'];
				$_SESSION['pass'] = $_POST['pass'];
				//$json_res['op'] = 'started session';
				break;
			case 'destroy':
				$_SESSION['user'] = null;
				$_SESSION['pass'] = null;
				session_destroy();
				//$json_res['op'] = 'destroyed session?';
				break;
			case 'check':
				if($_SESSION['user'] && $_SESSION['user']!=null){
					$json_res['exists'] = true;
					$json_res['user'] = $_SESSION['user'];
					$json_res['pass'] = $_SESSION['pass'];
				}
				else{
					$json_res['exists'] = false;
				}
				break;
			case 'renove':
				break;

		}
		$json_res['ok'] = true;
	}catch(Exception $e){
		$json_res['error'] = $e->getMessage();
	}	

	echo json_encode($json_res);