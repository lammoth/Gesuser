<?php

include_once('config.php');

class Gesuser {

	public $auth = false;
	
	public function __construct(){

		session_name(SESSION_NAME);
		session_start();
		
		if($_SESSION['user'] && $_SESSION['user']!=null){
			$this->auth = true;
			/*include(APP_ROOT."/php/login/login.php");
			exit();*/
		}
	}
}