<?php
/**
 * Classes autoload system.
 *
 * @param string $class_name
 */
function __autoload($class_name){
    
	$path = APP_ROOT.'/core/classes';
	$dir = opendir($path);
	while ($root_name = @readdir($dir)){
		if(file_exists(APP_ROOT.'/core/classes/'.$root_name.'/'.$class_name.'.php'))
    		require_once APP_ROOT.'/core/classes/'.$root_name.'/'.$class_name.'.php';
	} 
	
    if(file_exists(APP_ROOT.'/html/zones/'.$class_name.'.php'))
    	 require_once(APP_ROOT.'/html/zones/'.$class_name.'.php');
    	 
    //DEBUG:
    if($class_name == 'FB' && file_exists( APP_ROOT.'/core/classes/Common/FirePHPCore-0.3.1/lib/FirePHPCore/fb.php')){
    	require_once APP_ROOT.'/core/classes/Common/FirePHPCore-0.3.1/lib/FirePHPCore/fb.php';
    }
    
}
?>